from fastapi import APIRouter
from app.api.v1.private import seeder_router, session_router, training_router, injury_router
from app.api.v1.private import sport_men_router as sport_men_router_private, allergy_router
from app.api.v1.public import sport_men_router as sport_men_router_public
from app.api.v1.private import nutritional_information_router

public_router = APIRouter(prefix="")
public_router.include_router(sport_men_router_public)

private_router = APIRouter(prefix="/auth")
private_router.include_router(session_router)
private_router.include_router(training_router)
private_router.include_router(seeder_router)
private_router.include_router(allergy_router)
private_router.include_router(sport_men_router_private)
private_router.include_router(nutritional_information_router)
private_router.include_router(injury_router)
