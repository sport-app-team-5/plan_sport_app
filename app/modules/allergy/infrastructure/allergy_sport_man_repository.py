
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.allergy.aplication.dto import AllergySportManResponseDTO
from app.modules.allergy.domain.entities import AllergySportMan
from app.modules.allergy.domain.repository import AllergySportManRepository

class AllergySportManRepositoryPostgres(AllergySportManRepository):

    def get_all(self, db: Session) -> List[AllergySportManResponseDTO]:
        try:
            allergies = db.query(AllergySportMan).all()
            return allergies
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def update(self, id: int, allergy_data: AllergySportMan, db: Session) -> AllergySportManResponseDTO:
        try:
            allergy = db.query(AllergySportMan).filter(AllergySportMan.id == id).one()
            if not allergy:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='allergy not found')
        
            for key, value in allergy_data.dict().items():
                setattr(allergy, key, value)
            db.commit()
            return allergy
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def create(self, allergy_data: AllergySportMan, db: Session) -> AllergySportManResponseDTO:
        try:
            allergy = AllergySportMan(**allergy_data.dict())
            db.add(allergy)
            db.commit()
            return allergy
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_by_id(self, sport_man_id: int, db: Session) -> List[AllergySportManResponseDTO]:
        try:
            allergies = db.query(AllergySportMan).filter(AllergySportMan.sportsman_id == sport_man_id).all()
            return allergies
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def delete(self, id: int, db: Session) -> AllergySportManResponseDTO:
        try:
            allergy = db.query(AllergySportMan).filter(AllergySportMan.id == id).one()
            if not allergy:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='allergy not found')
            db.delete(allergy)
            db.commit()
            return allergy
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))