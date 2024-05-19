from typing import List
from sqlalchemy.orm import Session
from app.modules.injury.aplication.dto import InjuryResponseDTO
from app.modules.injury.domain.repository import InjuryRepository
from app.modules.injury.infrastructure.factories import RepositoryFactory
from app.modules.sport_man.aplication.service import SportsManService
from app.seedwork.application.services import Service


class InjuryService(Service):
    def __init__(self):
        self._repository_factory = RepositoryFactory()

    def get_injuries_by_sportsman_id(self, user_id: int, db: Session) -> InjuryResponseDTO:
        sportsman_service = SportsManService()
        sportsman = sportsman_service.get_sportsmen_by_id(user_id, db)
        repository = self._repository_factory.create_object(InjuryRepository)
        return repository.get_by_sportsman_id(sportsman.id, db)
