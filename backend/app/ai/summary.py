"""Note summary agent: structured output, offline deterministic model by default.

Real provider by env only: LLM_MODEL=anthropic:claude-sonnet-5-5
"""

import json
import re
from collections import Counter
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelResponse, ToolCallPart, UserPromptPart
from pydantic_ai.models import Model
from pydantic_ai.models.function import AgentInfo, FunctionModel

from app.core.settings import get_settings


class NoteSummary(BaseModel):
    summary: str = Field(max_length=200)
    tags: list[str] = Field(min_length=1, max_length=5)
    sentiment: Literal["positive", "neutral", "negative"]


summary_agent = Agent(
    output_type=NoteSummary,
    instructions="Summarise the note in one sentence (max 200 chars), 1-5 short lowercase tags, "
    "and its sentiment.",
    retries={"output": 1},
)

_POS = {"good", "great", "love", "happy", "excellent", "win", "nice"}
_NEG = {"bad", "sad", "hate", "angry", "terrible", "fail", "broken"}
_STOP = {"the", "and", "with", "this", "that", "from", "have", "for", "are", "was"}


def offline_summary(text: str) -> NoteSummary:
    """Deterministic stand-in for an LLM."""
    words = re.findall(r"[a-z']+", text.lower())
    first = re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0]
    tags = [w for w, _ in Counter(w for w in words if len(w) > 3 and w not in _STOP).most_common(3)]
    pos, neg = len(set(words) & _POS), len(set(words) & _NEG)
    sentiment = "positive" if pos > neg else "negative" if neg > pos else "neutral"
    return NoteSummary(summary=first[:200], tags=tags or ["note"], sentiment=sentiment)


def _prompt(messages: list[ModelMessage]) -> str:
    for part in messages[0].parts:
        if isinstance(part, UserPromptPart) and isinstance(part.content, str):
            return part.content
    return ""


def _offline_model(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
    args = offline_summary(_prompt(messages)).model_dump()
    return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, json.dumps(args))])


def summary_model() -> Model | str:
    name = get_settings().llm_model
    return FunctionModel(_offline_model, model_name="offline-summary") if name == "test" else name


def summarise(text: str, model: Model | str | None = None) -> NoteSummary:
    return summary_agent.run_sync(text, model=model or summary_model()).output
