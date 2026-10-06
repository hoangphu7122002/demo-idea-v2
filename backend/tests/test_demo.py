import pytest
from fastapi.testclient import TestClient

from app.core.settings import get_settings


def test_reset_404_when_demo_mode_off(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(get_settings(), "demo_mode", False)
    assert client.post("/api/demo/reset").status_code == 404


def test_reset_restores_seed_when_demo_mode_on(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(get_settings(), "demo_mode", True)
    r = client.post("/api/demo/reset")
    assert r.status_code == 200
    counts = r.json()["counts"]
    assert counts["notes"] == 2
    assert counts["posts"] == 1
    assert counts["post_paragraphs"] >= 8
    client.post("/api/notes", json={"title": "extra", "body": "x"})
    assert len(client.get("/api/notes").json()) == 3
    assert client.post("/api/demo/reset").status_code == 200
    assert len(client.get("/api/notes").json()) == 2
