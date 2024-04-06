from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from app.seedwork.domain.entities import Entity

class StartSportsSessionRequestModel(BaseModel):
    id: Optional[str] = None
    description: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "description": "Sesion de pesas",
        }
    })


class StartSportsSessionResponseModel(BaseModel):
    id: str
    model_config = ConfigDict(from_attributes=True)

class RegisterSportsSessionModel(BaseModel):
    id:  Optional[int] = None
    session_id: str
    indicators_id: int
    value: float
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "session_id": "6ecd8c99-4036-403d-bf84-cf8400f67836",
            "indicators_id": "1",
            "value": "60",
        }
    })

class RegisterSportsSessionResponseModel(BaseModel):
    id: int
    session_id:  Optional[str] = None
    indicators_id:  Optional[int] = None
    value:  Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)

class StopSportsSessionRequestModel(BaseModel):
    id: str
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "6ecd8c99-4036-403d-bf84-cf8400f67836",
        }
    })


class StopSportsSessionResponseModel(BaseModel):
    id: str
    model_config = ConfigDict(from_attributes=True)