from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.db import Base
from app.modules.sport_man.domain.entities import SportsMan


class SportManInjury(Base):
    __tablename__ = "sportman_injury"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_sporman: Mapped[int] = mapped_column(ForeignKey("sportsman.id"), index=True, nullable=True)
    id_injury: Mapped[int] = mapped_column(ForeignKey("injuries.id"), index=True, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    injury: Mapped["Injury"] = relationship()
    sportsman: Mapped["SportsMan"] = relationship(back_populates="injuries")

    def __str__(self):
        return self.id


class Injury(Base):
    __tablename__ = "injuries"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(200))
    severity: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __str__(self):
        return self.name
