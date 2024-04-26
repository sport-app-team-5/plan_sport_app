from typing import List
from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.auth.domain.enums.permission_enum import PermissionEnum
from app.modules.auth.domain.service import AuthService
from app.modules.training.aplication.dto import TrainingDTO, TrainingUpdateDTO
from app.modules.training.aplication.service import TrainingService
from app.seedwork.presentation.jwt import oauth2_scheme

auth_service = AuthService()
authorized = auth_service.authorized
training_router = APIRouter(
    prefix='/trainings',
    tags=["Trainings"],
    dependencies=[Depends(oauth2_scheme)]
)


@training_router.get("", response_model=List[TrainingDTO],
                     dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
def get_training(db: Session = Depends(get_db)):
    service = TrainingService()
    return service.get_training(db)


@training_router.get("/{id}", response_model=TrainingDTO,
                     dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
def get_training_by_id(id: int, db: Session = Depends(get_db)):
    service = TrainingService()
    training = service.get_training_by_id(id, db)
    return training


@training_router.put("/{id}", response_model=TrainingDTO, status_code=status.HTTP_201_CREATED,
                     dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
def update_training(id: int, training_data: TrainingUpdateDTO, db: Session = Depends(get_db)):
    service = TrainingService()
    return service.update_training(id, training_data, db)


@training_router.post("", response_model=TrainingDTO, status_code=status.HTTP_201_CREATED,
                     dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
def create_training(training_data: TrainingDTO, db: Session = Depends(get_db)):
    service = TrainingService()
    return service.create_training(training_data, db)