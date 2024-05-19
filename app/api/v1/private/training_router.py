from typing import List
from fastapi import APIRouter, Depends, Security, status, Query
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.auth.domain.enums.permission_enum import PermissionEnum
from app.modules.auth.domain.service import AuthService
from app.modules.training.aplication.dto import TrainingDTO, TrainingUpdateDTO, TrainingResponseDTO, \
    TrainingPlanResponseDTO
from app.modules.training.aplication.service import TrainingService
from app.seedwork.presentation.jwt import oauth2_scheme, get_current_user_id

auth_service = AuthService()
authorized = auth_service.authorized
training_router = APIRouter(
    prefix='/trainings',
    tags=["Trainings"],
    dependencies=[Depends(oauth2_scheme)]
)


@training_router.get("/plan/sportsman", response_model=List[TrainingPlanResponseDTO],
                     dependencies=[Security(authorized, scopes=[PermissionEnum.READ_SERVICE.code])])
def get_trainings_plan_by_sportsman_id(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    training_service = TrainingService()
    trainings = training_service.get_training_plan_by_sportsman_id(user_id, db)
    return trainings


@training_router.get("/sportsman", response_model=List[TrainingResponseDTO],
                     dependencies=[Security(authorized, scopes=[PermissionEnum.READ_SERVICE.code])])
def get_events_by_sportsman_id(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    training_service = TrainingService()
    trainings = training_service.get_trainings_by_sportsman_id(user_id, db)
    return trainings


@training_router.get("", response_model=List[TrainingDTO],
                     dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
def get_training(is_inside_house: bool = Query(None), db: Session = Depends(get_db)):
    service = TrainingService()
    return service.get_training(is_inside_house, db)


@training_router.get("/{training_id}", response_model=TrainingDTO,
                     dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
def get_training_by_id(training_id: int, db: Session = Depends(get_db)):
    service = TrainingService()
    training = service.get_training_by_id(training_id, db)
    return training


@training_router.put("/{training_id}", response_model=TrainingDTO, status_code=status.HTTP_201_CREATED,
                     dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
def update_training(training_id: int, training_data: TrainingUpdateDTO, db: Session = Depends(get_db)):
    service = TrainingService()
    return service.update_training(training_id, training_data, db)


@training_router.post("", response_model=TrainingDTO, status_code=status.HTTP_201_CREATED,
                      dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
def create_training(training_data: TrainingDTO, user_id: int = Depends(get_current_user_id),
                    db: Session = Depends(get_db)):
    service = TrainingService()
    return service.create_training(training_data, user_id, db)
