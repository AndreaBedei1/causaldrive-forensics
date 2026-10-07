"""OpenAI Responses API with Structured Outputs (``text.format`` = strict JSON schema).

POST https://api.openai.com/v1/responses, key in ``Authorization: Bearer``.
``store`` is false.  Temperature is sent when configured; some reasoning models
reject it, in which case the request is repeated once without it and the
analysis records that sampling was not pinned.  The Responses API has no seed:
none is sent and determinism is not claimed.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .base import BaseLLMProvider

DEFAULT_ENDPOINT = "https://api.openai.com/v1/responses"


class OpenAIProvider(BaseLLMProvider):
    name = "openai"
    api_key_env = "OPENAI_API_KEY"

    def endpoint(self) -> str:
        return str(self.settings.get("endpoint") or DEFAULT_ENDPOINT)

    def auth_headers(self, api_key: str) -> Dict[str, str]:
        return {"Authorization": "Bearer " + api_key}

    def default_parameters(self) -> Dict[str, Any]:
        return {"temperature": self.settings.get("temperature"),
                "max_output_tokens": self.settings.get("max_output_tokens"),
                "reasoning_effort": self.settings.get("reasoning_effort"),
                "seed": None}

    def request_body(self, system: str, user: str, schema: Dict[str, Any], schema_name: str,
                     parameters: Dict[str, Any]) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "model": self.model,
            "input": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "text": {"format": {"type": "json_schema", "name": schema_name, "schema": schema, "strict": True}},
            "store": False,
        }
        if parameters.get("temperature") is not None:
            body["temperature"] = float(parameters["temperature"])
        if parameters.get("max_output_tokens") is not None:
            body["max_output_tokens"] = int(parameters["max_output_tokens"])
        if parameters.get("reasoning_effort"):
            body["reasoning"] = {"effort": str(parameters["reasoning_effort"])}
        return body

    def adapt_after_error(self, status: int, data: Any, parameters: Dict[str, Any]) -> Optional[str]:
        message = str((data or {}).get("error", {}).get("message", "")) if isinstance(data, dict) else ""
        if status == 400 and "temperature" in message and parameters.get("temperature") is not None:
            parameters["temperature"] = None
            return "the model rejected 'temperature'; repeated without it (sampling not pinned)"
        if status == 400 and "reasoning" in message and parameters.get("reasoning_effort"):
            parameters["reasoning_effort"] = None
            return "the model rejected 'reasoning.effort'; repeated without it"
        return None

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
        details = usage.get("output_tokens_details") or {}
        finish = data.get("status")
        if data.get("incomplete_details"):
            finish = "{0}: {1}".format(finish, (data.get("incomplete_details") or {}).get("reason"))
        return {"text": "".join(texts) if texts else None, "refusal": refusal,
                "usage": {"input_tokens": usage.get("input_tokens"), "output_tokens": usage.get("output_tokens"),
                          "reasoning_tokens": details.get("reasoning_tokens"),
                          "total_tokens": usage.get("total_tokens")},
                "model_reported": data.get("model"), "response_id": data.get("id"), "finish_reason": finish}
