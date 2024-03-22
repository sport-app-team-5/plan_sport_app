from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import Column, Float, ForeignKey, Integer, Sequence, String, DateTime, Boolean, column, func
from app.config.db import Base


class SportsSession(Base):
    __tablename__ = 'sports_session'#TODO: Esto debe ser reemplazado por SportMan?

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, nullable=False, unique=True )
    description: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    def __str__(self):
        return self.id

class Monitoring(Base):
    __tablename__ = 'monitoring'

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey('sports_session.id'), nullable=False)#TODO: Esto debe ser reemplazado por SportMan?
    indicators_id: Mapped[int] = mapped_column(Integer, ForeignKey('indicators.id'), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    def __str__(self):
        return self.session_id

class Indicators(Base):
    __tablename__ = 'indicators'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    def __str__(self):
        return self.name
