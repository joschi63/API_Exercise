from ..database import engine, SessionDep
from sqlmodel import SQLModel, Field, Column
from pydantic import ConfigDict, EmailStr
from sqlalchemy import Boolean, text, TIMESTAMP


class UserBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    password: str = Field(nullable=False)

class User(UserBase, table=True):
    email: str = Field(nullable=False, unique=True)
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

class UserCreate(UserBase):
    email: EmailStr = Field(nullable=False, unique=True)