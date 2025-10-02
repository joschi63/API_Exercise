from fastapi import FastAPI

from .routers import post, user, auth

from .database import create_db_and_tables


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


