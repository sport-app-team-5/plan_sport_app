from dataclasses import dataclass
from app.modules.allergy.infrastructure.allergy_repository import AllergyRepositoryPostgres
from app.modules.allergy.infrastructure.allergy_sport_man_repository import AllergySportManRepositoryPostgres
from app.seedwork.domain.factories import Factory
from app.seedwork.domain.repositories import Repository
from .exceptions import ImplementationNotExistForFabricTypeException
from ..domain.repository import AllergyRepository, AllergySportManRepository

@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj_type) -> Repository:
        if obj_type == AllergyRepository:
            return AllergyRepositoryPostgres()
        if obj_type == AllergySportManRepository:
            return AllergySportManRepositoryPostgres()
        else:
            raise ImplementationNotExistForFabricTypeException()
