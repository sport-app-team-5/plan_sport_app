from typing import List
from sqlalchemy.orm import Session
from app.modules.sport_man.domain.entities import Subscription
def suscriptions_seed(db: Session):
    
    suscriptions_to_create = [
        Subscription(type="Basic", description="Plan básico de entrenamiento"),
        Subscription(type="Intermediate", description="Plan intermedio de entrenamiento"),
        Subscription(type="Premiun", description="Plan avanzado de entrenamiento"),
    ]
    create_or_update(db, suscriptions_to_create)
    db.commit()


def create_or_update(db: Session, suscriptions: List[Subscription]):
    for suscription_object in suscriptions:
        suscription = db.query(Subscription).filter_by(type=suscription_object.type).first()
        if suscription:
            suscription.description = suscription_object.description
            suscription.type = suscription_object.type           
        else:
            db.add(suscription_object)