import pytest
from pytest_mock import mocker
from unittest.mock import Mock
from app.modules.session.infrastructure.repository import (StartSessionRepositoryPostgres,
                                                          StopSessionRepositoryPostgres,
                                                          RegisterSessionRepositoryPostgres)
from sqlalchemy.orm import Session
from app.modules.session.domain.model import SportsSession, Monitoring
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

@pytest.fixture
def mock_session():
    return SportsSession(id=1, description="Original description")

def test_start_session_repository_update(mocker, mock_session):
    updated_description = "Updated description"
    updated_session = SportsSession(id=1, description=updated_description)
    db = mocker.MagicMock(Session)
    db.query().filter().first.return_value = mock_session  # Mocking the query
    repository = StartSessionRepositoryPostgres()
    updated_result = repository.update(1, updated_session, db)
    assert updated_result.description == updated_description
    db.commit.assert_called_once()  # Ensuring that commit is called

def test_start_session_repository_get_all(mocker):
    repository = StartSessionRepositoryPostgres()

    db = mocker.MagicMock(Session)

    db.query.return_value.all.return_value = [
        SportsSession(id=1, description="Description 1", status="started"),
        SportsSession(id=2, description="Description 2", status="started"),
    ]

    sessions = repository.get_all(db)
    assert len(sessions) == 2
    assert sessions[0].id == 1
    assert sessions[0].description == "Description 1"
    assert sessions[0].status == "started"
    assert sessions[1].id == 2
    assert sessions[1].description == "Description 2"
    assert sessions[1].status == "started"

def test_stop_session_repository_update(mocker):
    repository = StopSessionRepositoryPostgres()

    db = mocker.MagicMock(Session)
    entity = SportsSession(id=1, description="Some description", status='stopped')
    updated_entity = repository.update(1, entity, db)
    assert updated_entity.id == 1
    assert updated_entity.description == "Some description"
    assert updated_entity.status == "stopped"
    db.query.assert_called_once()
    db.commit.assert_called_once()

def test_register_session_repository_create(mocker):
    repository = RegisterSessionRepositoryPostgres()
    db = mocker.MagicMock(Session)
    entity = Monitoring(session_id="some_session_id", indicators_id=1, value=60.0)
    created_entity = repository.create(entity, db)
    assert created_entity.session_id == "some_session_id"
    assert created_entity.indicators_id == 1
    assert created_entity.value == 60.0
    db.commit.assert_called_once()

def test_start_session_repository_create(mocker):
    repository = StartSessionRepositoryPostgres()
    db = mocker.MagicMock(Session)
    entity = SportsSession(id=1, description="Some description")
    db.add.side_effect = SQLAlchemyError

    with pytest.raises(HTTPException) as exc_info:
        repository.create(entity, db)
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_start_session_repository_get_by_id(mocker):
    repository = StartSessionRepositoryPostgres()

    session_object = SportsSession(id=1, description="Description")
    db = mocker.MagicMock()

    db.query(SportsSession).filter.return_value.first.return_value = session_object

    session = repository.get_by_id(1, db)
    assert session.id == 1
    assert session.description == "Description"

@pytest.fixture
def mock_session():
    return SportsSession(id=1, description="Original description")
def test_start_session_repository_update(mocker, mock_session):
    updated_description = "Updated description"
    updated_session = SportsSession(id=1, description=updated_description)
    db = mocker.MagicMock(Session)
    db.query(SportsSession).filter.return_value.first.return_value = mock_session
    repository = StartSessionRepositoryPostgres()
    updated_result = repository.update(1, updated_session, db)
    assert updated_result.description == updated_description
    db.commit.assert_called_once()

def test_stop_session_repository_get_all(mocker):
    repository = StopSessionRepositoryPostgres()

    db = mocker.MagicMock(Session)

    db.query.return_value.all.return_value = [
        SportsSession(id=1, description="Description 1", status="started"),
        SportsSession(id=2, description="Description 2", status="started"),
    ]

    sessions = repository.get_all(db)
    assert len(sessions) == 2
    assert sessions[0].id == 1
    assert sessions[0].description == "Description 1"
    assert sessions[0].status == "started"
    assert sessions[1].id == 2
    assert sessions[1].description == "Description 2"
    assert sessions[1].status == "started"

