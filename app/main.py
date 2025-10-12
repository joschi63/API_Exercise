from fastapi import FastAPI

from .config import settings

from app.routers import post, user, auth, vote

#from app.database import create_db_and_tables



app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


