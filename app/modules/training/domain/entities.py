from datetime import datetime
from sqlalchemy import DateTime, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.config.db import Base


class Training(Base):
    __tablename__ = "training_plan"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sportsman_id: Mapped[int] = mapped_column(ForeignKey("sportsman.id"), index=True)
    is_inside_house: Mapped[bool] = mapped_column(Boolean)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(200))
    duration: Mapped[int] = mapped_column(Integer)
    sport: Mapped[str] = mapped_column(String(100))
    intensity: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __str__(self):
        return self.name
