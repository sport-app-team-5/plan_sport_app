from typing import List
from sqlalchemy.orm import Session
from app.modules.sport_man.aplication.dto import InjuryRequestDTO,SportsManRequestDTO, SportsManResponseDTO, SportManRequestProfileSportDTO
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
    
    def update_sportman_profile_information(self,  user_id: int,  sportsman_data: SportManRequestProfileSportDTO, db:Session):
        repository = self._repository_factory.create_object(UserRepository)      
        for  injury in sportsman_data.injuries:
                repository.create_injury(injury, user_id, db)
        return repository.update_sport_profile(user_id, sportsman_data, db)
    

    
 