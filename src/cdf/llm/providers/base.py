"""Provider interface, API keys from the environment / ``.env``, HTTP with retries.

API keys are read from the process environment or from the repository's
``.env`` (ignored by git).  A key is held by the provider object only, sent only
in the request header, and never written, printed, logged or put in an
exception: every error text passes through :func:`redact`.  A provider
without a key is *unavailable*; asking it for a completion raises
:class:`ProviderUnavailable`, which the pipeline reports without crashing.

Requests go through ``transport(url, headers, body, timeout_s)`` returning
``(status, parsed_json)``; the default uses ``urllib``, tests inject a fake.
"""

from __future__ import annotations

import json
import os
import socket
import time
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from ...common.config import repo_root

Transport = Callable[[str, Dict[str, str], Dict[str, Any], float], Tuple[int, Any]]
RETRYABLE_STATUS = (408, 409, 429, 500, 502, 503, 504)
REDACTED = "<redacted>"


class ProviderUnavailable(RuntimeError):
    """No API key (or no such provider): no request can be made."""


class ProviderError(RuntimeError):
    """The provider answered with an error, after retries."""

    def __init__(self, message: str, status: Optional[int] = None, attempts: Optional[List[Dict[str, Any]]] = None):
        super().__init__(message)
        self.status = status
        self.attempts = attempts or []


def env_file_path() -> Path:
    return repo_root() / ".env"


def load_env_file(path: Optional[Path] = None) -> Dict[str, str]:
    """KEY=VALUE lines of a .env file ({} when absent); comments and blanks ignored."""
    path = Path(path or env_file_path())
    values: Dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key.startswith("export "):
            key = key[len("export "):].strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key] = value
    return values


def resolve_api_key(env_name: str, env_file: Optional[Path] = None) -> Optional[str]:
    """The key from the environment, else from .env; None when missing or empty."""
    value = os.environ.get(env_name)
    if not value:
        value = load_env_file(env_file).get(env_name)
    value = (value or "").strip()
    return value or None


def redact(text: Any, secrets: List[Optional[str]]) -> str:
    out = str(text)
    for secret in secrets:
        if secret:
            out = out.replace(secret, REDACTED)
    return out


def urllib_transport(url: str, headers: Dict[str, str], body: Dict[str, Any], timeout_s: float) -> Tuple[int, Any]:
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        payload = error.read().decode("utf-8", "replace")
        try:
            parsed = json.loads(payload)
        except ValueError:
            parsed = {"error": {"message": payload[:2000]}}
        return error.code, parsed


@dataclass
class LLMResponse:
    """One completed request (after retries)."""

    provider: str
    model: str
    text: Optional[str]
    parsed: Optional[Dict[str, Any]]
    parse_error: Optional[str]
    usage: Dict[str, Any]
    latency_s: float
    attempts: List[Dict[str, Any]]
    parameters_sent: Dict[str, Any]
    model_reported: Optional[str] = None
    response_id: Optional[str] = None
    finish_reason: Optional[str] = None
    refusal: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"provider": self.provider, "model": self.model, "model_reported": self.model_reported,
                "response_id": self.response_id, "finish_reason": self.finish_reason, "refusal": self.refusal,
                "usage": self.usage, "latency_s": self.latency_s, "attempts": self.attempts,
                "parameters_sent": self.parameters_sent, "parse_error": self.parse_error, "notes": self.notes}


