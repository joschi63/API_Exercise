from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
import time

from sqlmodel import select
from .database import create_db_and_tables, SessionDep
from .models import Post


app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]

while True:
    try: 
        conn = psycopg.connect("host=localhost port=5432 dbname=postgres user=postgres password=13579")
        cur = conn.cursor() 
                
        print("successfully connected to the database")
        break
    except Exception as error:
        print("unable to connect to the database")
        print("Error details:", error)
        break
            


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 
        
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sql")
def test_sql(session: SessionDep):
    datas = session.exec(select(Post)).all()

    return {"status": datas}

@app.get("/posts")
def get_posts(session: SessionDep):
    posts = session.exec(select(Post)).all()

    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, session: SessionDep):
    session.add(post)
    session.commit()
    session.refresh(post)
    return {"data": post}


@app.get("/posts/{id}")
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

@app.put("/posts/{id}")
def update_post(id: int, post: Post, session: SessionDep):
    db_post = session.get(Post, id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    db_post.sqlmodel_update(post.model_dump(exclude_unset=True))
    session.add(db_post)
    session.commit()
    session.refresh(db_post)

    return "True"