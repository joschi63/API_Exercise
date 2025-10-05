from ..database import engine, SessionDep
from sqlmodel import SQLModel, Field, Column, Relationship
from pydantic import BaseModel
from sqlalchemy import Boolean, text, TIMESTAMP
from datetime import datetime
from .user_models import UserRead


class PostBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(
        sa_column=Column(Boolean, nullable=False, server_default=text("TRUE"))
    ) #this is special for setting a default value in a postgresql database
    
    
class Post(PostBase, table=True):
    __tablename__ = "posts" #type: ignore
    owner_id: int = Field(foreign_key="users.id", ondelete="CASCADE", nullable=False)
    created_at: str | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
        ), default="now()"
    )
    updated_at: str = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), server_default=None
        ), default=None
    )
    #Type hinting with a string to avoid circular import
    owner: "User" = Relationship(back_populates="posts") #type: ignore
    
class PostRead(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserRead
   
    

class PostCreate(PostBase):
    created_at: str | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
        ), default="now()"
    )
    owner_id: int | None = None

class PostUpdate(PostBase):
    updated_at: str = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()")
        ), default=None
    )
    owner_id: int | None = None
    



    #model_config = ConfigDict(table_name="posts")
