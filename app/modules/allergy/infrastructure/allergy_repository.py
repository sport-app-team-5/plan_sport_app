from typing import List
from app.modules.allergy.aplication.dto import AllergyDTO
from app.modules.allergy.domain.entities import Allergy
from app.modules.allergy.domain.repository import AllergyRepository
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

class AllergyRepositoryPostgres(AllergyRepository):

    def get_all(self, db: Session) -> List[AllergyDTO]:
        try:
            allergies = db.query(Allergy).all()
            return allergies
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        

    def get_by_id(self, allergy_id: int, db: Session) -> AllergyDTO:
        try:
            allergy = db.query(Allergy).filter(Allergy.id == allergy_id).one_or_none()
            return allergy
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    