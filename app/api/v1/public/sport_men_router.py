from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.sport_man.aplication.dto import SportsManRequestDTO, SportsManResponseDTO
from app.modules.sport_man.aplication.service import SportsManService

sport_men_router = APIRouter(
    prefix='/sport_men',
    tags=["SportMen"]
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


@sport_men_router.post("", response_model=SportsManResponseDTO, status_code=status.HTTP_201_CREATED)
def create_sportsman(sportsman_data: SportsManRequestDTO, db: Session = Depends(get_db)):
    service = SportsManService()
    return service.create_sportsmen(sportsman_data, db)


@sport_men_router.put("/{sportsman_id}", response_model=SportsManResponseDTO, status_code=status.HTTP_201_CREATED)
def update_sportsman(sportsman_id: int, sportsman_data: SportsManRequestDTO, db: Session = Depends(get_db)):
    service = SportsManService()
    return service.update_sportsmen(sportsman_id, sportsman_data, db)
