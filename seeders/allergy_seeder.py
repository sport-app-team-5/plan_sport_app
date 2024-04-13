from typing import List
from sqlalchemy.orm import Session
from app.modules.allergy.domain.entities import Allergy


def allergies_seed(db: Session):
    allergies_to_create = [
        Allergy(name="Lactose", description="Allergy to lactose"),
        Allergy(name="Gluten", description="Allergy to gluten"),
        Allergy(name="Peanuts", description="Allergy to peanuts"),
        Allergy(name="Shellfish", description="Allergy to shellfish"),
        Allergy(name="Soy", description="Allergy to soy"),
        Allergy(name="Eggs", description="Allergy to eggs"),
        Allergy(name="Fish", description="Allergy to fish"),
        Allergy(name="Tree nuts", description="Allergy to tree nuts"),
        Allergy(name="Wheat", description="Allergy to wheat"),
        Allergy(name="Sesame", description="Allergy to sesame")
    ]
    create_or_update(db, allergies_to_create)
    db.commit()


def create_or_update(db: Session, allergies: List[Allergy]):
    for allergy in allergies:
        allergy_db = db.query(Allergy).filter_by(name=allergy.name).first()

        if allergy_db:
            allergy_db.description = allergy.description
            allergy_db.name = allergy.name
        else:
            db.add(allergy)