class BaseLLMProvider(ABC):
    """A structured-output completion: system + user prompt, JSON schema -> JSON object."""

    name = ""
    api_key_env = ""

    def __init__(self, model: str, settings: Optional[Dict[str, Any]] = None, api_key: Optional[str] = None,
                 transport: Optional[Transport] = None, sleep: Callable[[float], None] = time.sleep) -> None:
        self.model = str(model)
        self.settings = dict(settings or {})
        self._api_key = api_key
        self._transport = transport or urllib_transport
        self._sleep = sleep
        self.timeout_s = float(self.settings.get("timeout_s", 300))
        self.max_retries = int(self.settings.get("max_retries", 3))

    @property
    def available(self) -> bool:
        return bool(self._api_key)

    def describe(self) -> Dict[str, Any]:
        """Safe to save: never the key."""
        return {"provider": self.name, "model": self.model, "api_key_env": self.api_key_env,
                "api_key_present": self.available}

    # -- to implement ------------------------------------------------------

    @abstractmethod
    def endpoint(self) -> str:
        """Request URL (must not contain the key)."""

    @abstractmethod
    def auth_headers(self, api_key: str) -> Dict[str, str]:
        """The header(s) carrying the key."""

    @abstractmethod
    def request_body(self, system: str, user: str, schema: Dict[str, Any], schema_name: str,
                     parameters: Dict[str, Any]) -> Dict[str, Any]:
        """The JSON body."""

    @abstractmethod
    def default_parameters(self) -> Dict[str, Any]:
        """Sampling parameters from the settings (None = not sent)."""

    @abstractmethod
    def parse(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """{text, usage, model_reported, response_id, finish_reason, refusal} from a response body."""

    def adapt_after_error(self, status: int, data: Any, parameters: Dict[str, Any]) -> Optional[str]:
        """Change ``parameters`` in place after a rejected request and return a note, or None to give up."""
        return None

    # -- shared ------------------------------------------------------------

    def preview(self, system: str, user: str, schema: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
        """What would be sent, with the key header redacted (for --dry-run)."""
        parameters = self.default_parameters()
        headers = dict(self.auth_headers(REDACTED), **{"Content-Type": "application/json"})
        return {"url": self.endpoint(), "headers": headers,
                "body": self.request_body(system, user, schema, schema_name, parameters)}

    def generate(self, system: str, user: str, schema: Dict[str, Any], schema_name: str) -> LLMResponse:
        if not self.available:
            raise ProviderUnavailable("{0}: no API key ({1} is not set in the environment or in .env)".format(
                self.name, self.api_key_env))
        secrets = [self._api_key]
        parameters = self.default_parameters()
        attempts: List[Dict[str, Any]] = []
        notes: List[str] = []
        started = time.monotonic()
        attempt = 0
        adapted = 0
        while True:
            attempt += 1
            body = self.request_body(system, user, schema, schema_name, parameters)
            headers = dict(self.auth_headers(self._api_key), **{"Content-Type": "application/json"})
            t0 = time.monotonic()
            status, data, error = None, None, None
            try:
                status, data = self._transport(self.endpoint(), headers, body, self.timeout_s)
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as exc:
                error = redact("{0}: {1}".format(type(exc).__name__, exc), secrets)
            del headers
            record = {"attempt": attempt, "status": status, "seconds": round(time.monotonic() - t0, 3)}
            if error is None and status is not None and 200 <= status < 300:
                attempts.append(record)
                break
            message = error or redact(_error_message(data), secrets)
            record["error"] = message[:2000]
            attempts.append(record)
            if status is not None and status not in RETRYABLE_STATUS and adapted < 2:
                note = self.adapt_after_error(status, data, parameters)
                if note:
                    adapted += 1
                    notes.append(note)
                    continue
            retryable = error is not None or status in RETRYABLE_STATUS
            if not retryable or attempt > self.max_retries:
                raise ProviderError("{0}: request failed ({1})".format(self.name, message[:500]), status, attempts)
            self._sleep(min(2.0 ** (attempt - 1), 30.0))
        parsed_fields = self.parse(data)
        text = parsed_fields.get("text")
        parsed, parse_error = None, None
        if text is not None:
            try:
                parsed = json.loads(text)
                if not isinstance(parsed, dict):
                    parsed, parse_error = None, "the answer is JSON but not an object"
            except ValueError as exc:
                parse_error = "the answer is not valid JSON: {0}".format(exc)
        elif parsed_fields.get("refusal"):
            parse_error = "the model refused"
        else:
            parse_error = "no text in the response"
        return LLMResponse(provider=self.name, model=self.model, text=text, parsed=parsed, parse_error=parse_error,
                           usage=parsed_fields.get("usage") or {}, latency_s=round(time.monotonic() - started, 3),
                           attempts=attempts, parameters_sent=dict(parameters),
                           model_reported=parsed_fields.get("model_reported"),
                           response_id=parsed_fields.get("response_id"),
                           finish_reason=parsed_fields.get("finish_reason"), refusal=parsed_fields.get("refusal"),
                           notes=notes)


def _error_message(data: Any) -> str:
    if isinstance(data, dict):
        error = data.get("error")
        if isinstance(error, dict):
            return str(error.get("message") or error)
        if error:
            return str(error)
    return json.dumps(data)[:2000] if data is not None else "no response"
