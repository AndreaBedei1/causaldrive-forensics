"""LLM providers: OpenAI and Gemini behind one interface (``BaseLLMProvider``).

Model policy (configs/llm.yaml): a provider with ``model_locked: true`` accepts
only its ``model`` (OpenAI: gpt-6-luna); otherwise the configured
``primary_model`` / ``secondary_model`` (Gemini: gemini-3.8-flash,
gemini-3.5-flash-lite).  Any other model is refused (:class:`ModelNotAllowed`);
nothing ever substitutes another model.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import (BaseLLMProvider, LLMResponse, ModelNotAllowed, ProviderError, ProviderUnavailable, Transport,
                   load_env_file, resolve_api_key)
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider

PROVIDERS = {"openai": OpenAIProvider, "gemini": GeminiProvider}

__all__ = ["BaseLLMProvider", "LLMResponse", "ModelNotAllowed", "ProviderError", "ProviderUnavailable", "PROVIDERS",
           "OpenAIProvider", "GeminiProvider", "allowed_models", "default_model", "make_provider", "load_env_file",
           "resolve_api_key"]


def default_model(settings: Dict[str, Any]) -> str:
    """The model a provider uses when none is asked for: ``model``, else ``primary_model``."""
    model = settings.get("model") or settings.get("primary_model")
    if not model:
        raise ModelNotAllowed("no model configured (model / primary_model)")
    return str(model)


def allowed_models(settings: Dict[str, Any]) -> List[str]:
    """The models a provider accepts: only ``model`` when locked, else the configured ones."""
    if settings.get("model_locked"):
        return [default_model(settings)]
    out: List[str] = []
    for value in [settings.get("model"), settings.get("primary_model"), settings.get("secondary_model")]:
        if value and str(value) not in out:
            out.append(str(value))
    return out


def make_provider(name: str, settings: Dict[str, Any], model: Optional[str] = None,
                  env_file: Optional[Path] = None, transport: Optional[Transport] = None) -> BaseLLMProvider:
    """A configured provider; its key comes from the environment or .env (it may be missing).

    ``model`` must be one the policy accepts; otherwise :class:`ModelNotAllowed` is raised and nothing
    else is tried.
    """
    if name not in PROVIDERS:
        raise ProviderUnavailable("unknown provider {0!r} (available: {1})".format(name, ", ".join(sorted(PROVIDERS))))
    chosen = str(model) if model else default_model(settings)
    allowed = allowed_models(settings)
    if chosen not in allowed:
        if settings.get("model_locked"):
            raise ModelNotAllowed(
                "{0} is locked to {1} for these experiments; {2!r} is refused.  Using another {0} model is a "
                "decision for Andrea: it needs his explicit approval and a change of configs/llm.yaml (model, "
                "model_locked); the tool never switches model by itself.".format(name, allowed[0], chosen))
        raise ModelNotAllowed("{0} accepts only the configured models ({1}); {2!r} is refused".format(
            name, ", ".join(allowed), chosen))
    cls = PROVIDERS[name]
    key_env = str(settings.get("api_key_env") or cls.api_key_env)
    provider = cls(model=chosen, settings=settings, api_key=resolve_api_key(key_env, env_file), transport=transport)
    provider.api_key_env = key_env
    return provider
