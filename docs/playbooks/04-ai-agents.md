# 4 · AI agents (PydanticAI)

## What's there

| File | Agent | Pattern |
|---|---|---|
| `backend/app/ai/agents.py` | `chat_agent` | streaming text + a tool (`current_time`), served as SSE by `api/routes/chat.py` |
| `backend/app/ai/summary.py` | `summary_agent` | structured output (`NoteSummary`), 1 retry on invalid output, run in a Celery task |
| `backend/app/ai/limits.py` | | `UsageLimits` per run + a Redis fixed-window rate limit per client |

## Offline by default

`LLM_MODEL=test` (the default in `.env.example`) swaps every agent to a `FunctionModel`, a deterministic fake that needs no key. Dev, tests and CI never call a real LLM.

Each agent gets its model from one function (`chat_model()`, `summary_model()`), so the switch lives in one place.

## Switch to a real model

1. Add the provider extra: `cd backend && uv add 'pydantic-ai-slim[anthropic]'` (or `[openai]`, `[google]`).
2. In `.env`:

```sh
LLM_MODEL=anthropic:claude-sonnet-5-5
ANTHROPIC_API_KEY=your-key
```

3. Restart `make dev`. Never commit keys: `.env` is git-ignored. In production, inject them as secrets.

## Add an agent

1. New file in `backend/app/ai/`, with:
   - the output model (Pydantic) if you need structured data,
   - `Agent(output_type=..., instructions=..., retries={"output": 1})`,
   - an offline `FunctionModel` that returns a realistic answer,
   - a `*_model()` function: offline when `LLM_MODEL=test`, else the configured name.
2. Decide where it runs: SSE in the API for interactive streaming; a Celery `llm_*` task for anything slow or batch (see [Add a feature](02-add-a-feature.md#sync-or-async)).
3. Tests: one happy path with the offline model; one where the model first returns invalid output (check that it retries); one where it always fails (check the error path). See `backend/tests/test_summary.py`.

## Streaming contract (chat)

`POST /api/chat` returns `text/event-stream`. Each frame is `data: <json>\n\n`:

```text
data: {"type": "tool", "name": "current_time"}
data: {"type": "delta", "text": "You "}
data: {"type": "done"}
```

The frontend reads it with `readSse()` in `frontend/src/features/chat/sse.ts`.
The response sets `X-Accel-Buffering: no` so nginx doesn't buffer it. Any proxy in front (load balancer, CDN) needs an idle timeout of at least 300 s.

Want the Vercel AI SDK (`useChat`) instead? PydanticAI ships a Vercel AI adapter that speaks its stream protocol; swap the route body and use `@ai-sdk/react` in the frontend.

## Production guardrails

| Risk | Guardrail in this template | Next step when needed |
|---|---|---|
| runaway tool loops | `UsageLimits(request_limit=5)` | tune per agent |
| abuse / cost spikes | Redis rate limit, 30 requests/min per client | per-user quotas once there is auth |
| provider 429s | slow LLM work isolated on the `llm` queue; agent retries only invalid output | `autoretry_for` + backoff on `llm_*` tasks, and a global concurrency cap in Redis |
| no visibility | | Logfire or OpenTelemetry: tokens, cost and latency per run |
