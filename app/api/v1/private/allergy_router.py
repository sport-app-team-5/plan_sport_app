from typing import List
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.allergy.aplication.dto import AllergyDTO
from app.modules.allergy.aplication.service import AllergiesService
from app.modules.auth.domain.enums.permission_enum import PermissionEnum
from app.modules.auth.domain.service import AuthService
from app.seedwork.presentation.jwt import oauth2_scheme

auth_service = AuthService()
authorized = auth_service.authorized
allergy_router = APIRouter(
    prefix='/allergies',
    tags=["Allergies"],
    dependencies=[Depends(oauth2_scheme)]
)

@allergy_router.get("", response_model=List[AllergyDTO],
                     dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_ALLERGY.code])])
def get_allergies(db: Session = Depends(get_db)):
    service = AllergiesService()
    return service.get_allergies(db)