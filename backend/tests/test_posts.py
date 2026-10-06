from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.db import SyncSessionLocal
from app.models import PostParagraph
from app.seed import reseed


def _seed() -> None:
    with SyncSessionLocal() as s:
        reseed(s)


def test_list_posts(client: TestClient) -> None:
    _seed()
    r = client.get("/api/posts")
    assert r.status_code == 200
    assert r.json() == [{"slug": "llm-api-post", "title": "Calling the Claude API from Python"}]


def test_get_post_ordered_with_stable_ids(client: TestClient) -> None:
    _seed()
    r = client.get("/api/posts/llm-api-post")
    assert r.status_code == 200
    body = r.json()
    assert body["slug"] == "llm-api-post"
    paras = body["paragraphs"]
    assert len(paras) == 20
    with SyncSessionLocal() as s:  # order must follow `position`, ids must be the DB ids
        rows = s.execute(
            select(PostParagraph.id, PostParagraph.md).order_by(PostParagraph.position)
        ).all()
    assert [(p["id"], p["md"]) for p in paras] == [(f"p-{i}", md) for i, md in rows]
    assert [p["id"] for p in paras] == [f"p-{i}" for i in range(1, 21)]
    assert paras[0]["md"].startswith("This post walks")


def test_unknown_post_404(client: TestClient) -> None:
    assert client.get("/api/posts/nope").status_code == 404


def test_404_declared_in_openapi(client: TestClient) -> None:
    spec = client.get("/openapi.json").json()["paths"]
    assert "404" in spec["/api/posts/{slug}"]["get"]["responses"]
    assert "404" in spec["/api/demo/reset"]["post"]["responses"]
