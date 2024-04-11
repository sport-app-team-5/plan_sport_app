
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.allergy.aplication.dto import AllergySportManResponseDTO
from app.modules.allergy.domain.entities import Allergy, AllergySportMan
from app.modules.allergy.domain.repository import AllergySportManRepository
from app.modules.sport_man.domain.entities import SportsMan

class AllergySportManRepositoryPostgres(AllergySportManRepository):

    def create(self, allergy: AllergySportMan, db: Session) -> AllergySportManResponseDTO:
        try:
            has_data_allergy = db.query(Allergy).filter(Allergy.id == allergy.allergy_id).first()
            if not has_data_allergy:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Allergy not exist')
            has_data_sport_man = db.query(SportsMan).filter(SportsMan.id == allergy.sportsman_id).first()
            if not has_data_sport_man:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not exist')
            db.add(allergy)
            db.commit()
            return allergy
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_by_id(self, sport_man_id: int, db: Session) -> List[AllergySportManResponseDTO]:
        try:
            allergies = db.query(AllergySportMan).filter(AllergySportMan.sportsman_id == sport_man_id).all()
            if not allergies:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nutritional information not exist')
            return allergies
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def delete(self, sport_man_id: int, db: Session) -> AllergySportManResponseDTO:
        try:
            allergies = db.query(AllergySportMan).filter(AllergySportMan.sportsman_id == sport_man_id).all()
            if allergies:                
                for allergy in allergies:
                    db.delete(allergy)
                db.commit()
            return allergies
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))