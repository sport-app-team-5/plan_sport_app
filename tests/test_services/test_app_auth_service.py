from unittest.mock import MagicMock
from fastapi.security import OAuth2PasswordRequestForm
from pytest import Session
import pytest

from app.modules.auth.aplication.dto import TokenResponse
from app.modules.auth.aplication.service import AuthService
from app.modules.auth.domain.repository import AuthRepository
from app.modules.auth.infrastructure.factories import RepositoryFactory


@pytest.fixture
def auth_service():
    return AuthService()

def test_authenticate_user(auth_service):
    form_data = OAuth2PasswordRequestForm(username="testuser", password="testpassword")
    db_mock = MagicMock(spec=Session)
    repository_mock = MagicMock(spec=AuthRepository)
    token_response = TokenResponse(access_token="test_access_token", token_type="bearer")
    repository_mock.authenticate.return_value = token_response

    repository_factory_mock = MagicMock(spec=RepositoryFactory)
    repository_factory_mock.create_object.return_value = repository_mock
    auth_service._repository_factory = repository_factory_mock
    

    result = auth_service.authenticate_user(form_data, db_mock)

    repository_factory_mock.create_object.assert_called_once_with(AuthRepository)
    repository_mock.authenticate.assert_called_once_with(form_data, db_mock)
    assert result == token_response