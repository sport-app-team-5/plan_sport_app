from typing import List
from sqlalchemy.orm import Session
from app.modules.allergy.domain.entities import Allergy
from app.modules.session.domain.model import Indicators


def indicators_seed(db: Session):
    indicators_to_create = [
        Indicators(name="FTP"),
        Indicators(name="VO2MAX"),
    ]
    create_or_update(db, indicators_to_create)
    db.commit()


def create_or_update(db: Session, indicators: List[Indicators]):
    for indicator in indicators:
        indicator_db = db.query(Indicators).filter_by(name=indicator.name).first()

        if indicator_db:
            indicator_db.name = indicator.name
        else:
            db.add(indicator)