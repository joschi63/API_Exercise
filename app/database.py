from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

sqlite_file_name = "database.db"

#sqlite_url = f"postgres://<username>:<password>@<ip-address/hostname>/<database_name>"

sqlite_url = f"postgresql://postgres:13579@localhost/postgres"

# only for sqlite connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url)

def get_ssession():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_ssession)]