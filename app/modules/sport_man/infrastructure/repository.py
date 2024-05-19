from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.modules.injury.domain.entities import SportManInjury
from app.modules.sport_man.aplication.dto import (SportResponseIndicatorsProfileDTO, SportsManResponseDTO,
                                                  SportManResponseProfileSportDTO, \
                                                  InjuryResponseDTO, SportManResponseProfileDTO)
from app.modules.sport_man.domain.entities import SportProfile, SportsMan, Subscription
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

    def calculate_clasification(self, muscle_mass_index, limits) -> SportManRisk:
        classification = SportManRisk.WITOOUTRISK.value
        if muscle_mass_index >= limits["high"]:
            classification = SportManRisk.HIGHRISK.value
        elif muscle_mass_index >= limits["medium"]:
            classification = SportManRisk.MEDIUMRISK.value
        elif muscle_mass_index >= limits["low"]:
            classification = SportManRisk.LOWRISK.value
        return classification

    def calculateRisk(self, year_of_birth, muscle_mass_index) -> SportManRisk:
        current_year = datetime.now().year
        age = current_year - year_of_birth

        risk_limits = {
            "<18": {"high": 30, "medium": 25, "low": 18.5},
            "18-30": {"high": 30, "medium": 25, "low": 20},
            "30-50": {"high": 30, "medium": 26, "low": 21},
            ">50": {"high": 30, "medium": 27, "low": 22}
        }

        classification = SportManRisk.WITOOUTRISK.value

        age_ranges = [
            ("<18", lambda age: age < 18),
            ("18-30", lambda age: 18 <= age < 30),
            ("30-50", lambda age: 30 <= age < 50),
            (">50", lambda age: age >= 50),
        ]

        for age_range, age_check in age_ranges:
            if age_check(age):
                classification = self.calculate_clasification(muscle_mass_index, risk_limits[age_range])
                break

        return classification

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

            return SportManResponseProfileDTO(id=sports_men.id, sport_preference=sports_men.sport_preference,
                                              injuries=injuries,
                                              exercise_experience=sports_men.exercise_experience,
                                              time_dedication_sport=sports_men.time_dedication_sport,
                                              risk=sports_men.risk, birth_year=sports_men.birth_year,
                                              height=sports_men.height, weight=sports_men.weight,
                                              subscription_id=sports_men.subscription_id)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=502, detail=str(e))

    def update_suscription_id(self, sportman_id: int, suscription_type: str, db: Session):
        try:
            sport_man = db.query(SportsMan).filter(SportsMan.id == sportman_id).first()
            subscription = db.query(Subscription).filter(Subscription.type == suscription_type).first()
            sport_man.subscription_id = subscription.id
            db.add(sport_man)
            db.commit()
            return sport_man
        except SQLAlchemyError as e:
            raise HTTPException(status_code=502, detail=str(e))

    def create_sport_indicators_profile(self, user_id: int, ftp: str, vo2_max: str, training_time: str,
                                        db: Session) -> SportManResponseProfileSportDTO:
        try:
            sport_man = self.__validate_exist_sport_men(user_id, db)

            training_time_parts = training_time.split(':')
            minutes = int(training_time_parts[1])
            seconds = int(training_time_parts[2])
            training_time_double = minutes + seconds / 60

            sport_profile = SportProfile(ftp=ftp, vo2_max=vo2_max, training_time=training_time_double)
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
