from .database import engine, SessionDep
from sqlmodel import SQLModel, Field

class Post1(SQLModel, table=True):
    __tablename__ = "posts"
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True)
    #created_at: str | None = None
