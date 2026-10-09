"""OpenAI Responses API with Structured Outputs (``text.format`` = strict JSON schema).

POST https://api.openai.com/v1/responses, key in ``Authorization: Bearer``.
``store`` is false.  ``reasoning.effort`` is sent as configured (``high`` for
gpt-6-luna) and ``temperature`` only when configured (null for a reasoning
model: not sent).  Nothing is changed after an error: a rejected parameter,
an unavailable model or an exhausted quota stops the request and is reported;
no other model and no other parameter set is tried.  The Responses API has no
seed: none is sent and determinism is not claimed.

Model access is checked without generating anything: GET /v1/models/<model>.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .base import TRANSIENT_STATUS, BaseLLMProvider

DEFAULT_ENDPOINT = "https://api.openai.com/v1/responses"
DEFAULT_MODELS_ENDPOINT = "https://api.openai.com/v1/models"


class OpenAIProvider(BaseLLMProvider):
    name = "openai"
    api_key_env = "OPENAI_API_KEY"

    def endpoint(self) -> str:
        return str(self.settings.get("endpoint") or DEFAULT_ENDPOINT)

    def models_list_url(self) -> Optional[str]:
        return str(self.settings.get("models_endpoint") or DEFAULT_MODELS_ENDPOINT)

    def model_info_url(self) -> Optional[str]:
        return "{0}/{1}".format(self.models_list_url().rstrip("/"), self.model)

    def auth_headers(self, api_key: str) -> Dict[str, str]:
        return {"Authorization": "Bearer " + api_key}

    def default_parameters(self) -> Dict[str, Any]:
        return {"reasoning_effort": self.settings.get("reasoning_effort"),
                "temperature": self.settings.get("temperature"),
                "max_output_tokens": self.settings.get("max_output_tokens")}

    def request_body(self, system: str, user: str, schema: Dict[str, Any], schema_name: str,
                     parameters: Dict[str, Any]) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "model": self.model,
            "input": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "text": {"format": {"type": "json_schema", "name": schema_name, "schema": schema, "strict": True}},
            "store": False,
        }
        if parameters.get("reasoning_effort"):
            body["reasoning"] = {"effort": str(parameters["reasoning_effort"])}
        if parameters.get("temperature") is not None:
            body["temperature"] = float(parameters["temperature"])
        if parameters.get("max_output_tokens") is not None:
            body["max_output_tokens"] = int(parameters["max_output_tokens"])
        return body

    def classify_error(self, status: int, data: Any) -> str:
        error = (data or {}).get("error") if isinstance(data, dict) else None
        code = str((error or {}).get("code") or (error or {}).get("type") or "") if isinstance(error, dict) else ""
        if status == 429:
            return "quota" if code == "insufficient_quota" else "rate_limit"
        if status in TRANSIENT_STATUS:
            return "transient"
        return "fatal"

    def metadata_summary(self, data: Any) -> Dict[str, Any]:
        data = data if isinstance(data, dict) else {}
        return {key: data.get(key) for key in ("id", "object", "created", "owned_by") if key in data}

    def parse(self, data: Dict[str, Any]) -> Dict[str, Any]:
        texts, refusal = [], None
        for item in data.get("output") or []:
            if item.get("type") != "message":
                continue
            for part in item.get("content") or []:
                if part.get("type") == "output_text":
                    texts.append(part.get("text", ""))
                elif part.get("type") == "refusal":
                    refusal = part.get("refusal")
        usage = data.get("usage") or {}
        output_details = usage.get("output_tokens_details") or {}
        input_details = usage.get("input_tokens_details") or {}
        finish = data.get("status")
        if data.get("incomplete_details"):
            finish = "{0}: {1}".format(finish, (data.get("incomplete_details") or {}).get("reason"))
        return {"text": "".join(texts) if texts else None, "refusal": refusal,
                "usage": {"input_tokens": usage.get("input_tokens"),
                          "cached_input_tokens": input_details.get("cached_tokens"),
                          "output_tokens": usage.get("output_tokens"),
                          "reasoning_tokens": output_details.get("reasoning_tokens"),
                          "total_tokens": usage.get("total_tokens"),
                          "note": "output_tokens include reasoning_tokens (billed as output)",
                          "raw": usage},
                "model_reported": data.get("model"), "response_id": data.get("id"), "finish_reason": finish}
