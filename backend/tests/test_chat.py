from fastapi.testclient import TestClient


def test_chat_streams_tool_then_tokens(client: TestClient) -> None:
    with client.stream("POST", "/api/chat", json={"message": "hi"}) as r:
        assert r.headers["content-type"].startswith("text/event-stream")
        assert r.headers["x-accel-buffering"] == "no"
        lines = [line for line in r.iter_lines() if line.startswith("data: ")]
    assert lines[0] == 'data: {"type": "tool", "name": "current_time"}'
    assert len([x for x in lines if '"delta"' in x]) > 3
    assert lines[-1] == 'data: {"type": "done"}'
