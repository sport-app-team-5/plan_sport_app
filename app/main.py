import logging
from fastapi import FastAPI, APIRouter
from app import api
from app.config.env import env

app = FastAPI()
app.title = env.PROJECT_NAME
app.version = env.PROJECT_VERSION

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

api_v1_plan = APIRouter(prefix='/api/v1/plan')
api_v1_plan.include_router(api.session_router)
app.include_router(api.health_check_router)
app.include_router(api_v1_plan)

app_test = app
