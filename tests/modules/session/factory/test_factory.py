from app.modules.session.infrastructure.repository import (StartSessionRepositoryPostgres,
                                                          StopSessionRepositoryPostgres,
                                                          RegisterSessionRepositoryPostgres)
from app.modules.session.domain.repository import (RegisterSessionRepository,
                                                    StartSessionRepository,
                                                    StopSessionRepository)

from app.modules.session.infrastructure.factories import RepositoryFactory


def test_create_object_start_session_repository():
    factory = RepositoryFactory()
    repo = factory.create_object(StartSessionRepository)
    assert isinstance(repo, StartSessionRepositoryPostgres)


def test_create_object_stop_session_repository():
    factory = RepositoryFactory()
    repo = factory.create_object(StopSessionRepository)
    assert isinstance(repo, StopSessionRepositoryPostgres)


def test_create_object_register_session_repository():
    factory = RepositoryFactory()
    repo = factory.create_object(RegisterSessionRepository)
    assert isinstance(repo, RegisterSessionRepositoryPostgres)


