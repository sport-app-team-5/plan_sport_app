from dataclasses import dataclass
from app.modules.injury.domain.repository import InjuryRepository
from app.modules.injury.infrastructure.exceptions import ImplementationNotExistForFabricTypeException
from app.modules.injury.infrastructure.repository import InjuryRepositoryPostgres
from app.seedwork.domain.factories import Factory
from app.seedwork.domain.repositories import Repository

@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj_type) -> Repository:
        if obj_type == InjuryRepository:
            return InjuryRepositoryPostgres()
        else:
            raise ImplementationNotExistForFabricTypeException()
