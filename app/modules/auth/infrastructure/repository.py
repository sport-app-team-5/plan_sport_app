from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.modules.auth.aplication.dto import TokenResponse
from app.modules.auth.domain.repository import AuthRepository
from app.seedwork.presentation.utils import verify_password
from app.seedwork.presentation.jwt import create_access_token


class AuthRepositoryPostgres(AuthRepository):
    def authenticate(self, form_data: OAuth2PasswordRequestForm, db: Session) -> TokenResponse:
        try:
            access_token = create_access_token(data={
                "sub": "",
                "role": "",
                "scopes": ""
            })
            return TokenResponse(access_token=access_token, token_type="Bearer")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
