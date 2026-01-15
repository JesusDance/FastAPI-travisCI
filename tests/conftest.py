import pytest

from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel

from app.main import app
from app.db import get_session
from app.config import TestingConfig
from app.models import User, Expense
from app.security import hash_password

settings = TestingConfig()

test_engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

def override_get_session():
    with Session(test_engine) as session:
        yield session


@pytest.fixture(scope="module")
def create_test_db():
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        default_user = User(username="Mary", password=hash_password("some_password"))
        second_user = User(username="John", password=hash_password("12345"))

        session.add_all([default_user, second_user])
        session.commit()

        expense1 = Expense(title="some_title1", amount=100, user_id=default_user.id)
        expense2 = Expense(title="some_title2", amount=200, user_id=default_user.id)
        expense3 = Expense(title="some_title3", amount=300, user_id=default_user.id)

        session.add_all([expense1, expense2, expense3])
        session.commit()

    yield
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(scope="module")
def test_client(create_test_db):
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def default_user_token(test_client):
    response = test_client.post(
        "/users/login/",
        json={
            "username": "Mary",
            "password": "some_password"
        }
    )
    json_response = response.json()
    yield json_response["access_token"]


@pytest.fixture(scope="module")
def second_user_token(test_client):
    response = test_client.post(
        "/users/login/",
        json={
            "username": "John",
            "password": "12345"
        }
    )
    json_response = response.json()
    yield json_response["access_token"]
