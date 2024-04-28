from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from app.config.db import Base


class SportsSession(Base):
    __tablename__ = 'training_plan_sportman'

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, nullable=False, unique=True )
    time: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    sportsman_id:  Mapped[int] = mapped_column(Integer, ForeignKey('sportsman.id'), nullable=False)
    training_plan_id: Mapped[int] = mapped_column(Integer, ForeignKey('training_plan.id'), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    def __str__(self):
        return self.id

class Monitoring(Base):
    __tablename__ = 'monitoring'

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey('training_plan_sportman.id'), nullable=False)
    indicators_id: Mapped[int] = mapped_column(Integer, ForeignKey('indicators.id'), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    def __str__(self):
        return self.session_id

class Indicators(Base):
    __tablename__ = 'indicators'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    def __str__(self):
        return self.name
