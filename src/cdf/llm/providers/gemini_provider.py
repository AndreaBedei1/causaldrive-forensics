"""Gemini API ``generateContent`` with a JSON response schema.

POST https://generativelanguage.googleapis.com/v1beta/models/<model>:generateContent,
key in the ``x-goog-api-key`` header (never in the URL),
``generationConfig.responseMimeType = application/json`` and
``generationConfig.responseJsonSchema``.  Temperature and seed are sent when
configured; a fixed seed makes repeated calls more repeatable, not guaranteed
identical, and the analysis says so.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .base import BaseLLMProvider

DEFAULT_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class GeminiProvider(BaseLLMProvider):
    name = "gemini"
    api_key_env = "GEMINI_API_KEY"

    def endpoint(self) -> str:
        return str(self.settings.get("endpoint") or DEFAULT_ENDPOINT).format(model=self.model)

    def auth_headers(self, api_key: str) -> Dict[str, str]:
        return {"x-goog-api-key": api_key}

    def default_parameters(self) -> Dict[str, Any]:
        return {"temperature": self.settings.get("temperature"), "seed": self.settings.get("seed"),
                "max_output_tokens": self.settings.get("max_output_tokens")}

    def request_body(self, system: str, user: str, schema: Dict[str, Any], schema_name: str,
                     parameters: Dict[str, Any]) -> Dict[str, Any]:
        config: Dict[str, Any] = {"responseMimeType": "application/json", "responseJsonSchema": schema}
        if parameters.get("temperature") is not None:
            config["temperature"] = float(parameters["temperature"])
        if parameters.get("seed") is not None:
            config["seed"] = int(parameters["seed"])
        if parameters.get("max_output_tokens") is not None:
            config["maxOutputTokens"] = int(parameters["max_output_tokens"])
        return {"systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": user}]}],
                "generationConfig": config}

    def adapt_after_error(self, status: int, data: Any, parameters: Dict[str, Any]) -> Optional[str]:
        message = str((data or {}).get("error", {}).get("message", "")) if isinstance(data, dict) else ""
        if status == 400 and "seed" in message and parameters.get("seed") is not None:
            parameters["seed"] = None
            return "the model rejected 'seed'; repeated without it"
        return None

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
                          "output_tokens": usage.get("candidatesTokenCount"),
                          "reasoning_tokens": usage.get("thoughtsTokenCount"),
                          "total_tokens": usage.get("totalTokenCount")},
                "model_reported": data.get("modelVersion"), "response_id": data.get("responseId"),
                "finish_reason": finish}
