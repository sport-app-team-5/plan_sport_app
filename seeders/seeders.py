from sqlalchemy.orm import Session
from . import allergies_seed


def all_seeders(db: Session):
    allergies_seed(db)
