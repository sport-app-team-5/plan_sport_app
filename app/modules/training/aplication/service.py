from typing import List
from sqlalchemy.orm import Session
from app.modules.sport_man.aplication.service import SportsManService
from app.modules.training.aplication.dto import TrainingDTO, TrainingUpdateDTO, TrainingResponseDTO, \
    TrainingPlanResponseDTO
from app.modules.training.domain.repository import TrainingRepository
from app.modules.training.infrastructure.factories import RepositoryFactory


class TrainingService:
    def __init__(self):
        self._repository_factory = RepositoryFactory()

    def get_training(self, is_inside_house: bool, db: Session) -> List[TrainingDTO]:
        repository = self._repository_factory.create_object(TrainingRepository)
        return repository.get_all(is_inside_house, db)

    def get_training_by_id(self, user_id: int, db: Session) -> TrainingDTO:
        repository = self._repository_factory.create_object(TrainingRepository)
        return repository.get_by_id(user_id, db)

    def create_training(self, training_data: TrainingDTO, user_id: int, db: Session) -> TrainingDTO:
        sports_man_service = SportsManService()
        sport_man = sports_man_service.get_sportsmen_by_id(user_id, db)
        if sport_man:
            training_data.sportsman_id = sport_man.id
            repository = self._repository_factory.create_object(TrainingRepository)
            return repository.create(training_data, db)

    def update_training(self, training_id: int, training_data: TrainingUpdateDTO,
                        db: Session) -> TrainingDTO:
        repository = self._repository_factory.create_object(TrainingRepository)
        return repository.update(training_id, training_data, db)

    def get_trainings_by_sportsman_id(self, user_id: int, db: Session) -> List[TrainingResponseDTO]:
        sportsman_service = SportsManService()
        sportsman = sportsman_service.get_sportsmen_by_id(user_id, db)
        if sportsman:
            repository = self._repository_factory.create_object(TrainingRepository)
            return repository.get_by_sportsman_id(sportsman.id, db)

    def get_training_plan_by_sportsman_id(self, user_id: int, db: Session) -> List[TrainingPlanResponseDTO]:
        sportsman_service = SportsManService()
        sportsman = sportsman_service.get_sportsmen_by_id(user_id, db)
        if sportsman:
            repository = self._repository_factory.create_object(TrainingRepository)
            return repository.get_plan_by_sportsman_id(sportsman.id, db)
