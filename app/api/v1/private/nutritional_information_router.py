from typing import List
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.allergy.aplication.dto import AllergySportManResponseDTO, NutritionalInformationRequestDTO
from app.modules.allergy.aplication.service import AllergiesSportsMenService, NutritionalInformationService
from app.modules.auth.domain.enums.permission_enum import PermissionEnum
from app.modules.auth.domain.service import AuthService
from app.seedwork.presentation.jwt import get_current_user_id, oauth2_scheme

auth_service = AuthService()
authorized = auth_service.authorized
nutritional_information_router = APIRouter(
    prefix='/nutritional_information',
    tags=["Nutritional Information"],
    dependencies=[Depends(oauth2_scheme)]
)


@nutritional_information_router.get("/{sport_man_id}", response_model=List[AllergySportManResponseDTO],
                     dependencies=[Security(authorized, scopes=[PermissionEnum.READ_ALLERGY_SPORTMAN.code])])
def get_allergies_by_sport_man_id(sport_man_id: int, db: Session = Depends(get_db)):
    service = AllergiesSportsMenService()
    return service.get_allergies_by_sport_man_id(sport_man_id, db)

@nutritional_information_router.post("/{sport_man_id}", 
                     dependencies=[Security(authorized, scopes=[PermissionEnum.CREATE_NUTRITIONAL_INFORMATION.code])])
def create_nutritional_information(user_id: int = Depends(get_current_user_id), 
                                   nutritional_information: NutritionalInformationRequestDTO = any, 
                                   db: Session = Depends(get_db)):
    service = NutritionalInformationService()
    return service.create_nutritional_information(user_id, nutritional_information, db)

@nutritional_information_router.get("",  
                                    dependencies=[Security(authorized, scopes=[PermissionEnum.READ_USER.code])])                                    
def get_nutritional_information(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    service = NutritionalInformationService()
    return service.get_nutritional_information(user_id, db)