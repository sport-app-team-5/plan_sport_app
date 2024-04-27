from fastapi import Response
import pytest

from app.modules.training.domain.entities import Training


@pytest.fixture
def training_seeders(db) -> None:
    db.add(Training(name="Levantamento de peso", description="Treino de força", duration=60, sport=1, intensity="Alta"))
    db.commit()


training_data = {
    "name": "Example Training",
    "description": "This is an example training",
    "sport": "Atletismo",
    "intensity": "Alta",
    "duration": 60
  }


class TesttrainingRouter:

    def test_create_training(self, client, headers):
        response = create_training(client, headers, training_data)
        assert response.status_code == 201
        assert response.json()["id"] == 1
        
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
        assert response.json()["sport"] ==  'Ciclismo'

    def test_get_training_by_invalid_id(self, client):
        response = client.get("/api/v1/auth/trainings/99999")
        assert response.status_code == 401

    def test_update_training_with_invalid_id(self, client):
        response = client.put("/api/v1/auth/trainings/99999", json=training_data)
        assert response.status_code == 401


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
