from fastapi import Response
import pytest
from app.modules.allergy.domain.entities import Allergy

@pytest.fixture
def allergy_seeders(db) -> None:
    db.add(Allergy(name="Lactose", description="Allergy to lactose"))
    db.add(Allergy(name="Gluten", description="Allergy to gluten"))
    db.commit()


class TestAllergyRouter:
    def test_get_allergies(self, client, headers, allergy_seeders):
        response = get(client, headers)
        assert response.status_code == 200
        assert response.json() == [
            {"id": 1, "name": "Lactose", "description": "Allergy to lactose"},
            {"id": 2, "name": "Gluten", "description": "Allergy to gluten"}
        ]

def get(client, headers) -> Response:
    result = client.get("/api/v1/allergies", headers=headers)
    return result