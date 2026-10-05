"""PydanticAI agents. LLM_MODEL=test (default) uses an offline FunctionModel.

Switch to a real provider by env only:
    LLM_MODEL=anthropic:claude-sonnet-5-5
    (+ uv add 'pydantic-ai-slim[anthropic]' and ANTHROPIC_API_KEY in the env)
"""

import asyncio
import json
from collections.abc import AsyncIterator
from datetime import UTC, datetime

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ToolReturnPart, UserPromptPart
from pydantic_ai.models import Model
from pydantic_ai.models.function import AgentInfo, DeltaToolCall, DeltaToolCalls, FunctionModel

from app.core.settings import get_settings


def _last_user_text(messages: list[ModelMessage]) -> str:
    for msg in reversed(messages):
        for part in msg.parts:
            if isinstance(part, UserPromptPart) and isinstance(part.content, str):
                return part.content
    return ""


async def _fake_chat_stream(
    messages: list[ModelMessage], info: AgentInfo
) -> AsyncIterator[str | DeltaToolCalls]:
    """Offline model: first calls the `current_time` tool, then streams an answer word by word."""
    tool_returns = [p for m in messages for p in m.parts if isinstance(p, ToolReturnPart)]
    if not tool_returns:
        yield {0: DeltaToolCall(name="current_time", json_args=json.dumps({}), tool_call_id="t1")}
        return
    answer = f"You said: {_last_user_text(messages)!r}. Server time is {tool_returns[-1].content}."
    for word in answer.split(" "):
        await asyncio.sleep(0.05)
        yield word + " "


def chat_model() -> Model | str:
    name = get_settings().llm_model
    if name == "test":
        return FunctionModel(stream_function=_fake_chat_stream, model_name="offline-chat")
    return name


chat_agent = Agent(instructions="You are a concise assistant for a notes app.")


@chat_agent.tool_plain
def current_time() -> str:
    """Return the current UTC time (ISO 8601)."""
    return datetime.now(UTC).strftime("%H:%M:%S UTC")
