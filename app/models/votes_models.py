#from ..database import engine, SessionDep
from sqlmodel import SQLModel, Field, Column, Relationship
from pydantic import ConfigDict, EmailStr, BaseModel
from sqlalchemy import Boolean, text, TIMESTAMP
from datetime import datetime
from pydantic.types import conint

class VoteBase(SQLModel):
    post_id: int = Field(foreign_key="posts.id", primary_key=True, nullable=False, ondelete="CASCADE")
    user_id: int = Field(foreign_key="users.id", primary_key=True, nullable=False, ondelete="CASCADE")

class Vote(VoteBase, table=True):
    __tablename__ = "votes" #type: ignore

class VoteCreate(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)  #type: ignore