from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.modules.sport_man.domain.enum.sport_preference_enum import SportPreference
from app.modules.training.aplication.dto import TrainingDTO, TrainingUpdateDTO, TrainingResponseDTO
from app.modules.training.domain.entities import Training
from app.modules.training.domain.enum.intensity_enum import Intensity
from app.modules.training.domain.repository import TrainingRepository


class TrainingRepositoryPostgres(TrainingRepository):
    @staticmethod
    def __validate_exist_training(id: int, db: Session) -> Training:
        training = db.query(Training).filter(Training.id == id).first()
        if not training:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Training not found')

        return training

    def get_by_id(self, id: int, db: Session) -> TrainingDTO:
        try:
            training = self.__validate_exist_training(id, db)
            if training.sport == 1:
                training.sport = SportPreference.CYCLING
            else:
                training.sport = SportPreference.ATHLETICS

            return training
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_all(self, db: Session) -> List[TrainingDTO]:
        try:
            trainings = db.query(Training).all()
            training_dto = []
            for training in trainings:
                sport_preference = SportPreference.CYCLING if training.sport == 1 else SportPreference.ATHLETICS
                training_dto.append(
                    TrainingDTO(
                        id=training.id,
                        name=training.name,
                        description=training.description,
                        sport=sport_preference,
                        intensity=Intensity(training.intensity),
                        duration=training.duration
                    )
                )
            return training_dto
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def update(self, id: int, entity: TrainingUpdateDTO, db: Session) -> TrainingDTO:
        try:
            training = db.query(Training).filter(Training.id == id).first()
            if not training:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Training not exist')
            if entity.name:
                training.name = entity.name
            if entity.description:
                training.description = entity.description
            if isinstance(entity.sport, SportPreference):
                sport_index = list(SportPreference).index(entity.sport)
                training.sport = sport_index + 1
            if isinstance(entity.intensity, Intensity):
                training.intensity = entity.intensity.value
            if entity.duration:
                training.duration = entity.duration

            db.add(training)
            db.commit()
            if training.sport:
                training.sport = self.__convert_sport_preference(training)
            return training

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def create(self, entity: TrainingDTO, db: Session) -> TrainingDTO:
        try:
            training = Training()
            sport_men = db.query(Training).filter(Training.name == entity.name).first()
            if sport_men:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Training already exist')
            training.name = entity.name
            training.description = entity.description
            training.sportsman_id = entity.sportsman_id
            training.sport = entity.sport.value
            training.intensity = entity.intensity.value
            training.duration = entity.duration
            training.is_inside_house = entity.is_inside_house
            db.add(training)
            db.commit()
            training.sport = self.__convert_sport_preference(training)
            return training
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def __convert_sport_preference(self, training):
        if training.sport == 1:
            return SportPreference.CYCLING
        else:
            return SportPreference.ATHLETICS

    def get_by_sportsman_id(self, sportsman_id: int, db: Session) -> List[TrainingResponseDTO]:
        try:
            trainings = db.query(Training).filter(Training.sportsman_id == sportsman_id).all()
            return trainings
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
