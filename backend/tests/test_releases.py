import pytest

from app.releases import resolve

DEMO = "https://platform.claude.com/docs/en/about-claude/model-deprecations"


def test_demo_url_resolves_offline() -> None:
    src = resolve(DEMO, None)
    assert src.url == DEMO
    assert "claude-sonnet-4-5-20250929" in src.text
    assert "claude-sonnet-5-5" in src.text
    assert len(src.hash) == 64


def test_url_normalized() -> None:
    upper_host = DEMO.replace("platform.claude.com", "PLATFORM.claude.com")
    assert resolve(upper_host + "/#x", None).text == resolve(DEMO, None).text
    assert resolve(DEMO + "/?a=1#frag", None).text == resolve(DEMO, None).text


def test_release_notes_url_also_resolves() -> None:
    assert resolve("https://platform.claude.com/docs/en/release-notes/overview", None).text


def test_pasted_text_passes_through() -> None:
    src = resolve(None, "  Model X is retired.  ")
    assert src.text == "Model X is retired."
    assert src.url is None
    assert src.hash == resolve(None, "Model X is retired.").hash


def test_text_wins_and_url_is_kept() -> None:
    src = resolve("https://example.com/not-in-index", "custom text")
    assert src.text == "custom text"
    assert src.url == "https://example.com/not-in-index"


def test_unknown_url_raises() -> None:
    with pytest.raises(ValueError, match="Unknown release URL"):
        resolve("https://example.com/nope", None)


@pytest.mark.parametrize("url,text", [(None, None), ("", ""), ("  ", "\n")])
def test_empty_raises(url: str | None, text: str | None) -> None:
    with pytest.raises(ValueError, match="Provide"):
        resolve(url, text)


def test_hash_differs_for_different_text() -> None:
    assert resolve(None, "a").hash != resolve(None, "b").hash
