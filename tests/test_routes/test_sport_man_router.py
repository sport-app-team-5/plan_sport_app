from fastapi import Response
import pytest
from app.modules.allergy.domain.entities import Allergy
from app.modules.sport_man.domain.entities import SportsMan, Injuries
from unittest.mock import patch
from app.modules.sport_man.aplication.dto import SportManRequestProfileSportDTO
# from app.api.v1.private.sport_men_router import  update_sportman_profile_information

@pytest.fixture
def sport_man_seeders(db) -> None:
    db.add(SportsMan(user_id=1))
    db.commit()


@pytest.fixture
def allergy_seeders(db) -> None:
    db.add(Allergy(name="Lactose", description="Allergy to lactose"))
    db.add(Allergy(name="Gluten", description="Allergy to gluten"))
    db.commit()
    
@pytest.fixture
def injuries_seeders(db) -> None:
    db.add(Injuries(name="Lesion de pie", description="Lesion de pie", severity=1))
    db.add(Injuries(name="Lesion de muñeca", description="Lesion de muñeca",severity=2))
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
sportsman_data_profile_information = {  
    "height": 10,
    "weight": 10,
    "id": 1,
    "injuries": [
        1,
        2
    ],
    "sport_preference": "CYCLING"
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
        response = get_sportsman_by_user_id(client, 1, headers=headers)
        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_update_sportsman(self, client, sport_man_seeders, headers):
        updated_data = sportsman_data.copy()
        updated_data["height"] = 185
        response = update_sportsman(client, headers, 1, updated_data)
        assert response.status_code == 201
        assert response.json()["height"] == 185

    def test_get_sportsman_by_invalid_id(self, client):
        response = client.get("/api/v1/auth/sport_men/99999")
        assert response.status_code == 404

    def test_update_sportsman_with_invalid_id(self, client):
        response = client.put("/api/v1/auth/sport_men/99999", json=sportsman_data)
        assert response.status_code == 404

    def test_update_sportman_profile_information(self, client, headers,injuries_seeders, sport_man_seeders):
        data = {
            "id": 1,
            "height": 180,
            "weight": 75,
            "birth_year": 1990,
            "injuries": [1, 2],
            "sport_preference": "ATHLETICS"
        }    
        result = update_sportman_profile_information(client, headers, 1, data)
        assert result.status_code == 200
        

def create_sportsman(client, headers, sportsman_data) -> Response:
    result = client.post("/api/v1/sports_men", headers=headers, json=sportsman_data)
    return result


def get_sportsman(client, headers) -> Response:
    result = client.get("/api/v1/auth/sports_men", headers=headers)
    return result


def get_sportsman_by_user_id(client, user_id, headers) -> Response:
    result = client.get(f"/api/v1/auth/sports_men/{user_id}", headers=headers)
    return result


def update_sportsman(client, headers, sportsman_id, sportsman_data) -> Response:
    result = client.put(f"/api/v1/auth/sports_men/{sportsman_id}", headers=headers, json=sportsman_data)
    return result

def update_sportman_profile_information(client, headers, sportsman_id, sportsman_data_profile_information) -> Response:
    result = client.put(f"/api/v1/auth/sports_men/profile/sport/{sportsman_id}", headers=headers, json=sportsman_data_profile_information)
    return result
