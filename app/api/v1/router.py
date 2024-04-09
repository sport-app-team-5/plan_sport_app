from fastapi import APIRouter
from app.api.v1.private import session_router
from app.api.v1.public import sport_men_router

public_router = APIRouter(prefix="")
public_router.include_router(sport_men_router)

private_router = APIRouter(prefix="/auth")
private_router.include_router(session_router)
