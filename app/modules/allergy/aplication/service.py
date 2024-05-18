from typing import List
from sqlalchemy.orm import Session

from app.modules.allergy.aplication.dto import AllergyDTO, AllergySportManResponseDTO, AllergySportManRequestDTO, NutritionalInformationRequestDTO, NutritionalInformationResponseDTO, AllergyDescDTO
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
    
    def get_allergy_by_id(self, allergy_id: int, db: Session) -> AllergyDTO:
        repository = self._repository_factory.create_object(AllergyRepository)
        return repository.get_by_id(allergy_id, db)
    
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

    def create_nutritional_information(self, user_id: int, nutritional_information: NutritionalInformationRequestDTO, db: Session):
        
        sports_man_service = SportsManService()
        sport_man = sports_man_service.get_sportsmen_by_id(user_id, db)
        sport_man_id = sport_man.id
        sport_man.user_id = user_id

        allergies_sport_men_service = AllergiesSportsMenService()
        allergies_sport_men_service.delete_all_allergies_by_sport_man_id(sport_man_id, db)
        for  allergy_id in nutritional_information.allergies:                
                allergy_sport_man = AllergySportMan()
                allergy_sport_man.allergy_id = allergy_id
                allergy_sport_man.sportsman_id = sport_man_id
                allergies_sport_men_service.create_allergy(allergy_sport_man, db)

        if nutritional_information.food_preference:
            sport_man_service = SportsManService()
            sport_nut_profile = SportsManRequestDTO(user_id=user_id, food_preference=nutritional_information.food_preference)
            sport_man.food_preference = sport_nut_profile.food_preference
            sport_man_service.update_sportsmen(sport_man_id, sport_man, db)

        return nutritional_information        
       
    
    def get_nutritional_information(self, user_id: int, db: Session) -> NutritionalInformationResponseDTO:
        allergies_sport_men_service = AllergiesSportsMenService()
        sports_man_service = SportsManService()
        allergies_service = AllergiesService()

        sport_man = sports_man_service.get_sportsmen_by_id(user_id, db)
        sport_man_id = sport_man.id

        allergies_sportman = allergies_sport_men_service.get_allergies_by_sport_man_id(sport_man_id, db)    

        allergies = []
        
        for allergy in allergies_sportman:
            allergy_desc = AllergyDescDTO()
            allergy_db = allergies_service.get_allergy_by_id(allergy.allergy_id, db)
            allergy_desc.id = allergy_db.id
            allergy_desc.name = allergy_db.name
            allergy_desc.description = allergy_db.description
            allergies.append(allergy_desc)


        nutritional_information = NutritionalInformationResponseDTO()
        nutritional_information.sportsman_id = sport_man_id
        nutritional_information.allergies = allergies
        nutritional_information.food_preference = sport_man.food_preference

        return nutritional_information
