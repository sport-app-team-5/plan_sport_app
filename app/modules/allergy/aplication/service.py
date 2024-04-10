from typing import List
from sqlalchemy.orm import Session

from app.modules.allergy.aplication.dto import AllergyDTO, AllergySportManResponseDTO, AllergySportManRequestDTO
from app.modules.allergy.domain.repository import AllergyRepository, AllergySportManRepository
from app.modules.allergy.infrastructure.factories import RepositoryFactory

class AllergiesService:
    def __init__(self):
        self._repository_factory = RepositoryFactory()

    def get_allergies(self, db: Session) -> List[AllergyDTO]:
        repository = self._repository_factory.create_object(AllergyRepository)
        return repository.get_all(db)
    
class AllergiesSportsMenService:
    def __init__(self):
        self._repository_factory = RepositoryFactory()

    def get_allergies(self, db: Session) -> List[AllergySportManResponseDTO]:
        repository = self._repository_factory.create_object(AllergySportManRepository)
        return repository.get_all(db)
    
    def update_allergy(self, id: int, allergy_data: AllergySportManRequestDTO, db: Session) -> AllergySportManResponseDTO:
        repository = self._repository_factory.create_object(AllergySportManRepository)
        return repository.update(id, allergy_data, db)

    def create_allergy(self, allergy_data: AllergySportManRequestDTO, db: Session) -> AllergySportManResponseDTO:
        repository = self._repository_factory.create_object(AllergySportManRepository)
        return repository.create(allergy_data, db)

    def get_allergies_by_sport_man_id(self , sport_man_id: int, db: Session) -> List[AllergySportManResponseDTO]:
        repository = self._repository_factory.create_object(AllergySportManRepository)
        return repository.get_by_id(sport_man_id, db)
    
    def delete_allergy(self, id: int, db: Session) -> AllergySportManResponseDTO:
        repository = self._repository_factory.create_object(AllergySportManRepository)
        return repository.delete(id, db)