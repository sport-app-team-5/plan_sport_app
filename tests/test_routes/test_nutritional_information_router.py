from fastapi import Response
import pytest
from app.modules.allergy.domain.entities import Allergy, AllergySportMan
from app.modules.sport_man.domain.entities import SportsMan

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
def allergy_sport_man_seeders(db) -> None:
    db.add(AllergySportMan(sportsman_id=1, allergy_id=1))
    db.commit()


class TestNutritionalInformationRouter:
    def test_create_nutritional_information(self, client, headers, sport_man_seeders, allergy_seeders):
        nutritional_information_data = {
            "allergies": [1, 2],
            "food_preference": "VEGAN"
        }
        response = create_nutritional_information(client, headers, 1, nutritional_information_data)
        assert response.status_code == 200
        assert response.json()["allergies"] == [1, 2]
        assert response.json()["food_preference"] == "VEGAN"

    def test_create_nutritional_information_with_invalid_sport_man_id(self, client, headers, allergy_seeders):
        nutritional_information_data = {
            "allergies": [1, 2],
            "food_preference": "VEGAN"
        }
        response = create_nutritional_information(client, headers, 99999, nutritional_information_data)
        assert response.status_code == 404

    def test_get_nutritional_information_by_sport_man_id(self, client, headers, sport_man_seeders, allergy_seeders, allergy_sport_man_seeders):
        response = get_nutritional_information_by_sport_man_id(client, 1, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for item in data:
            assert "sportsman_id" in item

    def test_get_nutritional_information_by_invalid_sport_man_id(self, client, headers):
        response = client.get("/api/v1/auth/nutritional_information/99999", headers=headers)
        assert response.status_code == 404

def create_nutritional_information(client, headers, sport_man_id, nutritional_information_data) -> Response:
    result = client.post(f"/api/v1/auth/nutritional_information/{sport_man_id}", headers=headers, json=nutritional_information_data)
    return result

def get_nutritional_information_by_sport_man_id(client, sport_man_id, headers) -> Response:
    result = client.get(f"/api/v1/auth/nutritional_information/{sport_man_id}", headers=headers)
    return result