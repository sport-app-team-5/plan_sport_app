from typing import List
from fastapi import APIRouter, Depends, status, Security
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.auth.domain.service import AuthService
from app.modules.sport_man.aplication.dto import SportsManRequestDTO, SportsManResponseDTO, \
    SportManRequestProfileSportDTO, SportManResponseProfileDTO
from app.modules.sport_man.aplication.service import SportsManService
from app.seedwork.presentation.jwt import oauth2_scheme, get_current_user_id
from app.modules.auth.domain.enums.permission_enum import PermissionEnum

auth_service = AuthService()
authorized = auth_service.authorized
sport_men_router = APIRouter(
    prefix='/sports_men',
    tags=["Sports Men"],
    dependencies=[Depends(oauth2_scheme)]
)


@sport_men_router.get("", response_model=List[SportsManResponseDTO])
def get_sportsmen(db: Session = Depends(get_db)):
    service = SportsManService()
    return service.get_sportsman(db)


@sport_men_router.get("/{sportsman_id}", response_model=SportsManResponseDTO)
def get_sportsman_by_user_id(sportsman_id: int, db: Session = Depends(get_db)):
    service = SportsManService()
    sportsman = service.get_sportsmen_by_id(sportsman_id, db)
    return sportsman


@sport_men_router.put("/{sportsman_id}", response_model=SportsManResponseDTO, status_code=status.HTTP_201_CREATED)
def update_sportsman(sportsman_id: int, sportsman_data: SportsManRequestDTO, db: Session = Depends(get_db)):
    service = SportsManService()
    return service.update_sportsmen(sportsman_id, sportsman_data, db)


@sport_men_router.put("/profile/sport/{user_id}",
                      dependencies=[
                          Security(authorized, scopes=[PermissionEnum.UPDATE_SPORT_MAN_PROFILE_INFORMATION.code])])
def update_sportsman_profile_information(user_id: int, sportsman_profile_information: SportManRequestProfileSportDTO,
                                         db: Session = Depends(get_db)):
    service = SportsManService()
    return service.update_sportsman_profile_information(user_id, sportsman_profile_information, db)


@sport_men_router.get("/profile/sport", response_model=SportManResponseProfileDTO,
                      dependencies=[Security(authorized)])
def get_sportsman_profile_information(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    service = SportsManService()
    return service.get_sportsman_profile(user_id, db)
