from fastapi import APIRouter
from app.api.v1.private import seeder_router, session_router
from app.api.v1.private import sport_men_router, allergy_router
from app.api.v1.private import nutritional_information_router

public_router = APIRouter(prefix="")

private_router = APIRouter(prefix="/auth")
private_router.include_router(session_router)
private_router.include_router(seeder_router)
private_router.include_router(allergy_router)
private_router.include_router(sport_men_router)
private_router.include_router(nutritional_information_router)