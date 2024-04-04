from sqlalchemy.orm import Session
from . import permission_roles_seed


def all_seeders(db: Session):
    permission_roles_seed(db)

