from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.modules.sport_man.aplication.dto import SportResponseIndicatorsProfileDTO, SportsManResponseDTO, SportManResponseProfileSportDTO, \
    InjuryResponseDTO, SportManResponseProfileDTO
from app.modules.sport_man.domain.entities import SportProfile, SportsMan, Injuries, SportManInjury, Subscription
from app.modules.sport_man.domain.enum.food_preference_enum import FoodPreference
from app.modules.sport_man.domain.enum.trining_goal_enum import TrainingGoal
from app.modules.sport_man.domain.repository import UserRepository
from app.modules.sport_man.domain.enum.sport_preference_enum import SportPreference, SporExperience, SportDedication, \
    SportManRisk
from datetime import datetime


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

    def update_sport_profile(self, user_id: int, entity: SportsMan, db: Session) -> SportManResponseProfileSportDTO:
        try:
            sport_men = db.query(SportsMan).filter(SportsMan.user_id == user_id).first()
            if not sport_men:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Sports men not exist')
            altura = entity.height
            sport_men.birth_year = entity.birth_year
            sport_men.height = altura
            sport_men.weight = entity.weight
            sport_men.exercise_experience = entity.exercise_experience

            if isinstance(entity.sport_preference, SportPreference):
                sport_men.sport_preference = entity.sport_preference.value

            if isinstance(entity.time_dedication_sport, SportDedication):
                sport_men.time_dedication_sport = entity.time_dedication_sport.value

            if isinstance(entity.exercise_experience, SporExperience):
                sport_men.exercise_experience = entity.exercise_experience.value
            mass_index_value = round((entity.weight) / ((altura / 100) ** 2), 1)
            sport_men.body_mass_index = mass_index_value
            sport_men.risk = self.calculateRisk(entity.birth_year, mass_index_value)
            db.add(sport_men)
            db.commit()
            return sport_men
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def calculateRisk(self, birth_year: int, body_mass_index: float) -> SportManRisk:
        risk = SportManRisk.WITOOUTRISK.value
        current_year = datetime.now().year
        age = current_year - birth_year
        if (age > 70 and body_mass_index < 16.5) or (age > 70 and body_mass_index > 30):
            risk = SportManRisk.HIGHRISK.value

        elif (55 < age <= 70 and 16.5 <= body_mass_index <= 18.5) or (55 < age <= 70 and 25 <= body_mass_index <= 30):
            risk = SportManRisk.MEDIUMRISK.value

        elif age <= 55 and 18.5 < body_mass_index < 25:
            risk = SportManRisk.WITOOUTRISK.value

        return risk

    def create_injury(self, id_injury: int, sportman_id: int, db: Session) -> InjuryResponseDTO:
        try:
            injury = SportManInjury()
            injury_db = db.query(SportManInjury).filter(SportManInjury.id_injury == id_injury).first()
            if not injury_db:
                injury.id_sporman = sportman_id
                injury.id_injury = id_injury
                db.add(injury)
                db.commit()
                return injury
        except SQLAlchemyError as e:
            db.rollback()
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
            raise HTTPException(status_code=500, detail=str(e))

    def update(self, entity_id: int, entity: SportsMan, db: Session) -> SportsManResponseDTO:
        try:
            sportsman = db.query(SportsMan).filter(SportsMan.id == entity_id).first()

            if sportsman:
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
            raise HTTPException(status_code=status.HTTP_502_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_sports_profile(self, user_id: int, db: Session) -> SportManResponseProfileDTO:
        try:
            sports_men = db.query(SportsMan).filter(SportsMan.user_id == user_id).first()
            if sports_men.risk == None:
                raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail="Sport man not have risk")
                
            injuries = []
            for injury in sports_men.injuries:
                injuries.append(injury.injury.name)

            return SportManResponseProfileDTO(id=sports_men.id, sport_preference=sports_men.sport_preference, injuries=injuries,
                                              exercise_experience=sports_men.exercise_experience,
                                              time_dedication_sport=sports_men.time_dedication_sport,
                                              risk=sports_men.risk)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=502, detail=str(e))

    def update_suscription_id(self, user_id: int, suscription_type: str, db: Session):
        try:
            sport_man = db.query(SportsMan).filter(SportsMan.user_id == user_id).first()
            subscription = db.query(Subscription).filter(Subscription.type == suscription_type).first()
            sport_man.subscription_id = subscription.id
            db.add(sport_man)
            db.commit()
            return sport_man
        except SQLAlchemyError as e:
            raise HTTPException(status_code=502, detail=str(e))
    
    
    def create_sport_indicators_profile(self, user_id: int, ftp:str, vo2_max: str, training_time: str,  db: Session) -> SportManResponseProfileSportDTO:
        try:
            sport_man = self.__validate_exist_sport_men(user_id, db)
            
            training_time_parts = training_time.split(':')
            minutes = int(training_time_parts[1])
            seconds = int(training_time_parts[2])
            training_time_double = minutes + seconds / 60       

            sport_profile = SportProfile(ftp=ftp, vo2_max=vo2_max, training_time=training_time_double )
            sport_man.sport_profile_id = sport_profile.id

            db.add(sport_profile)
            db.commit()
            return sport_profile
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    def get_indicator_profile_by_user_id(self, user_id: int, db: Session) -> SportResponseIndicatorsProfileDTO:
        try:
            sport_man = self.__validate_exist_sport_men(user_id, db)
            sport_profile = db.query(SportProfile).filter(SportProfile.id == sport_man.sport_profile_id).first()
            return sport_profile
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

