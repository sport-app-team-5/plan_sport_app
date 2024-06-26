from datetime import datetime
from unittest.mock import patch

from fastapi import Response
import pytest
from app.modules.allergy.domain.entities import Allergy, AllergySportMan
from app.modules.session.aplication.service import SessionService
from app.modules.session.domain.model import Monitoring, SportsSession
from app.modules.sport_man.domain.entities import SportsMan
from app.modules.training.domain.entities import Training


@pytest.fixture
def sport_man_seeders(db) -> None:
    db.add(SportsMan(user_id=1, weight=70, food_preference='CARNIVOROUS'))
    db.commit()


@pytest.fixture
def training_plan_seeders(db) -> None:
    db.add(Training(id=1, name="Levantamiento de pesas", description=" desc levantamiento", duration="50",
                    sport="Atletismo", intensity="Alta", created_at=datetime.strptime('2024-05-10', '%Y-%m-%d'),
                    updated_at=datetime.strptime('2024-05-10', '%Y-%m-%d'), sportsman_id=1, is_inside_house=True))
    db.add(Training(id=2, name="Estiramiento", description=" desc Estiramiento", duration="20", sport="Atletismo",
                    intensity="Alta", created_at=datetime.strptime('2024-05-10', '%Y-%m-%d'),
                    updated_at=datetime.strptime('2024-05-10', '%Y-%m-%d'), sportsman_id=1, is_inside_house=True))
    db.commit()
    db.add(SportsSession(id="ABC", time="00:20:25", status="start", sportsman_id=1, training_plan_id=1,
                         created_at=datetime.strptime('2024-05-10', '%Y-%m-%d'),
                         updated_at=datetime.strptime('2024-05-10', '%Y-%m-%d')))
    db.add(SportsSession(id="ABCD", time="00:30:25", status="start", sportsman_id=1, training_plan_id=1,
                         created_at=datetime.strptime('2024-05-10', '%Y-%m-%d'),
                         updated_at=datetime.strptime('2024-05-10', '%Y-%m-%d')))
    db.commit()
    db.add(Monitoring(session_id='ABC', indicators_id=1, value='80',
                      created_at=datetime.strptime('2024-05-10', '%Y-%m-%d'),
                      updated_at=datetime.strptime('2024-05-10', '%Y-%m-%d')))
    db.add(Monitoring(session_id='ABC', indicators_id=1, value='90',
                      created_at=datetime.strptime('2024-05-10', '%Y-%m-%d'),
                      updated_at=datetime.strptime('2024-05-10', '%Y-%m-%d')))
    db.add(Monitoring(session_id='ABC', indicators_id=1, value='100',
                      created_at=datetime.strptime('2024-05-10', '%Y-%m-%d'),
                      updated_at=datetime.strptime('2024-05-10', '%Y-%m-%d')))
    db.add(Monitoring(session_id='ABC', indicators_id=1, value='110',
                      created_at=datetime.strptime('2024-05-10', '%Y-%m-%d'),
                      updated_at=datetime.strptime('2024-05-10', '%Y-%m-%d')))
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


session_stop_data = {
    "id": "ABC",
    "time": "00:20:50"
}

session_start_data = {
    "id": "ABC",
    "training_plan_id": "3"
}

session_register_data = {
    "session_id": "ABC",
    "indicators_id": "1",
    "value": "60.0"
}


class TestSessionRouter:
    def test_start_session(self, client, headers, sport_man_seeders, training_plan_seeders):
        response = start_session(client, headers, session_start_data)
        assert response.status_code == 200

    def test_register_session(self, client, headers, sport_man_seeders, training_plan_seeders):
        response = register_session(client, headers, session_register_data)
        assert response.status_code == 200

    @patch.object(SessionService, 'send_to_pub_sub')
    def test_stop_session(self, mock_send, client, headers, sport_man_seeders, training_plan_seeders):
        mock_send.return_value = True
        response = stop_session(client, headers, session_stop_data)
        assert response.status_code == 200

    def test_sport_information(self, client, headers, sport_man_seeders, training_plan_seeders, allergy_seeders,
                               allergy_sport_man_seeders):
        response = sport_information(client, "ABC", headers)
        assert response.status_code == 200


def start_session(client, headers, session_data, ) -> Response:
    result = client.post("/api/v1/auth/sessions/start", headers=headers, json=session_data)
    return result


def register_session(client, headers, session_data, ) -> Response:
    result = client.post("/api/v1/auth/sessions/register", headers=headers, json=session_data)
    return result


def stop_session(client, headers, session_data, ) -> Response:
    result = client.post("/api/v1/auth/sessions/stop", headers=headers, json=session_data)
    return result


def sport_information(client, id, headers) -> Response:
    result = client.get(f"/api/v1/auth/sessions/session_information/{id}", headers=headers)
    return result
