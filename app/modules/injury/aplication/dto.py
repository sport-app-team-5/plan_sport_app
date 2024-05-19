from pydantic import BaseModel


class InjuryResponseDTO(BaseModel):
    name: str
