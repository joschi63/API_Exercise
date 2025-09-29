from .database import engine, SessionDep
from sqlmodel import SQLModel, Field, Column
from pydantic import ConfigDict
from sqlalchemy import Boolean, text, TIMESTAMP


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(
        sa_column=Column(Boolean, nullable=False, server_default=text("TRUE"))
    ) #this is special for setting a default value in a postgresql database
    created_at: str = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
        )
    )
    #created_at: str | None = None

    #model_config = ConfigDict(table_name="posts")
