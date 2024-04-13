from typing import List
from pydantic import ConfigDict, BaseModel

from app.modules.sport_man.domain.enum.food_preference_enum import FoodPreference

    
class AllergyDTO(BaseModel):
    id: int
    description: str
    name: str

    model_config = ConfigDict(json_schema_extra={
            "example": {
                "id": 1,
                "description": "Intolerance to gluten",
                "name": "Gluten"
            }
        })
    
class AllergySportManRequestDTO(BaseModel):
    sportsman_id: int
    allergy_id: int

    model_config = ConfigDict(json_schema_extra={
            "example": {
                "sportsman_id": 1,
                "allergy_id": 1
            }
        })
    
class AllergySportManResponseDTO(BaseModel):
    sportsman_id: int
    allergy_id: int
    id: int

    model_config = ConfigDict(json_schema_extra={
            "example": {
                "sportsman_id": 1,
                "allergy_id": 1
            }
        })
class NutritionalInformationRequestDTO(BaseModel):
    allergies: List[int]
    food_preference: FoodPreference

    model_config = ConfigDict(json_schema_extra={
            "example": {
                "allergies": [1, 2],
                "food_preference": "VEGAN"
            }
        })