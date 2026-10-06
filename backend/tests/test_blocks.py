from app.models.post import PostParagraph, paragraph_ref
from app.posts.blocks import split_blocks


def test_paragraphs_split_on_blank_lines() -> None:
    assert split_blocks("one\ntwo\n\nthree") == ["one\ntwo", "three"]


def test_heading_is_own_block() -> None:
    assert split_blocks("# Title\ntext\n\n## Sub") == ["# Title", "text", "## Sub"]


def test_code_fence_with_blank_lines_is_one_block() -> None:
    md = "intro\n\n```py\na = 1\n\n\nb = 2\n```\n\nafter"
    assert split_blocks(md) == ["intro", "```py\na = 1\n\n\nb = 2\n```", "after"]


def test_math_block_is_one_block() -> None:
    md = "before\n\n$$\nx = 1\n\ny = 2\n$$\n\nafter"
    assert split_blocks(md) == ["before", "$$\nx = 1\n\ny = 2\n$$", "after"]


def test_single_line_math() -> None:
    assert split_blocks("$$x^2$$\n\ntext") == ["$$x^2$$", "text"]


def test_fence_containing_math_marker_wins() -> None:
    md = "```\n$$\n\nnot math\n```\n\nafter"
    assert split_blocks(md) == ["```\n$$\n\nnot math\n```", "after"]


def test_math_containing_fence_marker_stays_math() -> None:
    md = "$$\n```\n\n$$\n\nafter"
    assert split_blocks(md) == ["$$\n```\n\n$$", "after"]


def test_list_and_quote_are_single_blocks() -> None:
    md = "- a\n- b\n  more\n\n> q1\n> q2\n\ntext"
    assert split_blocks(md) == ["- a\n- b\n  more", "> q1\n> q2", "text"]


def test_tilde_fence_and_unclosed_fence() -> None:
    assert split_blocks("~~~\na\n\nb\n~~~") == ["~~~\na\n\nb\n~~~"]
    assert split_blocks("```\na\n\nb") == ["```\na\n\nb"]


def test_empty() -> None:
    assert split_blocks("") == []
    assert split_blocks("\n\n") == []


def test_paragraph_ref_derives_from_db_id() -> None:
    assert paragraph_ref(7) == "p-7"
    assert PostParagraph(id=7, post_id=1, position=0, md="x").ref == "p-7"
