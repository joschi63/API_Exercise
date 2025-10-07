from ..database import engine, SessionDep
from sqlmodel import SQLModel, Field, Column, Relationship
from pydantic import ConfigDict, EmailStr, BaseModel
from sqlalchemy import Boolean, text, TIMESTAMP
from datetime import datetime



class UserBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    password: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    

class User(UserBase, table=True):
    __tablename__ = "users" #type: ignore
    created_at: str | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), server_default=text("now()")
        ), default="now()"
    )
    updated_at: str = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=True, server_default=None, onupdate=text("now()")
        ), default=None
    )
    #Type hinting with a string to avoid circular import
    posts: "Post" = Relationship(back_populates="owner") #type: ignore

class UserRead(BaseModel):
    id: int
    email: str
    created_at: datetime

class UserCreate(UserBase):
    email: EmailStr = Field(nullable=False, unique=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

