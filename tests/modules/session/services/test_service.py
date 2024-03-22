from app.modules.session.aplication.service import SessionService
from unittest.mock import MagicMock
from app.modules.session.aplication.schemas.session_schema import (StartSportsSessionRequestModel,
                                                                   StopSportsSessionRequestModel,
                                                                   RegisterSportsSessionModel)

class MockRepositoryFactory:
    def create_object(self, repository):
        return MagicMock()

class MockSession:
    pass

def test_start():
    service = SessionService()
    service._repository_factory = MockRepositoryFactory()

    model = StartSportsSessionRequestModel(description="Some description")
    db = MockSession()

    assert service.start(model, db) is not None

def test_stop():
    service = SessionService()
    service._repository_factory = MockRepositoryFactory()

    model = StopSportsSessionRequestModel(id="some_id")
    db = MockSession()

    assert service.stop(model, db) is not None

def test_register():
    service = SessionService()
    service._repository_factory = MockRepositoryFactory()

    model = RegisterSportsSessionModel(session_id="some_session_id", indicators_id=1, value=60.0)
    db = MockSession()

    assert service.register(model, db) is not None
