from fastapi import APIRouter
from app.api.v1.public import session_router as public_plan_router
from app.api.v1.public import sport_men_router, session_router

public_router = APIRouter(prefix="")
public_router.include_router(session_router)
public_router.include_router(sport_men_router)
public_router.include_router(public_plan_router)