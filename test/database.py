import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

from alembic import command

from app.config import settings
from app.main import app
from app.database import get_session, create_db_and_tables, drop_db_and_tables


#creating and connecting to test database
testing_postgres_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(testing_postgres_url)

@pytest.fixture(scope="function") #scope module means this fixture is created once per module, standard is function (once per test function)
def session():
    print("my ficture ran")
    drop_db_and_tables(engine=engine) #make it possible to watch tables when errors occur
    create_db_and_tables(engine=engine)

    with Session(engine) as session:
        yield session


email = "user3@gmail.com"
password = "password123"

@pytest.fixture(scope="function")
def client(session):
    #run code before run tests
    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session # override the get_session dependency in the tests to use the testing database
    
    yield TestClient(app)

    #run code after tests are done
    