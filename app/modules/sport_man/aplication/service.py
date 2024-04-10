from typing import List
from sqlalchemy.orm import Session
from app.modules.allergy.aplication.dto import AllergyDTO
from app.modules.allergy.domain.repository import AllergyRepository
from app.modules.sport_man.aplication.dto import SportsManRequestDTO, SportsManResponseDTO
from app.modules.sport_man.domain.repository import UserRepository
from app.modules.sport_man.infrastructure.factories import RepositoryFactory


class SportsManService:
    def __init__(self):
        self._repository_factory = RepositoryFactory()

    def get_sportsman(self, db: Session) -> List[SportsManResponseDTO]:
        repository = self._repository_factory.create_object(UserRepository)
        return repository.get_all(db)

    def get_sportsmen_by_id(self, user_id: int, db: Session) -> SportsManResponseDTO:
        repository = self._repository_factory.create_object(UserRepository)
        return repository.get_by_id(user_id, db)

    def create_sportsmen(self, sportsman_data: SportsManRequestDTO, db: Session) -> SportsManResponseDTO:
        repository = self._repository_factory.create_object(UserRepository)
        return repository.create(sportsman_data, db)

    def update_sportsmen(self, sportsman_id: int, sportsman_data: SportsManRequestDTO, db: Session) -> SportsManResponseDTO:
        repository = self._repository_factory.create_object(UserRepository)
        return repository.update(sportsman_id, sportsman_data, db)

class AllergiesSportManService:
    def __init__(self):
        self._repository_factory = RepositoryFactory()

    def get_allergies(self, db: Session) -> List[AllergyDTO]:
        repository = self._repository_factory.create_object(AllergyRepository)
        return repository.get_all(db)