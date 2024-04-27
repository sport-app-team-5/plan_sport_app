from sqlalchemy.orm import Session
from . import allergies_seed
from . import indicators_seed
from . import injuries_seed
from . import suscriptions_seed

def all_seeders(db: Session):
    allergies_seed(db)
    indicators_seed(db)
    injuries_seed(db)
    suscriptions_seed(db)