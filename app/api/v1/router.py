from fastapi import APIRouter
from app.api.v1.public import session_router, health_check_router as public_plan_router
from app.api.v1.public import health_check_router
from app.api.v1.private import seeder_router as private_plan_router

public_router = APIRouter(prefix="")
public_router.include_router(session_router)
public_router.include_router(health_check_router)
public_router.include_router(public_plan_router)

private_router = APIRouter(prefix="")
private_router.include_router(private_plan_router)
