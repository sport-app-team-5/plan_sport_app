from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.modules.session.aplication.schemas import RegisterSportsSessionResponseModel, StartSportsSessionResponseModel, StopSportsSessionResponseModel
from app.modules.session.domain.model import SportsSession, Monitoring
from app.modules.session.domain.repository import RegisterSessionRepository, StartSessionRepository, StopSessionRepository


class StartSessionRepositoryPostgres(StartSessionRepository):

    def get_all(self, db: Session) -> List[StartSportsSessionResponseModel]:
        try:
            _sessions = db.query(SportsSession).all()
            return _sessions
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def create(self, entity: SportsSession, db: Session, user_id: int) -> StartSportsSessionResponseModel:
        try:
            new_sesion = SportsSession(id=entity.id, status="started", sportsman_id=user_id, training_plan_id=entity.training_plan_id)
            db.add(new_sesion)
            db.commit()
            return new_sesion
        except SQLAlchemyError as e:
            print(str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_by_id(self, entity_id: int, db: Session) -> StartSportsSessionResponseModel:
        try:
            session = db.query(SportsSession).filter(SportsSession.id == entity_id).first()
            if session:
                return session
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def update(self, entity_id: int, entity: SportsSession, db: Session) -> StartSportsSessionResponseModel:
        try:
            session = db.query(SportsSession).filter(SportsSession.id == entity_id).first()
            if session:
                session.time = entity.time
                db.commit()
                return session
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def delete(self, entity_id: int, db: Session) -> StartSportsSessionResponseModel:
        raise NotImplementedError
    
class StopSessionRepositoryPostgres(StopSessionRepository):
    def get_by_id(self, entity_id: int, db: Session) -> StopSportsSessionResponseModel:
        raise NotImplementedError

    def get_all(self, db: Session) -> List[StopSportsSessionResponseModel]:
        try:
            _sessions = db.query(SportsSession).all()
            return _sessions
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def create(self, entity: SportsSession, db: Session) -> StopSportsSessionResponseModel:
        raise NotImplementedError

    def update(self, entity_id: int, entity: SportsSession, db: Session) -> StopSportsSessionResponseModel:
        try:        
            update = db.query(SportsSession).filter(SportsSession.id == entity_id).update({SportsSession.status: "stopped", SportsSession.time: entity.time})
            db.commit()
            return entity
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    def delete(self, entity_id: int, db: Session) -> StopSportsSessionResponseModel:
        raise NotImplementedError
    
    def create_sport_indicators(self, weight: int, entity: SportsSession, db: Session) -> StopSportsSessionResponseModel:
        try:
            average_ftp = self.calculate_average_ftp(entity.id, db)            
            vo2_max = self.calculate_vo2_max(weight, entity.time, db)

            entity.ftp = str(int(average_ftp))
            entity.vo2max = str(int(vo2_max))

            return entity
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    
    def calculate_average_ftp(self, session_id: int, db: Session) -> float:
        try:
            monitoring_records = db.query(Monitoring).filter(Monitoring.session_id == session_id).all()
            ftp_values = [record.value for record in monitoring_records]
            if len(ftp_values) > 0:                
                average_ftp = sum(ftp_values) / len(ftp_values)
                return average_ftp
            else:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No monitoring records found")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def calculate_vo2_max(self, sportman_weight: float, session_duration: int) -> float:
        try:
            oxigin_consumption = 3.5

            weight = sportman_weight
            duration = session_duration
            duration_parts = duration.split(':')
            minutes = int(duration_parts[1])
            seconds = int(duration_parts[2])
            duration_parts_double = minutes + seconds / 60

            velocity = 15

            met = (weight * velocity) / duration_parts_double

            vo2_max = met / oxigin_consumption

            return vo2_max
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

class RegisterSessionRepositoryPostgres(RegisterSessionRepository):
    def get_by_id(self, entity_id: int, db: Session) -> RegisterSportsSessionResponseModel:
        raise NotImplementedError

    def get_all(self, db: Session) -> List[RegisterSportsSessionResponseModel]:
        try:
            _sessions = db.query(Monitoring).all()
            return _sessions
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def create(self, entity: Monitoring, db: Session) -> RegisterSportsSessionResponseModel:
        try:
            new_sesion = Monitoring(session_id = entity.session_id, indicators_id=entity.indicators_id, value=entity.value)
            db.add(new_sesion)
            db.commit()
            return new_sesion
        except SQLAlchemyError as e:
            print(str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def update(self, entity_id: int, entity: Monitoring, db: Session) -> RegisterSportsSessionResponseModel:
        raise NotImplementedError

    def delete(self, entity_id: int, db: Session) -> RegisterSportsSessionResponseModel:
        raise NotImplementedError
    