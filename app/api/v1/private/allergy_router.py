from typing import List
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.allergy.aplication.dto import AllergyDTO, AllergySportManResponseDTO, AllergySportManRequestDTO
from app.modules.allergy.aplication.service import AllergiesService, AllergiesSportsMenService
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

@allergy_router.get("/sports_men", response_model=List[AllergySportManResponseDTO],
                     dependencies=[Security(authorized, scopes=[PermissionEnum.READ_ALLERGY_SPORTMAN.code])])
def get_sports_men_allergies(db: Session = Depends(get_db)):
    service = AllergiesSportsMenService()
    return service.get_allergies(db)

@allergy_router.post("/sports_men", response_model=AllergySportManResponseDTO,
                     dependencies=[Security(authorized, scopes=[PermissionEnum.CREATE_ALLERGY_SPORTMAN.code])])
def create_allergy(allergy: AllergySportManRequestDTO, db: Session = Depends(get_db)):
    service = AllergiesSportsMenService()
    return service.create_allergy(allergy, db)

@allergy_router.put("/sports_men/{id}", response_model=AllergySportManResponseDTO,
                     dependencies=[Security(authorized, scopes=[PermissionEnum.UPDATE_ALLERGY_SPORTMAN.code])])
def update_allergy(id: int, allergy: AllergySportManRequestDTO, db: Session = Depends(get_db)):
    service = AllergiesSportsMenService()
    return service.update_allergy(id, allergy, db)

@allergy_router.get("/sports_men/{sport_man_id}", response_model=List[AllergySportManResponseDTO],
                     dependencies=[Security(authorized, scopes=[PermissionEnum.READ_ALLERGY_SPORTMAN.code])])
def get_allergies_by_sport_man_id(sport_man_id: int, db: Session = Depends(get_db)):
    service = AllergiesSportsMenService()
    return service.get_allergies_by_sport_man_id(sport_man_id, db)

@allergy_router.delete("/sports_men/{id}", response_model=AllergySportManResponseDTO,
                     dependencies=[Security(authorized, scopes=[PermissionEnum.DEACTIVATE_ALLERGY_SPORTMAN.code])])
def delete_allergy(id: int, db: Session = Depends(get_db)):
    service = AllergiesSportsMenService()
    return service.delete_allergy(id, db)