#from ..database import engine, SessionDep
from sqlmodel import SQLModel, Field, Column, Relationship
from pydantic import BaseModel
from sqlalchemy import Boolean, text, TIMESTAMP
from datetime import datetime
from .user_models import UserRead


class PostBase(SQLModel):
    title: str
    content: str
    published: bool = True

    
    
class Post(PostBase, table=True):
    __tablename__ = "posts" #type: ignore

    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="users.id", nullable=False)
    owner: "User" = Relationship(back_populates="posts") #type: ignore

    created_at: datetime | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
        )
    )

    updated_at: datetime | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=True,
            server_default=None,
            onupdate=text("now()")
        ),
        default=None
    )

    #Type hinting with a string to avoid circular import
   
    
class PostRead(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserRead

class PostOut(BaseModel):
    Post: PostRead
    votes: int
    

class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None

    



    #model_config = ConfigDict(table_name="posts")
