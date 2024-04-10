from pydantic import ConfigDict, BaseModel

    
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