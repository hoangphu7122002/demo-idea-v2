from pydantic import BaseModel


class PostSummary(BaseModel):
    slug: str
    title: str


class ParagraphOut(BaseModel):
    id: str  # stable "p-<db id>"
    md: str


class PostOut(BaseModel):
    slug: str
    title: str
    paragraphs: list[ParagraphOut]
