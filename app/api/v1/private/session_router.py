from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.allergy.aplication.dto import NutritionalInformationResponseDTO
from app.modules.allergy.aplication.service import NutritionalInformationService
from app.modules.auth.domain.service import AuthService
from app.modules.auth.domain.enums.permission_enum import PermissionEnum
from app.modules.session.aplication.schemas import StartSportsSessionRequestModel
from app.modules.session.aplication.schemas.session_schema import RegisterSportsSessionModel, SportInformationDTO, \
    SportsSessionResponseModel, \
    StopSportsSessionRequestModel
from app.modules.session.aplication.service import SessionService
from app.modules.sport_man.aplication.dto import SportsManResponseDTO
from app.modules.sport_man.aplication.service import SportsManService
from app.modules.training.aplication.dto import TrainingDTO
from app.modules.training.aplication.service import TrainingService
from app.seedwork.presentation.jwt import oauth2_scheme, get_current_user_id

auth_service = AuthService()
authorized = auth_service.authorized
session_router = APIRouter(
    prefix='/sessions',
    tags=["Sessions"],
    dependencies=[Depends(oauth2_scheme)]
)


@session_router.post("/start", response_model=StartSportsSessionRequestModel,
                     dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
async def start(model: StartSportsSessionRequestModel, db: Session = Depends(get_db),
                user_id: int = Depends(get_current_user_id)):
    session = SessionService().start(model, db, user_id)
    return session


@session_router.post("/stop", response_model=StopSportsSessionRequestModel,
                     dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
async def stop(model: StopSportsSessionRequestModel, db: Session = Depends(get_db),
               user_id: int = Depends(get_current_user_id)):
    session = SessionService().stop(user_id, model, db)
    return session


@session_router.post("/register", response_model=RegisterSportsSessionModel,
                     dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
async def register(model: RegisterSportsSessionModel, db: Session = Depends(get_db)):
    session = SessionService().register(model, db)
    return session


@session_router.get("/session_information/{session_id}", response_model=SportInformationDTO,
                    dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
async def get_session_information(session_id: str, user_id: int = Depends(get_current_user_id),
                                  db: Session = Depends(get_db)):
    session_service = SessionService()
    session_sport: SportsSessionResponseModel = session_service.get_by_id(session_id, db)

    service = TrainingService()
    training: TrainingDTO = service.get_training_by_id(session_sport.training_plan_id, db)

    service = SportsManService()
    sport_men: SportsManResponseDTO = service.get_sportsmen_by_id(user_id, db)

    service = NutritionalInformationService()
    nutritional_information: NutritionalInformationResponseDTO = service.get_nutritional_information(user_id, db)

    sport_information = build_sport_information(session_sport.time, training, sport_men, nutritional_information)

    return sport_information


def build_sport_information(time: str, training: TrainingDTO, sport_men: SportsManResponseDTO,
                            nutritional_information: NutritionalInformationResponseDTO):
    allergies_names = [allergy.name for allergy in nutritional_information.allergies]

    duration_parts = time.split(':')
    hours = int(duration_parts[0])
    minutes = int(duration_parts[1])
    seconds = int(duration_parts[2])
    total_minutes = (hours * 60) + minutes + (seconds / 60)

    sport_information = SportInformationDTO(type=sport_men.food_preference, weight=sport_men.weight, time=total_minutes,
                                            intensity=training.intensity, allergies=allergies_names)

    return sport_information
