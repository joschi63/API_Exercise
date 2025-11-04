from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings

from app.routers import post, user, auth, vote

#from app.database import create_db_and_tables



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Welcome to my API-Server 2!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


