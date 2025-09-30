from .database import engine, SessionDep
from sqlmodel import SQLModel, Field, Column
from pydantic import ConfigDict
from sqlalchemy import Boolean, text, TIMESTAMP


class PostBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    
    published: bool = Field(
        sa_column=Column(Boolean, nullable=False, server_default=text("TRUE"))
    ) #this is special for setting a default value in a postgresql database
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)

    
class Post(PostBase, table=True):
    created_at: str | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), server_default=text("now()")
        ), default="now()"
    )
    updated_at: str = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()")
        ), default=None
    )
    
    
class PostRead(PostBase):
    pass
    

class PostCreate(PostBase):
    created_at: str | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), server_default=text("now()")
        ), default="now()"
    )

class PostUpdate(PostBase):
    updated_at: str = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()")
        ), default=None
    )
    


    #model_config = ConfigDict(table_name="posts")
