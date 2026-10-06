"""Check a post against a release note: which paragraphs does the release make outdated?

Live: PydanticAI agent with structured output (LLM_MODEL=anthropic:claude-sonnet-5-5).
Fallback: cache keyed by inputs. LLM_MODEL=test (default) and any live error/timeout use it.
A successful live run writes the cache (write-through) so a later fallback returns the same flags.
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models import Model

from app.core.settings import get_settings
from app.releases import ReleaseSource, cache

log = logging.getLogger(__name__)

LIVE_TIMEOUT_S = 20.0


class Flag(BaseModel):
    paragraph_id: str  # "p-<id>"
    reason: str
    source_quote: str  # verbatim line from the release text
    proposed_fix: str


class FlagList(BaseModel):
    flags: list[Flag]


@dataclass(frozen=True)
class CheckResult:
    flags: list[Flag]
    source: Literal["live", "cache"]


class CheckUnavailable(Exception):
    """Live check failed (or is disabled) and no cached result exists for these inputs."""


INSTRUCTIONS = (
    "You check a technical blog post against a release note. The post is a list of paragraphs, "
    "each with an id like p-3. Flag ONLY paragraphs that the release note contradicts or makes "
    "outdated; do not flag unrelated or still-correct paragraphs. For each flag give: "
    "paragraph_id (exactly as given), reason (one sentence), source_quote (a verbatim line "
    "copied from the release note) and proposed_fix (the minimal change to the paragraph). "
    "If nothing is outdated, return an empty list."
)

release_check_agent = Agent(output_type=FlagList, instructions=INSTRUCTIONS)


def _prompt(paragraphs: list[tuple[str, str]], release: ReleaseSource) -> str:
    post = "\n\n".join(f"[{pid}]\n{md}" for pid, md in paragraphs)
    return f"## Release note\n{release.text}\n\n## Post paragraphs\n{post}"


def _from_cache(key: str) -> CheckResult:
    raw = cache.load(key)
    if raw is None:
        raise CheckUnavailable(
            "Live check unavailable and no cached result for this post and release note"
        )
    return CheckResult(flags=[Flag(**f) for f in raw], source="cache")


async def check_live(
    paragraphs: list[tuple[str, str]],
    release: ReleaseSource,
    model: Model | str,
    timeout: float = LIVE_TIMEOUT_S,
) -> list[Flag]:
    """One live run; flags with unknown paragraph ids are dropped."""
    result = await asyncio.wait_for(
        release_check_agent.run(_prompt(paragraphs, release), model=model), timeout
    )
    known = {pid for pid, _ in paragraphs}
    return [f for f in result.output.flags if f.paragraph_id in known]


async def check(
    paragraphs: list[tuple[str, str]],
    release: ReleaseSource,
    model: Model | str | None = None,
    timeout: float = LIVE_TIMEOUT_S,
) -> CheckResult:
    key = cache.cache_key(paragraphs, release.text)
    live_model = model or get_settings().llm_model
    if live_model == "test":
        return _from_cache(key)
    try:
        flags = await check_live(paragraphs, release, live_model, timeout)
    except Exception as exc:  # noqa: BLE001 - any live failure falls back to the cache
        log.warning("live release check failed (%s); using cache", type(exc).__name__)
        return _from_cache(key)
    cache.save(key, [f.model_dump() for f in flags])
    return CheckResult(flags=flags, source="live")
