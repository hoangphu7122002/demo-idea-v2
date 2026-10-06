from pathlib import Path

import pytest
from pydantic_ai.models import Model, infer_model
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIResponsesModel

from app.ai import release_check
from app.core.settings import get_settings
from app.releases import ReleaseSource, cache

CASES = [
    ("anthropic:claude-sonnet-5-5", "ANTHROPIC_API_KEY", AnthropicModel),
    ("openai:gpt-5", "OPENAI_API_KEY", (OpenAIChatModel, OpenAIResponsesModel)),
    ("google:gemini-2.5-pro", "GEMINI_API_KEY", GoogleModel),
]


@pytest.mark.parametrize(("name", "key_var", "cls"), CASES)
def test_provider_string_resolves_to_a_model_without_network(
    name: str, key_var: str, cls: type | tuple[type, ...], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(key_var, "dummy-key")
    assert isinstance(infer_model(name), cls)


@pytest.mark.parametrize(("name", "key_var", "cls"), CASES)
async def test_check_passes_the_configured_model_string_through(
    name: str,
    key_var: str,
    cls: type | tuple[type, ...],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """LLM_MODEL reaches the agent unchanged: no provider-specific branch in check()."""
    monkeypatch.setattr(cache, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(get_settings(), "llm_model", name)
    seen: list[Model | str | None] = []

    class _Result:
        class output:  # noqa: N801 - minimal stand-in for AgentRunResult
            flags: list[object] = []

    async def fake_run(prompt: str, *, model: Model | str | None = None) -> _Result:
        seen.append(model)
        return _Result()

    monkeypatch.setattr(release_check.release_check_agent, "run", fake_run)
    release = ReleaseSource(url=None, text="r", hash="h")
    res = await release_check.check([("p-1", "a")], release)
    assert res.source == "live"
    assert seen == [name]
