from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.auth.domain.service import AuthService
from app.modules.sport_man.aplication.dto import SportsManRequestDTO, SportsManResponseDTO
from app.modules.sport_man.aplication.service import SportsManService

auth_service = AuthService()
authorized = auth_service.authorized
sport_men_router = APIRouter(
    prefix='/sports_men',
    tags=["Sports Men"]
)


@sport_men_router.post("", response_model=SportsManResponseDTO, status_code=status.HTTP_201_CREATED)
def create_sportsman(sportsman_data: SportsManRequestDTO, db: Session = Depends(get_db)):
    service = SportsManService()
    return service.create_sportsmen(sportsman_data, db)
