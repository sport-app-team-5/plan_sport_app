from dataclasses import dataclass
from app.seedwork.domain.exceptions import FactoryException
from app.seedwork.domain.factories import Factory
from app.seedwork.domain.repositories import Repository
from .repository import RegisterSessionRepositoryPostgres, StartSessionRepositoryPostgres, StopSessionRepositoryPostgres
from ..domain.repository import RegisterSessionRepository, StartSessionRepository, StopSessionRepository


@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj: type) -> Repository:
        if obj == StartSessionRepository:
            return StartSessionRepositoryPostgres()
        if obj == StopSessionRepository:
            return StopSessionRepositoryPostgres()
        if obj == RegisterSessionRepository:
            return RegisterSessionRepositoryPostgres()
        else:
            raise FactoryException

