from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session
from app.modules.allergy.aplication.dto import AllergyDTO, AllergySportManResponseDTO
from app.modules.allergy.domain.entities import AllergySportMan
from app.seedwork.domain.repositories import Repository


class AllergyRepository(Repository, ABC):
    @abstractmethod
    def get_all(self, db: Session) -> List[AllergyDTO]:
            ...
    
class AllergySportManRepository(Repository, ABC):
    @abstractmethod
    def get_by_id(self, entity_id: int, db: Session) -> List[AllergySportManResponseDTO]:
        ...

    @abstractmethod
    def create(self, entity: AllergySportMan, db: Session) -> AllergySportManResponseDTO:
        ...

    @abstractmethod
    def delete(self, id: int, db: Session) -> AllergySportManResponseDTO:
        ...