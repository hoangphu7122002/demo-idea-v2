from sqlalchemy.orm import Session

from app.models import Note
from app.seed import register


@register("notes", (Note,))
def load(session: Session) -> None:
    session.add_all(
        [
            Note(id=1, title="Welcome", body="Demo note one."),
            Note(id=2, title="Groceries", body="milk, eggs"),
        ]
    )
