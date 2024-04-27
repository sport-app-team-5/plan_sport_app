from typing import List
from sqlalchemy.orm import Session
from app.modules.training.aplication.dto import TrainingDTO, TrainingUpdateDTO
from app.modules.training.domain.repository import TrainingRepository
from app.modules.training.infrastructure.factories import RepositoryFactory


class TrainingService:
    def __init__(self):
        self._repository_factory = RepositoryFactory()

    def get_training(self, db: Session) -> List[TrainingDTO]:
        repository = self._repository_factory.create_object(TrainingRepository)
        return repository.get_all(db)

    def get_training_by_id(self, user_id: int, db: Session) -> TrainingDTO:
        repository = self._repository_factory.create_object(TrainingRepository)
        return repository.get_by_id(user_id, db)

    def create_training(self, training_data: TrainingDTO, db: Session) -> TrainingDTO:
        repository = self._repository_factory.create_object(TrainingRepository)
        return repository.create(training_data, db)

    def update_training(self, training_id: int, training_data: TrainingUpdateDTO,
                         db: Session) -> TrainingDTO:
        repository = self._repository_factory.create_object(TrainingRepository)
        return repository.update(training_id, training_data, db)
