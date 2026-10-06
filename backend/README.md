# backend

FastAPI API, Celery worker and PydanticAI agents in one package (`app`), built into one Docker image.
See the root README and `docs/playbooks/`.

## LLM provider

The model is chosen by env only, with no provider-specific code. `LLM_MODEL` is a PydanticAI
model string; set the matching key (the clients ship as `pydantic-ai-slim` extras):

| `LLM_MODEL` | key env var |
| --- | --- |
| `test` (default) | none: offline; the resource check answers from its cache |
| `anthropic:<model>` | `ANTHROPIC_API_KEY` |
| `openai:<model>` | `OPENAI_API_KEY` |
| `google:<model>` | `GEMINI_API_KEY` |

Record a live resource-check result into the cache (works with any provider above):

```
LLM_MODEL=openai:<model> OPENAI_API_KEY=... uv run python -m app.resources.record \
  --slug llm-api-post --url <resource url>
```

A live run writes the cache. On any live error or timeout the check falls back to it.
