from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.db import Base
from app.modules.sport_man.domain.entities import SportsMan


class Allergy(Base):
    __tablename__ = "allergy"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String(200))
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __str__(self):
        return self.name
    
class AllergySportMan(Base):
    __tablename__ = "allergy_sportman"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sportsman_id: Mapped[int] = mapped_column(ForeignKey("sportsman.id"), index=True)
    allergy_id: Mapped[int] = mapped_column(ForeignKey("allergy.id"), index=True)
    sportsman: Mapped["SportsMan"] = relationship()
    allergy: Mapped["Allergy"] = relationship()
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __str__(self):
        return self.name