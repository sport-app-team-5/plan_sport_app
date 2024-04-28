from typing import List
from sqlalchemy.orm import Session

from app.modules.training.domain.entities import Training


def training_seed(db: Session):
    trainings_to_create = [
        Training(name="Levantamento de peso", description="Treino de força", duration=60, sport=1, intensity="Alta"),
        Training(name="Yoga", description="Resistencia", duration=30, sport=2, intensity="Baja"),
        Training(name="Vuelta a la plaza mayor", description="Aeróbico", duration=45, sport=1, intensity="Media"),
    ]
    create_or_update(db, trainings_to_create)
    db.commit()


def create_or_update(db: Session, trainings: List[Training]):
    for training in trainings:
        indicator_db = db.query(Training).filter_by(name=training.name).first()

        if indicator_db:
            indicator_db.name = training.name
        else:
            db.add(training)