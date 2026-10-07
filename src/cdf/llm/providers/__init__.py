"""LLM providers: OpenAI and Gemini behind one interface (``BaseLLMProvider``)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from .base import (BaseLLMProvider, LLMResponse, ProviderError, ProviderUnavailable, Transport, load_env_file,
                   resolve_api_key)
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider

PROVIDERS = {"openai": OpenAIProvider, "gemini": GeminiProvider}

__all__ = ["BaseLLMProvider", "LLMResponse", "ProviderError", "ProviderUnavailable", "PROVIDERS",
           "OpenAIProvider", "GeminiProvider", "make_provider", "load_env_file", "resolve_api_key"]


def make_provider(name: str, settings: Dict[str, Any], model: Optional[str] = None,
                  env_file: Optional[Path] = None, transport: Optional[Transport] = None) -> BaseLLMProvider:
    """A configured provider; its key comes from the environment or .env (it may be missing)."""
    if name not in PROVIDERS:
        raise ProviderUnavailable("unknown provider {0!r} (available: {1})".format(name, ", ".join(sorted(PROVIDERS))))
    cls = PROVIDERS[name]
    key_env = str(settings.get("api_key_env") or cls.api_key_env)
    provider = cls(model=model or settings["model"], settings=settings,
                   api_key=resolve_api_key(key_env, env_file), transport=transport)
    provider.api_key_env = key_env
    return provider
