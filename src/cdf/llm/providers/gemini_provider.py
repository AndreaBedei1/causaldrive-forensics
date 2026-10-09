"""Gemini API ``generateContent`` with a JSON response schema, for Gemini 3 models.

POST https://generativelanguage.googleapis.com/v1beta/models/<model>:generateContent,
key in the ``x-goog-api-key`` header (never in the URL),
``generationConfig.responseMimeType = application/json``,
``generationConfig.responseJsonSchema`` and
``generationConfig.thinkingConfig.thinkingLevel`` (``high``).

Gemini 3 keeps its default sampling: Google strongly recommends temperature
1.0 for every Gemini 3 model, so no ``temperature``, ``topP``, ``topK``,
``candidateCount`` or ``seed`` is sent, and the legacy ``thinkingBudget`` is
not sent either (a settings file that still has them is refused rather than
silently ignored).  Thinking tokens count towards ``maxOutputTokens``.

A daily quota error (``RESOURCE_EXHAUSTED`` with a per-day quota, or a retry
delay above a minute) stops the request: no other model is tried.  A per-minute
rate limit is retried after the delay the API asks for (at most a minute).

Model access is checked without generating anything: GET /v1beta/models/<model> (models.get).
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from .base import MAX_PROVIDER_RETRY_DELAY_S, TRANSIENT_STATUS, BaseLLMProvider

DEFAULT_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_MODELS_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"
# Sampling / legacy controls that are not sent to Gemini 3 (see the module docstring).
NOT_SENT_TO_GEMINI_3 = ("temperature", "top_p", "top_k", "candidate_count", "seed", "thinking_budget")


def _details(data: Any) -> List[Dict[str, Any]]:
    error = data.get("error") if isinstance(data, dict) else None
    return list(error.get("details") or []) if isinstance(error, dict) else []


def _retry_delay_s(data: Any) -> Optional[float]:
    for item in _details(data):
        if str(item.get("@type", "")).endswith("RetryInfo"):
            match = re.match(r"^\s*([0-9.]+)s\s*$", str(item.get("retryDelay", "")))
            if match:
                return float(match.group(1))
    return None


def _quota_ids(data: Any) -> List[str]:
    ids = []
    for item in _details(data):
        if str(item.get("@type", "")).endswith("QuotaFailure"):
            ids += [str(v.get("quotaId") or v.get("quotaMetric") or "") for v in item.get("violations") or []]
    return ids


class GeminiProvider(BaseLLMProvider):
    name = "gemini"
    api_key_env = "GEMINI_API_KEY"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        legacy = [key for key in NOT_SENT_TO_GEMINI_3 if self.settings.get(key) is not None]
        if legacy:
            raise ValueError("gemini settings {0} are not sent to Gemini 3 models (default sampling; thinking is "
                             "set by thinking_level): remove them from configs/llm.yaml".format(", ".join(legacy)))

    def endpoint(self) -> str:
        return str(self.settings.get("endpoint") or DEFAULT_ENDPOINT).format(model=self.model)

    def models_list_url(self) -> Optional[str]:
        return str(self.settings.get("models_endpoint") or DEFAULT_MODELS_ENDPOINT) + "?pageSize=1"

    def model_info_url(self) -> Optional[str]:
        return "{0}/{1}".format(str(self.settings.get("models_endpoint") or DEFAULT_MODELS_ENDPOINT).rstrip("/"),
                                self.model)

    def auth_headers(self, api_key: str) -> Dict[str, str]:
        return {"x-goog-api-key": api_key}

    def default_parameters(self) -> Dict[str, Any]:
        return {"thinking_level": self.settings.get("thinking_level"),
                "max_output_tokens": self.settings.get("max_output_tokens")}

    def request_body(self, system: str, user: str, schema: Dict[str, Any], schema_name: str,
                     parameters: Dict[str, Any]) -> Dict[str, Any]:
        config: Dict[str, Any] = {"responseMimeType": "application/json", "responseJsonSchema": schema}
        if parameters.get("thinking_level"):
            config["thinkingConfig"] = {"thinkingLevel": str(parameters["thinking_level"])}
        if parameters.get("max_output_tokens") is not None:
            config["maxOutputTokens"] = int(parameters["max_output_tokens"])
        return {"systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": user}]}],
                "generationConfig": config}

    def classify_error(self, status: int, data: Any) -> str:
        if status == 429:
            delay = _retry_delay_s(data)
            per_day = any("perday" in quota.lower().replace("_", "") for quota in _quota_ids(data))
            message = str(((data or {}).get("error") or {}).get("message", "")) if isinstance(data, dict) else ""
            if per_day or "per day" in message.lower() or (delay is not None and delay > MAX_PROVIDER_RETRY_DELAY_S):
                return "quota"
            return "rate_limit"
        if status in TRANSIENT_STATUS:
            return "transient"
        return "fatal"

    def retry_delay(self, status: Optional[int], data: Any, attempt: int) -> float:
        delay = _retry_delay_s(data)
        if delay is not None:
            return min(delay + 1.0, MAX_PROVIDER_RETRY_DELAY_S)
        return super().retry_delay(status, data, attempt)

    def metadata_summary(self, data: Any) -> Dict[str, Any]:
        data = data if isinstance(data, dict) else {}
        keys = ("name", "baseModelId", "version", "displayName", "inputTokenLimit", "outputTokenLimit",
                "supportedGenerationMethods", "thinking")
        return {key: data.get(key) for key in keys if key in data}

    def parse(self, data: Dict[str, Any]) -> Dict[str, Any]:
        candidates = data.get("candidates") or []
        text, finish, refusal = None, None, None
        if candidates:
            first = candidates[0]
            finish = first.get("finishReason")
            parts = (first.get("content") or {}).get("parts") or []
            texts = [part.get("text", "") for part in parts if "text" in part and not part.get("thought")]
            text = "".join(texts) if texts else None
            if finish in ("SAFETY", "RECITATION", "PROHIBITED_CONTENT", "BLOCKLIST", "SPII"):
                refusal = "finishReason " + str(finish)
        feedback = data.get("promptFeedback") or {}
        if feedback.get("blockReason"):
            refusal = "prompt blocked: {0}".format(feedback["blockReason"])
        usage = data.get("usageMetadata") or {}
        return {"text": text, "refusal": refusal,
                "usage": {"input_tokens": usage.get("promptTokenCount"),
                          "cached_input_tokens": usage.get("cachedContentTokenCount"),
                          "output_tokens": usage.get("candidatesTokenCount"),
                          "reasoning_tokens": usage.get("thoughtsTokenCount"),
                          "total_tokens": usage.get("totalTokenCount"),
                          "note": "output_tokens exclude the thinking tokens (thoughtsTokenCount)",
                          "raw": usage},
                "model_reported": data.get("modelVersion"), "response_id": data.get("responseId"),
                "finish_reason": finish}
