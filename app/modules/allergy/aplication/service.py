from typing import List
from sqlalchemy.orm import Session

from app.modules.allergy.aplication.dto import AllergyDTO, AllergySportManResponseDTO, AllergySportManRequestDTO, NutritionalInformationRequestDTO
from app.modules.allergy.domain.entities import AllergySportMan
from app.modules.allergy.domain.repository import AllergyRepository, AllergySportManRepository
from app.modules.allergy.infrastructure.factories import RepositoryFactory
from app.modules.sport_man.aplication.dto import SportsManRequestDTO
from app.modules.sport_man.aplication.service import SportsManService

class AllergiesService:
    def __init__(self):
        self._repository_factory = RepositoryFactory()

    def get_allergies(self, db: Session) -> List[AllergyDTO]:
        repository = self._repository_factory.create_object(AllergyRepository)
        return repository.get_all(db)
    
class AllergiesSportsMenService:
    def __init__(self):
        self._repository_factory = RepositoryFactory()

    def create_allergy(self, allergy_data: AllergySportManRequestDTO, db: Session) -> AllergySportManResponseDTO:
        repository = self._repository_factory.create_object(AllergySportManRepository)
        return repository.create(allergy_data, db)

    def get_allergies_by_sport_man_id(self , sport_man_id: int, db: Session) -> List[AllergySportManResponseDTO]:
        repository = self._repository_factory.create_object(AllergySportManRepository)
        return repository.get_by_id(sport_man_id, db)
    
    def delete_all_allergies_by_sport_man_id(self, sport_man_id: int, db: Session) -> AllergySportManResponseDTO:
        repository = self._repository_factory.create_object(AllergySportManRepository)
        return repository.delete(sport_man_id, db)
    
class NutritionalInformationService:

    def create_nutritional_information(self, sport_man_id: int, nutritional_information: NutritionalInformationRequestDTO, db: Session):
        allergies_sport_men_service = AllergiesSportsMenService()
        allergies_sport_men_service.delete_all_allergies_by_sport_man_id(sport_man_id, db)
        for  allergy_id in nutritional_information.allergies:                
                allergy_sport_man = AllergySportMan()
                allergy_sport_man.allergy_id = allergy_id
                allergy_sport_man.sportsman_id = sport_man_id
                allergies_sport_men_service.create_allergy(allergy_sport_man, db)

        if nutritional_information.food_preference:
            sport_man_service = SportsManService()
            sport_man = SportsManRequestDTO(user_id=sport_man_id, food_preference=nutritional_information.food_preference)
            sport_man_service.update_sportsmen(sport_man_id, sport_man, db)

        return nutritional_information    

    