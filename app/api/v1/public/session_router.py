from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.session.aplication.schemas import StartSportsSessionRequestModel
from app.modules.session.aplication.schemas.session_schema import RegisterSportsSessionModel, \
    StopSportsSessionRequestModel
from app.modules.session.aplication.service import SessionService

session_router = APIRouter(
    prefix='/sessions',
    tags=["session"]
)


@session_router.post("/start", response_model=StartSportsSessionRequestModel)
async def start(model: StartSportsSessionRequestModel, db: Session = Depends(get_db)):
    session = SessionService().start(model, db)
    return session


@session_router.post("/stop", response_model=StopSportsSessionRequestModel)
async def stop(model: StopSportsSessionRequestModel, db: Session = Depends(get_db)):
    session = SessionService().stop(model, db)
    return session


@session_router.post("/register", response_model=RegisterSportsSessionModel)
async def register(model: RegisterSportsSessionModel, db: Session = Depends(get_db)):
    session = SessionService().register(model, db)
    return session
