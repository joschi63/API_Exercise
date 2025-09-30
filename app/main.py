from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
import time

from sqlmodel import select
from .database import create_db_and_tables, SessionDep
from .models import PostBase, Post, PostCreate, PostUpdate, PostRead


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts", response_model=list[PostRead])
def get_posts(session: SessionDep):
    posts = session.exec(select(Post)).all()

    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostRead)
def create_post(post: PostCreate, session: SessionDep):
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)

    return db_post


@app.get("/posts/{id}", response_model=PostRead)
def get_post(id: int, session: SessionDep):
    post = session.get(Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: SessionDep):
    post = session.get(Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    session.delete(post)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def update_post(id: int, post: PostUpdate, session: SessionDep):
    db_post = session.get(Post, id)

    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    db_post.sqlmodel_update(post.model_dump(exclude_unset=True))
    session.add(db_post)
    session.commit()
    session.refresh(db_post)

    return db_post