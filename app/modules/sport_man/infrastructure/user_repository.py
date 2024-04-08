from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.modules.sport_man.aplication.dto import SportsManResponseDTO
from app.modules.sport_man.domain.entities import SportsMan
from app.modules.sport_man.domain.enum.food_preference_enum import FoodPreference
from app.modules.sport_man.domain.enum.trining_goal_enum import TrainingGoal
from app.modules.sport_man.domain.repository import UserRepository



class UserRepositoryPostgres(UserRepository):

    @staticmethod
    def __validate_exist_sport_men(user_id: int, db: Session) -> SportsMan:
        sport_man = db.query(SportsMan).filter(SportsMan.user_id == user_id).first()
        if not sport_man:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Sports men not found')

        return sport_man

    def get_by_id(self, user_id: int, db: Session) -> SportsManResponseDTO:
        try:
            sport_man = self.__validate_exist_sport_men(user_id, db)
            return sport_man
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_all(self, db: Session) -> List[SportsManResponseDTO]:
        try:
            users = db.query(SportsMan).all()
            return users
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def create(self, entity: SportsMan, db: Session) -> SportsManResponseDTO:
        try:
            sportsman = SportsMan()
            sport_men = db.query(SportsMan).filter(SportsMan.user_id == entity.user_id).first()
            if sport_men:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Sports men already exist')
            sportsman.user_id = entity.user_id
            sportsman.sport_profile_id = entity.sport_profile_id
            sportsman.subscription_id = entity.subscription_id
            if isinstance(entity.food_preference, FoodPreference):
                sportsman.food_preference = entity.food_preference.value
            elif isinstance(sportsman.training_goal, TrainingGoal):
                sportsman.training_goal = entity.training_goal
            sportsman.birth_year = entity.birth_year
            sportsman.height = entity.height
            sportsman.weight = entity.weight
            sportsman.body_mass_index = entity.body_mass_index
            db.add(sportsman)
            db.commit()
            return sportsman
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def update(self, entity_id: int, entity: SportsMan, db: Session) -> SportsManResponseDTO:
        try:

            sportsman = db.query(SportsMan).filter(SportsMan.id == entity_id).first()
            
            if sportsman:
                sportsman.user_id = entity.user_id
                sportsman.sport_profile_id = entity.sport_profile_id
                sportsman.subscription_id = entity.subscription_id
                if isinstance(entity.food_preference, FoodPreference):
                    sportsman.food_preference = entity.food_preference.value
                elif isinstance(sportsman.training_goal, TrainingGoal):
                    sportsman.training_goal = entity.training_goal
                sportsman.birth_year = entity.birth_year
                sportsman.height = entity.height
                sportsman.weight = entity.weight
                sportsman.body_mass_index = entity.body_mass_index
                db.add(sportsman)
                db.commit()
                
                return sportsman
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sport men not found")    
            
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))