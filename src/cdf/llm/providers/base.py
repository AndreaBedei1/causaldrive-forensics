"""Provider interface, API keys from the environment / ``.env``, HTTP with retries.

API keys are read from the process environment or from the repository's
``.env`` (ignored by git).  A key is held by the provider object only, sent only
in the request header, and never written, printed, logged or put in an
exception: every error text passes through :func:`redact`.  A provider
without a key is *unavailable*; asking it for a completion raises
:class:`ProviderUnavailable`, which the pipeline reports without crashing.

Requests go through ``transport(url, headers, body, timeout_s)`` returning
``(status, parsed_json)``; the default uses ``urllib``, tests inject a fake.

Nothing about a request changes between attempts: no parameter is dropped and
no other model is tried after an error.  An error is classified (``quota``,
``rate_limit``, ``transient``, ``network``, ``timeout``, ``fatal``); only
``rate_limit``, ``transient`` and ``network`` errors (and ``timeout`` when the
provider allows it) are retried, at most ``max_retries`` times.  A quota error
stops at once.
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
BeforeSend = Callable[[str, Dict[str, Any]], None]
RETRYABLE_STATUS = (408, 409, 429, 500, 502, 503, 504)
TRANSIENT_STATUS = (408, 409, 500, 502, 503, 504)
RETRYABLE_KINDS = ("rate_limit", "transient", "network")
REDACTED = "<redacted>"
MAX_PROVIDER_RETRY_DELAY_S = 60.0


class ProviderUnavailable(RuntimeError):
    """No API key (or no such provider): no request can be made."""


class ModelNotAllowed(ValueError):
    """A model outside the configured policy was requested: nothing is sent, nothing is substituted."""


class ProviderError(RuntimeError):
    """The provider answered with an error, after retries.  ``kind`` classifies it (``quota``: stop)."""

    def __init__(self, message: str, status: Optional[int] = None, attempts: Optional[List[Dict[str, Any]]] = None,
                 kind: str = "fatal"):
        super().__init__(message)
        self.status = status
        self.attempts = attempts or []
        self.kind = kind


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


def redact_json(value: Any, secrets: List[Optional[str]]) -> Any:
    """A JSON value with every secret replaced (round-tripped through text)."""
    if value is None:
        return None
    return json.loads(redact(json.dumps(value, ensure_ascii=False), secrets))


def _read_error(error: urllib.error.HTTPError) -> Any:
    payload = error.read().decode("utf-8", "replace")
    try:
        return json.loads(payload)
    except ValueError:
        return {"error": {"message": payload[:2000]}}


def urllib_transport(url: str, headers: Dict[str, str], body: Dict[str, Any], timeout_s: float) -> Tuple[int, Any]:
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        return error.code, _read_error(error)


def urllib_get(url: str, headers: Dict[str, str], timeout_s: float) -> Tuple[int, Any]:
    """GET returning ``(status, parsed_json)``; used for model metadata (no generation)."""
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        return error.code, _read_error(error)


def _is_timeout(exc: BaseException) -> bool:
    if isinstance(exc, (socket.timeout, TimeoutError)):
        return True
    return isinstance(exc, urllib.error.URLError) and isinstance(getattr(exc, "reason", None),
                                                                 (socket.timeout, TimeoutError))


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
    raw_response: Optional[Dict[str, Any]] = None  # the provider's response body (secrets redacted)
    sent_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"provider": self.provider, "model": self.model, "model_reported": self.model_reported,
                "response_id": self.response_id, "finish_reason": self.finish_reason, "refusal": self.refusal,
                "usage": self.usage, "latency_s": self.latency_s, "sent_at": self.sent_at, "attempts": self.attempts,
                "parameters_sent": self.parameters_sent, "parse_error": self.parse_error, "notes": self.notes}


class BaseLLMProvider(ABC):
    """A structured-output completion: system + user prompt, JSON schema -> JSON object."""

    name = ""
    api_key_env = ""

    def __init__(self, model: str, settings: Optional[Dict[str, Any]] = None, api_key: Optional[str] = None,
                 transport: Optional[Transport] = None, sleep: Callable[[float], None] = time.sleep,
                 getter: Optional[Callable[[str, Dict[str, str], float], Tuple[int, Any]]] = None) -> None:
        self.model = str(model)
        self.settings = dict(settings or {})
        self._api_key = api_key
        self._transport = transport or urllib_transport
        self._getter = getter or urllib_get
        self._sleep = sleep
        self.timeout_s = float(self.settings.get("timeout_s", 300))
        self.max_retries = int(self.settings.get("max_retries", 3))
        self.retry_on_timeout = bool(self.settings.get("retry_on_timeout", True))

    @property
    def available(self) -> bool:
        return bool(self._api_key)

    def describe(self) -> Dict[str, Any]:
        """Safe to save: never the key."""
        return {"provider": self.name, "model": self.model, "api_key_env": self.api_key_env,
                "api_key_present": self.available, "generation_settings": self.generation_settings()}

    def generation_settings(self) -> Dict[str, Any]:
        """What shapes the generation (reasoning / thinking level, output cap), for the records."""
        return {key: value for key, value in self.default_parameters().items() if value is not None}

    # -- error policy (override per provider) ---------------------------------------

    def classify_error(self, status: int, data: Any) -> str:
        """``quota`` (stop), ``rate_limit`` / ``transient`` (retry, limited) or ``fatal``."""
        if status == 429:
            return "rate_limit"
        if status in TRANSIENT_STATUS:
            return "transient"
        return "fatal"

    def retry_delay(self, status: Optional[int], data: Any, attempt: int) -> float:
        return min(2.0 ** (attempt - 1), 30.0)

    # -- model access (no generation) ----------------------------------------------

    def model_info_url(self) -> Optional[str]:
        """URL of the model's metadata (GET, no generation), or None."""
        return None

    def models_list_url(self) -> Optional[str]:
        """URL listing models (GET), used to tell a bad key from an inaccessible model."""
        return None

    def check_access(self) -> Dict[str, Any]:
        """Key validity and access to ``self.model`` from metadata endpoints only: nothing is generated.

        Returns ``{key_valid, model_access, http_status, error, model_metadata}``; ``error`` is redacted.
        """
        if not self.available:
            return {"key_valid": None, "model_access": None, "http_status": None,
                    "error": "{0} is not set in the environment or in .env".format(self.api_key_env),
                    "model_metadata": None}
        secrets = [self._api_key]
        headers = self.auth_headers(self._api_key)
        try:
            status, data = self._getter(self.model_info_url(), headers, min(self.timeout_s, 60.0))
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as exc:
            return {"key_valid": None, "model_access": None, "http_status": None,
                    "error": redact("{0}: {1}".format(type(exc).__name__, exc), secrets), "model_metadata": None}
        if 200 <= status < 300:
            return {"key_valid": True, "model_access": True, "http_status": status, "error": None,
                    "model_metadata": redact_json(self.metadata_summary(data), secrets)}
        error = redact(_error_message(data), secrets)
        key_valid: Optional[bool] = False if status in (401,) else None
        if key_valid is None and self.models_list_url():
            try:
                list_status, _ = self._getter(self.models_list_url(), headers, min(self.timeout_s, 60.0))
                key_valid = True if 200 <= list_status < 300 else (False if list_status in (400, 401, 403) else None)
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError):
                key_valid = None
        del headers
        return {"key_valid": key_valid, "model_access": False, "http_status": status,
                "error": "{0} {1}".format(_error_status(data) or "", error[:300]).strip(), "model_metadata": None}

    def metadata_summary(self, data: Any) -> Dict[str, Any]:
        """The non-secret parts of a model-metadata response worth recording."""
        return dict(data) if isinstance(data, dict) else {}

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

    # -- shared ------------------------------------------------------------

    def preview(self, system: str, user: str, schema: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
        """What would be sent, with the key header redacted (for --dry-run)."""
        parameters = self.default_parameters()
        headers = dict(self.auth_headers(REDACTED), **{"Content-Type": "application/json"})
        return {"url": self.endpoint(), "headers": headers,
                "body": self.request_body(system, user, schema, schema_name, parameters)}

    def generate(self, system: str, user: str, schema: Dict[str, Any], schema_name: str,
                 before_send: Optional[BeforeSend] = None) -> LLMResponse:
        """One structured completion.  The same body (same model, same parameters) on every attempt.

        ``before_send(url, body)`` runs before every attempt and may raise to stop the request
        (a pre-send payload audit); nothing is sent then.
        """
        if not self.available:
            raise ProviderUnavailable("{0}: no API key ({1} is not set in the environment or in .env)".format(
                self.name, self.api_key_env))
        secrets = [self._api_key]
        parameters = self.default_parameters()
        attempts: List[Dict[str, Any]] = []
        notes: List[str] = []
        started = time.monotonic()
        sent_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        attempt = 0
        while True:
            attempt += 1
            body = self.request_body(system, user, schema, schema_name, parameters)
            if before_send is not None:
                before_send(self.endpoint(), body)
            headers = dict(self.auth_headers(self._api_key), **{"Content-Type": "application/json"})
            t0 = time.monotonic()
            status, data, error, timed_out = None, None, None, False
            try:
                status, data = self._transport(self.endpoint(), headers, body, self.timeout_s)
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as exc:
                error = redact("{0}: {1}".format(type(exc).__name__, exc), secrets)
                timed_out = _is_timeout(exc)
            del headers
            record = {"attempt": attempt, "status": status, "seconds": round(time.monotonic() - t0, 3)}
            if error is None and status is not None and 200 <= status < 300:
                attempts.append(record)
                break
            if error is not None:
                kind = "timeout" if timed_out else "network"
            else:
                kind = self.classify_error(status, data)
            message = error or redact(_error_message(data), secrets)
            record.update(kind=kind, error=message[:2000])
            if data is not None:
                record["error_body"] = redact_json(data, secrets)
            attempts.append(record)
            retryable = kind in RETRYABLE_KINDS or (kind == "timeout" and self.retry_on_timeout)
            if not retryable or attempt > self.max_retries:
                raise ProviderError("{0}: request failed [{1}] ({2})".format(self.name, kind, message[:500]),
                                    status, attempts, kind=kind)
            self._sleep(self.retry_delay(status, data, attempt))
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
                           notes=notes, raw_response=redact_json(data, secrets), sent_at=sent_at)


def _error_message(data: Any) -> str:
    if isinstance(data, dict):
        error = data.get("error")
        if isinstance(error, dict):
            return str(error.get("message") or error)
        if error:
            return str(error)
    return json.dumps(data)[:2000] if data is not None else "no response"


def _error_status(data: Any) -> Optional[str]:
    """The provider's symbolic error status / code (e.g. NOT_FOUND, model_not_found), if any."""
    if isinstance(data, dict) and isinstance(data.get("error"), dict):
        error = data["error"]
        return str(error.get("status") or error.get("code") or error.get("type") or "") or None
    return None
