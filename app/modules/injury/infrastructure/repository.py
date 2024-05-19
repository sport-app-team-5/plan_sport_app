from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.modules.injury.aplication.dto import InjuryResponseDTO
from app.modules.injury.domain.entities import SportManInjury
from app.modules.injury.domain.repository import InjuryRepository


class InjuryRepositoryPostgres(InjuryRepository):
    def get_by_sportsman_id(self, sportsman_id: int, db: Session) -> InjuryResponseDTO:
        try:
            injuries = db.query(SportManInjury).filter(SportManInjury.id_sporman == sportsman_id).all()
            injuries_str: str = ''
            for injury_iterator in injuries:
                if injuries_str == '':
                    injuries_str += injury_iterator.injury.name
                else:
                    injuries_str += ', ' + injury_iterator.injury.name
            return InjuryResponseDTO(name=injuries_str)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
