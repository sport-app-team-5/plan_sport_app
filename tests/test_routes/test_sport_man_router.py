from fastapi import Response
import pytest
from app.modules.allergy.domain.entities import Allergy
from app.modules.injury.domain.entities import SportManInjury, Injury
from app.modules.sport_man.domain.entities import SportProfile, SportsMan, Subscription


@pytest.fixture
def sport_man_seeders(db) -> None:
    db.add(SportProfile(id=1, ftp=1, vo2_max=1, training_time=1.0))
    db.commit()

    db.add(SportsMan(user_id=1, sport_profile_id=1))
    db.commit()


@pytest.fixture
def allergy_seeders(db) -> None:
    db.add(Allergy(name="Lactose", description="Allergy to lactose"))
    db.add(Allergy(name="Gluten", description="Allergy to gluten"))
    db.commit()


@pytest.fixture
def injuries_seeders(db) -> None:
    db.add(Injury(name="Lesion de pie", description="Lesion de pie", severity=1))
    db.add(Injury(name="Lesion de muñeca", description="Lesion de muñeca", severity=2))
    db.commit()


@pytest.fixture
def profile_seeders(db) -> None:
    db.add(SportsMan(user_id=1, sport_preference='Atletismo', exercise_experience='Si',
                     time_dedication_sport='1 a 3 horas', risk='Riesgo Bajo', birth_year=2000,
                     height=100, weight=100))
    db.add(Injury(name="Lesion de pie", description="Lesion de pie", severity=1))
    db.add(Injury(name="Lesion de muñeca", description="Lesion de muñeca", severity=2))
    db.commit()
    db.add(SportManInjury(id_sporman=1, id_injury=1))
    db.commit()


@pytest.fixture
def suscriptions_seeders(db) -> None:
    db.add(Subscription(type="Basic", description="Plan básico de entrenamiento"))
    db.add(Subscription(type="Intermediate", description="Plan intermedio de entrenamiento"))
    db.add(Subscription(type="Premiun", description="Plan avanzado de entrenamiento"))
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
    "birth_year": 1994,
    "height": 10,
    "weight": 10,
    "id": 1,
    "injuries": [
        1,
        2
    ],
    "sport_preference": "Atletismo",
    "exercise_experience": "Si",
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

    def test_update_sportman_profile_information(self, client, headers, injuries_seeders, sport_man_seeders):
        data = {
            "id": 1,
            "height": 180,
            "weight": 75,
            "birth_year": 1990,
            "injuries": [1, 2],
            "sport_preference": "Atletismo",
            "exercise_experience": "Si",
            "time_dedication_sport": "1 a 3 horas"
        }
        result = update_sportman_profile_information(client, headers, 1, data)
        assert result.status_code == 200

    def test_update_sportman_profile_information_risk_low(self, client, headers, injuries_seeders, sport_man_seeders):
        data = {
            "id": 1,
            "height": 175,
            "weight": 70,
            "birth_year": 1964,
            "injuries": [1, 2],
            "sport_preference": "Atletismo",
            "exercise_experience": "Si",
            "time_dedication_sport": "1 a 3 horas"
        }
        result = update_sportman_profile_information(client, headers, 1, data)
        response = get_sportsman_by_user_id(client, 1, headers=headers)
        assert response.status_code == 200
        assert response.json()["risk"] == "Riesgo Bajo"

        assert result.status_code == 200

    def test_update_sportman_profile_information_without_risk(self, client, headers, injuries_seeders, sport_man_seeders):
        data = {
            "id": 1,
            "height": 180,
            "weight": 65,
            "birth_year": 1964,
            "injuries": [1, 2],
            "sport_preference": "Atletismo",
            "exercise_experience": "Si",
            "time_dedication_sport": "1 a 3 horas"
        }
        result = update_sportman_profile_information(client, headers, 1, data)
        response = get_sportsman_by_user_id(client, 1, headers=headers)
        assert response.status_code == 200
        assert response.json()["risk"] == "Sin Riesgo"
        assert result.status_code == 200

    def test_update_sportman_profile_information_risk_medium(self, client, headers, injuries_seeders, sport_man_seeders):
        data = {
            "id": 1,
            "height": 175,
            "weight": 80,
            "birth_year": 1989,
            "injuries": [1, 2],
            "sport_preference": "Atletismo",
            "exercise_experience": "Si",
            "time_dedication_sport": "1 a 3 horas"
        }
        result = update_sportman_profile_information(client, headers, 1, data)
        response = get_sportsman_by_user_id(client, 1, headers=headers)
        assert response.status_code == 200
        assert response.json()["risk"] == "Riesgo Medio"
        assert result.status_code == 200

    def test_update_sportman_profile_information_risk_high(self, client, headers, injuries_seeders, sport_man_seeders):
        data = {
            "id": 1,
            "height": 165,
            "weight": 90,
            "birth_year": 2008,
            "injuries": [1, 2],
            "sport_preference": "Atletismo",
            "exercise_experience": "Si",
            "time_dedication_sport": "1 a 3 horas"
        }
        result = update_sportman_profile_information(client, headers, 1, data)
        response = get_sportsman_by_user_id(client, 1, headers=headers)
        assert response.status_code == 200
        assert response.json()["risk"] == "Riesgo alto"
        assert result.status_code == 200

    

    def test_update_sportman_profile_information_when_missing_attributes(self, client, headers, injuries_seeders,
                                                                         sport_man_seeders):
        data = {
            "id": 1,
            "height": 180,
            "weight": 75,
            "birth_year": 1990,
            "injuries": [1, 2],
            "sport_preference": "ATHLETICS",
            "exercise_experience": "SI"

        }
        result = update_sportman_profile_information(client, headers, 1, data)
        assert result.status_code == 422

    def test_update_sportman_suscription_id(self, client, headers, suscriptions_seeders, profile_seeders):
        result = update_sportman_susciption_id(client, headers, "Basic")
        assert result.status_code == 200

    def test_get_sportsman_profile(self, client, headers, profile_seeders):
        response = get_sportsman_profile(client, headers)
        assert response.status_code == 200

    def test_get_sportsman_profile_indicators(self, client, headers, sport_man_seeders, profile_seeders):
        response = get_sportsman_profile_indicators(client, headers)
        assert response.status_code == 200


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
    result = client.put(f"/api/v1/auth/sports_men/profile/sport/{sportsman_id}", headers=headers,
                        json=sportsman_data_profile_information)
    return result


def get_sportsman_profile(client, headers) -> Response:
    result = client.get("/api/v1/auth/sports_men/profile/sport", headers=headers)
    return result


def update_sportman_susciption_id(client, headers, suscription_type) -> Response:
    result = client.put(f"/api/v1/auth/sports_men/profile/set_suscription/{suscription_type}", headers=headers)
    return result


def get_sportsman_profile_indicators(client, headers) -> Response:
    result = client.get("/api/v1/auth/sports_men/profile/sport/indicators", headers=headers)
    return result
