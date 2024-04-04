# from fastapi.security import SecurityScopes
# import pytest
# from unittest.mock import MagicMock
# from fastapi import HTTPException, status

# from app.modules.auth.domain.service import AuthService


# @pytest.fixture
# def auth_service():
#     return AuthService()

# def test_authorized_with_enough_permissions(auth_service):
#     token = "dummy_token_with_scopes"
#     token_mock = MagicMock(return_value={"scopes": []})
    
#     auth_service.authorized(SecurityScopes(scopes=[]), token_mock)
    

# def test_authorized_with_not_enough_permissions(auth_service):
#     token = "dummy_token_without_required_scopes"
#     token_mock = MagicMock(return_value={"scopes": ["read"]})
    
#     with pytest.raises(HTTPException) as exc_info:
#         auth_service.authorized(SecurityScopes(scopes=["read", "write"]), token_mock)
    
#     assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
#     assert exc_info.value.detail == "Not enough permissions"