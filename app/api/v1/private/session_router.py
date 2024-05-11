from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.auth.domain.service import AuthService
from app.modules.auth.domain.enums.permission_enum import PermissionEnum
from app.modules.session.aplication.schemas import StartSportsSessionRequestModel
from app.modules.session.aplication.schemas.session_schema import RegisterSportsSessionModel, \
    StopSportsSessionRequestModel
from app.modules.session.aplication.service import SessionService
from app.seedwork.presentation.jwt import get_current_user_id, oauth2_scheme

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
async def stop(model: StopSportsSessionRequestModel, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    session = SessionService().stop(user_id, model, db)
    return session


@session_router.post("/register", response_model=RegisterSportsSessionModel,
                     dependencies=[Security(authorized, scopes=[PermissionEnum.MANAGE_SESSION.code])])
async def register(model: RegisterSportsSessionModel, db: Session = Depends(get_db)):
    session = SessionService().register(model, db)
    return session
