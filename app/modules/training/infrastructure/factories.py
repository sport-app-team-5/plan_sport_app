from dataclasses import dataclass
from app.seedwork.domain.factories import Factory
from app.seedwork.domain.repositories import Repository
from .repository import TrainingRepositoryPostgres
from .exceptions import ImplementationNotExistForFabricTypeException
from ..domain.repository import TrainingRepository

@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj_type) -> Repository:
        if obj_type == TrainingRepository:
            return TrainingRepositoryPostgres()       
        else:
            raise ImplementationNotExistForFabricTypeException()
