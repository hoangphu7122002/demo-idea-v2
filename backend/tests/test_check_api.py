import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select

from app.core.db import SyncSessionLocal
from app.core.settings import get_settings
from app.models import ParagraphFlag, PostParagraph, ResourceCheck
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
    r = client.post(CHECK, json={"resource_url": URL})
    assert r.status_code == 200
    body = r.json()
    assert body["source"] == "cache"
    assert body["resource_url"] == URL
    assert [f["paragraph_id"] for f in body["flags"]] == ["p-6", "p-7", "p-11"]
    assert all(f["reason"] and f["source_quote"] and f["proposed_fix"] for f in body["flags"])
    with SyncSessionLocal() as s:
        assert s.scalar(select(func.count()).select_from(ResourceCheck)) == 1
        stored = s.scalars(select(ParagraphFlag).order_by(ParagraphFlag.id)).all()
        assert [f.paragraph_id for f in stored] == [6, 7, 11]  # DB ids behind p-6, p-7, p-11
        assert all(f.check_id == body["check_id"] for f in stored)
        mds = [s.get(PostParagraph, f.paragraph_id).md for f in stored]  # type: ignore[union-attr]
        assert all("claude-sonnet-4-5" in md for md in mds)


def test_get_flags_returns_latest_check(client: TestClient) -> None:
    assert client.get(FLAGS).json() is None  # never checked
    first = client.post(CHECK, json={"resource_url": URL}).json()
    second = client.post(CHECK, json={"resource_url": URL}).json()
    assert second["check_id"] > first["check_id"]
    got = client.get(FLAGS).json()
    assert got["check_id"] == second["check_id"]
    assert got["source"] is None
    assert got["flags"] == second["flags"]


def test_unknown_slug_404(client: TestClient) -> None:
    assert client.post("/api/posts/nope/check", json={"resource_url": URL}).status_code == 404
    assert client.get("/api/posts/nope/flags").status_code == 404


def test_unknown_url_422_with_readable_detail(client: TestClient) -> None:
    r = client.post(CHECK, json={"resource_url": "https://example.com/nope"})
    assert r.status_code == 422
    assert "Unknown resource URL" in r.json()["detail"]


def test_empty_body_422(client: TestClient) -> None:
    r = client.post(CHECK, json={})
    assert r.status_code == 422
    assert "Provide a resource URL" in r.json()["detail"]


def test_pasted_text_without_cache_503(client: TestClient) -> None:
    r = client.post(CHECK, json={"resource_text": "Some brand new resource."})
    assert r.status_code == 503
    assert "no cached result" in r.json()["detail"]
    with SyncSessionLocal() as s:
        assert s.scalar(select(func.count()).select_from(ResourceCheck)) == 0


def test_error_codes_declared_in_openapi(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]
    post = paths["/api/posts/{slug}/check"]["post"]["responses"]
    assert {"200", "404", "422", "503"} <= set(post)
    assert "404" in paths["/api/posts/{slug}/flags"]["get"]["responses"]


def test_removed_release_fields_are_ignored(client: TestClient) -> None:
    r = client.post(CHECK, json={"release_url": URL})
    assert r.status_code == 422  # nothing usable sent: the old name no longer counts
    assert "Provide a resource URL" in r.json()["detail"]
    r = client.post(CHECK, json={"release_text": "Some brand new resource."})
    assert r.status_code == 422
    assert "Provide a resource URL" in r.json()["detail"]


def test_stray_release_field_does_not_override_resource_field(client: TestClient) -> None:
    body = {"resource_url": URL, "release_url": "https://example.com/nope"}
    r = client.post(CHECK, json=body)
    assert r.status_code == 200
    assert r.json()["resource_url"] == URL


def test_response_has_no_release_url(client: TestClient) -> None:
    assert "release_url" not in client.post(CHECK, json={"resource_url": URL}).json()
    assert "release_url" not in client.get(FLAGS).json()


def test_openapi_has_no_release_fields(client: TestClient) -> None:
    schemas = client.get("/openapi.json").json()["components"]["schemas"]
    for name in ("CheckIn", "CheckOut"):
        props = schemas[name]["properties"]
        assert "resource_url" in props
        assert not [k for k in props if k.startswith("release_")]
