from pathlib import Path

from sqlalchemy.orm import Session

from app.models import Post, PostParagraph
from app.posts.blocks import split_blocks
from app.seed import register

FIXTURES = Path(__file__).parent / "fixtures"


def _load_fixture(name: str, *, post_id: int, slug: str, first_paragraph_id: int) -> Post:
    """Fixture = `# Title` + body. The H1 becomes the title, not a paragraph."""
    blocks = split_blocks((FIXTURES / name).read_text(encoding="utf-8"))
    title = blocks[0].removeprefix("# ").strip()
    return Post(
        id=post_id,
        slug=slug,
        title=title,
        paragraphs=[
            PostParagraph(id=first_paragraph_id + i, position=i, md=md)
            for i, md in enumerate(blocks[1:])
        ],
    )


@register("posts", (Post, PostParagraph))
def load(session: Session) -> None:
    session.add(
        _load_fixture("llm-api-post.md", post_id=1, slug="llm-api-post", first_paragraph_id=1)
    )
