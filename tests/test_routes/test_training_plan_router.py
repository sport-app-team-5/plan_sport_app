import uuid
from typing import Any
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from app.config.db import Base, get_db
from app.main import app
from app.modules.auth.domain.service import AuthService
from app.seedwork.presentation.jwt import get_current_user_id

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def __app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    yield app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db() -> Generator[SessionTesting, Any, None]:  # type: ignore
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(__app: FastAPI, db: SessionTesting) -> Generator[TestClient, Any, None]:  # type: ignore
    def __get_test_db():
        yield db

    def __get_current_user_id():
        return 1

    def __authorized():
        pass

    # noinspection PyUnresolvedReferences
    app.dependency_overrides.update(
        {get_db: __get_test_db, AuthService.authorized: __authorized, get_current_user_id: __get_current_user_id})

    with TestClient(__app) as client:
        yield client


@pytest.fixture
def headers() -> dict:
    uuid_token = uuid.uuid4()
    return {"Authorization": f"Bearer {uuid_token}"}


from fastapi import Response
import pytest
from app.modules.sport_man.domain.entities import SportsMan
from app.modules.training.domain.entities import Training


@pytest.fixture
def training_seeders(db) -> None:
    db.add(SportsMan(user_id=1, sport_preference='Atletismo', exercise_experience='Si',
                     time_dedication_sport='1 a 3 horas', risk='Riesgo Bajo'))
    db.add(Training(name="Levantamento de peso", description="Treino de força", duration=60, sport="Atletismo",
                    intensity="Alta", sportsman_id=1))
    db.commit()


training_data = {
    "name": "Example Training",
    "description": "This is an example training",
    "sport": "Atletismo",
    "intensity": "Alta",
    "duration": 60
  }


class TestTrainingRouter:
    def test_create_training(self, client, headers, training_seeders):
        response = create_training(client, headers, training_data)
        assert response.status_code == 201
        assert response.json()["id"] == 2
        
    def test_get_training(self, client, headers, training_seeders):
        response = get_training(client, headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_training_by_id(self, client, headers, training_seeders):
        response = get_training_by_user_id(client, 1, headers=headers)
        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_update_training(self, client, training_seeders, headers):
        updated_data = training_data.copy()
        updated_data["sport"] = 'Ciclismo'
        response = update_training(client, headers, 1, updated_data)
        assert response.status_code == 201
        assert response.json()["sport"] == 'Atletismo'

    def test_get_training_by_invalid_id(self, client):
        response = client.get("/api/v1/auth/trainings/99999")
        assert response.status_code == 401

    def test_update_training_with_invalid_id(self, client):
        response = client.put("/api/v1/auth/trainings/99999", json=training_data)
        assert response.status_code == 401

    def test_get_event_by_sportsman_id(self, client, headers, training_seeders):
        response = get_event_by_sportsman_id(client, headers=headers)
        assert response.status_code == 200
        assert response.json()[0]["id"] == 1


def create_training(client, headers, training_data) -> Response:
    result = client.post("/api/v1/auth/trainings", headers=headers, json=training_data)
    return result


def get_training(client, headers) -> Response:
    result = client.get("/api/v1/auth/trainings", headers=headers)
    return result


def get_training_by_user_id(client, user_id, headers) -> Response:
    result = client.get(f"/api/v1/auth/trainings/{user_id}", headers=headers)
    return result


def update_training(client, headers, id, training_data) -> Response:
    result = client.put(f"/api/v1/auth/trainings/{id}", headers=headers, json=training_data)
    return result


def get_event_by_sportsman_id(client, headers) -> Response:
    trainings = client.get(f"/api/v1/auth/trainings/sportsman", headers=headers)
    return trainings
