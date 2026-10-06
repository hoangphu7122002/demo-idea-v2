import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select

from app.core.db import SyncSessionLocal
from app.core.settings import get_settings
from app.models import ParagraphFlag, ReleaseCheck
from app.seed import reseed

URL = "https://platform.claude.com/docs/en/about-claude/model-deprecations"
CHECK = "/api/posts/llm-api-post/check"
FLAGS = "/api/posts/llm-api-post/flags"


@pytest.fixture(autouse=True)
def _offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(get_settings(), "llm_model", "test")
    with SyncSessionLocal() as s:
        reseed(s)


def test_check_demo_url_returns_cached_flags_and_persists(client: TestClient) -> None:
    r = client.post(CHECK, json={"release_url": URL})
    assert r.status_code == 200
    body = r.json()
    assert body["source"] == "cache"
    assert body["release_url"] == URL
    assert [f["paragraph_id"] for f in body["flags"]] == ["p-6", "p-7", "p-11"]
    assert all(f["reason"] and f["source_quote"] and f["proposed_fix"] for f in body["flags"])
    with SyncSessionLocal() as s:
        assert s.scalar(select(func.count()).select_from(ReleaseCheck)) == 1
        assert s.scalar(select(func.count()).select_from(ParagraphFlag)) == 3


def test_get_flags_returns_latest_check(client: TestClient) -> None:
    assert client.get(FLAGS).json() is None  # never checked
    first = client.post(CHECK, json={"release_url": URL}).json()
    second = client.post(CHECK, json={"release_url": URL}).json()
    assert second["check_id"] > first["check_id"]
    got = client.get(FLAGS).json()
    assert got["check_id"] == second["check_id"]
    assert got["source"] is None
    assert got["flags"] == second["flags"]


def test_unknown_slug_404(client: TestClient) -> None:
    assert client.post("/api/posts/nope/check", json={"release_url": URL}).status_code == 404
    assert client.get("/api/posts/nope/flags").status_code == 404


def test_unknown_url_422_with_readable_detail(client: TestClient) -> None:
    r = client.post(CHECK, json={"release_url": "https://example.com/nope"})
    assert r.status_code == 422
    assert "Unknown release URL" in r.json()["detail"]


def test_empty_body_422(client: TestClient) -> None:
    r = client.post(CHECK, json={})
    assert r.status_code == 422
    assert "Provide a release URL" in r.json()["detail"]


def test_pasted_text_without_cache_503(client: TestClient) -> None:
    r = client.post(CHECK, json={"release_text": "Some brand new release note."})
    assert r.status_code == 503
    assert "no cached result" in r.json()["detail"]
    with SyncSessionLocal() as s:
        assert s.scalar(select(func.count()).select_from(ReleaseCheck)) == 0


def test_error_codes_declared_in_openapi(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]
    post = paths["/api/posts/{slug}/check"]["post"]["responses"]
    assert {"200", "404", "422", "503"} <= set(post)
    assert "404" in paths["/api/posts/{slug}/flags"]["get"]["responses"]
