from fastapi import Response
import pytest
from app.main import app
from app.modules.sport_man.domain.entities import SportProfile, SportsMan

@pytest.fixture
def sport_man_seeders(db) -> None:
    db.add(SportsMan(user_id=1))
    db.commit()

sportsman_data = {
    "user_id": 1,
    "birth_year": 1990,
    "food_preference": "VEGAN",
    "training_goal": "TONE",
    "height": 180,
    "weight": 75,
    "body_mass_index": 23.15
}

class TestSportManRouter:

    def test_create_sportsman(self, client, headers):
        response = create_sportsman(client, headers, sportsman_data)
        assert response.status_code == 201
        assert response.json()["user_id"] == sportsman_data["user_id"]

    def test_get_sportsmen(self, client, headers, sport_man_seeders):
        response = get_sportsman(client, headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_sportsman_by_id(self, client, headers, sport_man_seeders):
        response = get_sportsman_by_user_id(client,1, headers=headers)       
        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_update_sportsman(self, client, sport_man_seeders, headers):
        updated_data = sportsman_data.copy()
        updated_data["height"] = 185
        response = update_sportsman(client, headers, 1 , updated_data)
        assert response.status_code == 201
        assert response.json()["height"] == 185


    def test_get_sportsman_by_invalid_id(self, client):
         response = client.get("/sport_men/99999")
         assert response.status_code == 404

    def test_update_sportsman_with_invalid_id(self, client):
         response = client.put("/sport_men/99999", json=sportsman_data)
         assert response.status_code == 404

def create_sportsman(client, headers, sportsman_data) -> Response:
    result = client.post("/api/v1/sport_men", headers=headers, json=sportsman_data)
    return result

def get_sportsman(client, headers) -> Response:
    result = client.get("/api/v1/sport_men", headers=headers)
    return result

def get_sportsman_by_user_id(client, user_id, headers) -> Response:
    result = client.get(f"/api/v1/sport_men/{user_id}", headers=headers)
    return result

def update_sportsman(client, headers, sportsman_id, sportsman_data) -> Response:
    result = client.put(f"/api/v1/sport_men/{sportsman_id}", headers=headers, json=sportsman_data)
    return result