import pytest
from app.modules.auth.aplication.service import AuthService
from app.modules.auth.infrastructure.exceptions import ImplementationNotExistForFabricTypeException


class NonRepository:
    pass


class TestAuthException:
    def test_factory_auth(self):
        auth_service = AuthService()

        with pytest.raises(ImplementationNotExistForFabricTypeException) as exc_info:
            auth_service.repository_factory.create_object(NonRepository)

        assert 'There is no implementation for the repository with the given type' in str(exc_info.value)
