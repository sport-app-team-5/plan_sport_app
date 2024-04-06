from typing import Optional
from pydantic import ConfigDict, BaseModel

from app.modules.sport_man.domain.enum.food_preference_enum import FoodPreference
from app.modules.sport_man.domain.enum.subscription_type_enum import SubscriptionType
from app.modules.sport_man.domain.enum.trining_goal_enum import TrainingGoal

class SportsManRequestDTO(BaseModel):
    user_id: int
    sport_profile_id:  Optional[int]  = None
    food_preference: Optional[FoodPreference] = None
    training_goal: Optional[TrainingGoal]  = None
    subscription_id: Optional[int]  = None
    birth_year: Optional[int]  = None
    height: Optional[int]  = None
    weight: Optional[int]  = None
    body_mass_index: Optional[float]  = None
    model_config = ConfigDict(json_schema_extra={
            "example": {
                "user_id": 1,
                "sport_profile_id": 1,
                "subscription_id": 1,
                "food_preference": "VEGAN",
                "training_goal": "TONE",
                "birth_year": 2000,
                "height": 180,
                "weight": 75,
                "body_mass_index": 25.0
            }
        })


class SportsManResponseDTO(BaseModel):
    id: int
    user_id: int
    sport_profile_id: Optional[int]  = None
    food_preference: Optional[FoodPreference]  = None
    training_goal: Optional[TrainingGoal]  = None
    subscription_id: Optional[int]  = None
    birth_year: Optional[int]  = None
    height: Optional[int]  = None
    weight: Optional[int]  = None
    body_mass_index: Optional[float]  = None

    model_config = ConfigDict(from_attributes=True)

class SubscriptionDTO(BaseModel):
    id: int
    description: str
    type: SubscriptionType

    model_config = ConfigDict(json_schema_extra={
            "example": {
                "id": 1,
                "description": "example_description",
                "type": "example_type"
            }
        })

class SportProfileDTO(BaseModel):
    id: int
    ftp: str
    vo2_max: str
    training_time: float

    model_config = ConfigDict(json_schema_extra={
            "example": {
                "id": 1,
                "ftp": "100",
                "vo2_max": "95",
                "training_time": 1.5
            }
        })