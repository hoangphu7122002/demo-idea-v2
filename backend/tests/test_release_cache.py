import json
import os
import threading
from pathlib import Path

import pytest

from app.ai.release_check import CheckUnavailable, check
from app.releases import ReleaseSource, cache

FLAG = {"paragraph_id": "p-1", "reason": "r", "source_quote": "q", "proposed_fix": "f"}


@pytest.fixture(autouse=True)
def _tmp_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(cache, "CACHE_DIR", tmp_path)
    return tmp_path


def test_save_load_roundtrip_leaves_no_temp_files(tmp_path: Path) -> None:
    cache.save("k", [FLAG])
    assert cache.load("k") == [FLAG]
    assert [p.name for p in tmp_path.iterdir()] == ["k.json"]


def test_failed_save_cleans_temp_and_keeps_old_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cache.save("k", [FLAG])

    def boom(src: str, dst: object) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(os, "replace", boom)
    with pytest.raises(OSError):
        cache.save("k", [])
    assert cache.load("k") == [FLAG]
    assert [p.name for p in tmp_path.iterdir()] == ["k.json"]


def test_concurrent_save_and_load_never_see_partial_json() -> None:
    big = [{**FLAG, "reason": "x" * 20_000}] * 5
    cache.save("k", big)
    stop = threading.Event()
    bad: list[object] = []

    def writer() -> None:
        while not stop.is_set():
            cache.save("k", big)

    t = threading.Thread(target=writer)
    t.start()
    try:
        for _ in range(300):
            got = cache.load("k")
            if got != big:
                bad.append(got)
    finally:
        stop.set()
        t.join()
    assert bad == []


@pytest.mark.parametrize(
    "content",
    [
        "{not json",
        "",
        '{"flags": "nope"}',
        '{"nope": []}',
        '{"flags": [{"paragraph_id": 1}]}',
        "[]",
    ],
)
def test_corrupt_or_malformed_file_is_a_miss(tmp_path: Path, content: str) -> None:
    (tmp_path / "k.json").write_text(content, encoding="utf-8")
    assert cache.load("k") is None


async def test_corrupt_cache_means_check_unavailable_not_500(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from app.core.settings import get_settings

    monkeypatch.setattr(get_settings(), "llm_model", "test")
    paras = [("p-1", "a")]
    release = ReleaseSource(url=None, text="r", hash="h")
    (tmp_path / f"{cache.cache_key(paras, 'r')}.json").write_text("{trunc", encoding="utf-8")
    with pytest.raises(CheckUnavailable):
        await check(paras, release)


def test_valid_file_with_extra_keys_loads(tmp_path: Path) -> None:
    (tmp_path / "k.json").write_text(
        json.dumps({"flags": [{**FLAG, "extra": 1}]}), encoding="utf-8"
    )
    assert cache.load("k") == [FLAG]
