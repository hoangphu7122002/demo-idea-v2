import json
import uuid
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.messages import ModelMessage, ModelResponse, RetryPromptPart, ToolCallPart
from pydantic_ai.models.function import AgentInfo, FunctionModel

from app.ai.summary import NoteSummary, summarise
from app.core.db import SyncSessionLocal
from app.models import Job
from app.worker.tasks import llm_summarize_note

BODY = "Great sprint review today. The team shipped the billing page and the search fix."


def test_offline_agent_returns_structured_output() -> None:
    out = summarise(BODY)
    assert isinstance(out, NoteSummary)
    assert out.summary == "Great sprint review today."
    assert 1 <= len(out.tags) <= 5
    assert out.sentiment == "positive"


def _tool(info: AgentInfo, args: dict[str, object]) -> ModelResponse:
    return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, json.dumps(args))])


def test_invalid_output_is_retried_once() -> None:
    calls: list[int] = []

    def flaky(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        calls.append(1)
        if len(calls) == 1:  # invalid: 0 tags, bad sentiment
            return _tool(info, {"summary": "x", "tags": [], "sentiment": "ecstatic"})
        retry = [p for m in messages for p in m.parts if isinstance(p, RetryPromptPart)]
        assert retry, "second call must carry the validation error back to the model"
        return _tool(info, {"summary": "ok", "tags": ["a"], "sentiment": "neutral"})

    out = summarise("anything", model=FunctionModel(flaky))
    assert out.tags == ["a"] and len(calls) == 2


def test_gives_up_after_one_retry() -> None:
    def always_bad(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        return _tool(info, {"summary": "y" * 300, "tags": ["a"], "sentiment": "neutral"})

    with pytest.raises(UnexpectedModelBehavior):
        summarise("anything", model=FunctionModel(always_bad))


def test_summary_endpoint_queues_job_and_task_stores_result(client: TestClient) -> None:
    note = client.post("/api/notes", json={"title": "Sprint", "body": BODY}).json()
    with patch.object(llm_summarize_note, "apply_async") as enqueue:
        r = client.post(f"/api/notes/{note['id']}/summary")
    assert r.status_code == 202
    job_id = r.json()["job_id"]
    assert enqueue.call_args.kwargs["task_id"] == job_id

    llm_summarize_note.run(job_id, note["id"])  # worker body, inline
    with SyncSessionLocal() as s:
        job = s.get(Job, uuid.UUID(job_id))
        assert job is not None and job.status == "done"

    listed = client.get("/api/notes").json()[0]
    assert listed["summary"] == "Great sprint review today."
    assert listed["sentiment"] == "positive"
    assert client.get(f"/api/jobs/{job_id}").json()["result"]["tags"] == listed["tags"]


def test_summary_404_for_missing_note(client: TestClient) -> None:
    assert client.post("/api/notes/999/summary").status_code == 404
