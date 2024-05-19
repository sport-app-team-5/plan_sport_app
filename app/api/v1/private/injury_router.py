from typing import List
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.auth.domain.enums.permission_enum import PermissionEnum
from app.modules.auth.domain.service import AuthService
from app.modules.injury.aplication.dto import InjuryResponseDTO
from app.modules.injury.aplication.service import InjuryService
from app.seedwork.presentation.jwt import oauth2_scheme, get_current_user_id

auth_service = AuthService()
authorized = auth_service.authorized
injury_router = APIRouter(
    prefix='/injuries',
    tags=["Injuries"],
    dependencies=[Depends(oauth2_scheme)]
)


@injury_router.get("/sportsman", response_model=InjuryResponseDTO,
                   dependencies=[Security(authorized, scopes=[PermissionEnum.READ_USER.code])])
def get_injuries_by_sportsman_id(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    injurie_service = InjuryService()
    injurie = injurie_service.get_injuries_by_sportsman_id(user_id, db)
    return injurie
