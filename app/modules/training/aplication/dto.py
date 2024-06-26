from typing import Optional
from pydantic import ConfigDict, BaseModel
from app.modules.sport_man.domain.enum.sport_preference_enum import SportPreference
from app.modules.training.domain.enum.intensity_enum import Intensity


class TrainingDTO(BaseModel):
    id: Optional[int] = None
    sportsman_id: Optional[int] = None
    is_inside_house: bool
    name: str
    description: str
    sport: SportPreference
    intensity: Intensity
    duration: int

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "is_inside_house": True,
            "name": "Example Training",
            "description": "This is an example training",
            "sport": "Atletismo",
            "intensity": "Alta",
            "duration": 60
        }
    })


class TrainingUpdateDTO(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    sport: Optional[SportPreference] = None
    intensity: Optional[Intensity] = None
    duration: Optional[int] = None

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": 1,
            "name": "Example Training",
            "description": "This is an example training",
            "sport": "Atletismo",
            "intensity": "Alta",
            "duration": 60
        }
    })


class TrainingResponseDTO(BaseModel):
    id: int
    sportsman_id: int
    is_inside_house: bool
    name: str
    description: str
    sport: SportPreference
    intensity: Intensity
    duration: int


class TrainingResDTO(BaseModel):
    name: str
    intensity: Intensity


class TrainingPlanResponseDTO(BaseModel):
    time: str
    training_plan: TrainingResDTO
