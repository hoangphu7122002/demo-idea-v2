import json
from collections.abc import AsyncIterator

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from pydantic_ai.messages import (
    FunctionToolCallEvent,
    PartDeltaEvent,
    PartStartEvent,
    TextPart,
    TextPartDelta,
)

from app.ai.agents import chat_agent, chat_model
from app.ai.limits import CHAT_LIMITS, allow

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


def _sse(payload: dict[str, str]) -> str:
    return f"data: {json.dumps(payload)}\n\n"


async def _events(message: str) -> AsyncIterator[str]:
    async with chat_agent.run_stream_events(
        message, model=chat_model(), usage_limits=CHAT_LIMITS
    ) as events:
        async for ev in events:
            if isinstance(ev, FunctionToolCallEvent):
                yield _sse({"type": "tool", "name": ev.part.tool_name})
            elif (
                isinstance(ev, PartStartEvent) and isinstance(ev.part, TextPart) and ev.part.content
            ):
                yield _sse({"type": "delta", "text": ev.part.content})
            elif isinstance(ev, PartDeltaEvent) and isinstance(ev.delta, TextPartDelta):
                yield _sse({"type": "delta", "text": ev.delta.content_delta})
    yield _sse({"type": "done"})


@router.post("", response_class=StreamingResponse)
async def chat(data: ChatIn, request: Request) -> StreamingResponse:
    if not await allow(f"chat:{request.client.host if request.client else 'anon'}"):
        raise HTTPException(429, "rate limited")
    return StreamingResponse(
        _events(data.message),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
