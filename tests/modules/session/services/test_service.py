from app.modules.session.aplication.service import SessionService
from unittest.mock import MagicMock
from app.modules.session.aplication.schemas.session_schema import StartSportsSessionRequestModel
from app.modules.session.aplication.service import SessionService
from unittest.mock import MagicMock
from app.modules.session.aplication.schemas.session_schema import StartSportsSessionResponseModel
import uuid
from app.modules.session.aplication.schemas.session_schema import (StartSportsSessionRequestModel,
                                                                   StopSportsSessionRequestModel,
                                                                   RegisterSportsSessionModel)

class MockRepositoryFactory:
    def create_object(self, repository):
        return MagicMock()

class MockSession:
    ...  


class MockRepositoryFactory:
    def create_object(self, repository):        
        return MagicMock()


def test_start():
    service = SessionService()
    service._repository_factory = MockRepositoryFactory()

    model = StartSportsSessionRequestModel(id="1", training_plan_id=1)
    db = MockSession()

    service.start = MagicMock(return_value=StartSportsSessionResponseModel(id="1", training_plan_id=1))

    assert service.start(model, db, 1) is not None

def test_register():
    service = SessionService()
    service._repository_factory = MockRepositoryFactory()

    model = RegisterSportsSessionModel(session_id="some_session_id", indicators_id=1, value=60.0)
    db = MockSession()

    assert service.register(model, db) is not None
