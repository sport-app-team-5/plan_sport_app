from typing import List
from sqlalchemy.orm import Session
from app.modules.injury.domain.entities import Injury


def injuries_seed(db: Session):
    injuries_to_create = [
        Injury(name="Fractuas miembro superior", description="Fractuas miembro superior",severity=1),
        Injury(name="Fracturas miembro inferiores", description="Fracturas miembro inferiores",severity=1),
        Injury(name="Dolor en miembros superiores", description="Dolor en miembros superiores",severity=1),
        Injury(name="Dolor en miembros inferiores", description="Dolor en miembros inferiores",severity=1),
        Injury(name="Dolor en la espalda", description="Dolor en la espalda",severity=1),
        Injury(name="Quemaduras en la espalda", description="Quemaduras en la espalda",severity=1),
        Injury(name="Ampollas miembros inferiores", description="Ampollas en miembros inferiores",severity=1),
        Injury(name="Ampollas miembros superiores", description="Ampollas en miembros superiores",severity=1),
        Injury(name="Ninguna", description="Ninguna", severity=1)

    ]
    create_or_update(db, injuries_to_create)
    db.commit()


def create_or_update(db: Session, injuries: List[Injury]):
    for injury in injuries:
        injury_db = db.query(Injury).filter_by(name=injury.name).first()

        if injury_db:
            injury_db.description = injury.description
            injury_db.name = injury.name
            injury_db.severity = injury.severity
        else:
            db.add(injury)
