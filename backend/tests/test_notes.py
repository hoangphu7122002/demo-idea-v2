from fastapi.testclient import TestClient


def test_create_and_list_notes(client: TestClient) -> None:
    r = client.post("/api/notes", json={"title": "Groceries", "body": "milk, eggs"})
    assert r.status_code == 201
    created = r.json()
    assert created["title"] == "Groceries"

    r = client.get("/api/notes")
    assert r.status_code == 200
    assert [n["id"] for n in r.json()] == [created["id"]]


def test_rejects_empty_title(client: TestClient) -> None:
    assert client.post("/api/notes", json={"title": "", "body": "x"}).status_code == 422


def test_title_is_trimmed(client: TestClient) -> None:
    r = client.post("/api/notes", json={"title": "  Trim me  ", "body": "x"})
    assert r.json()["title"] == "Trim me"
