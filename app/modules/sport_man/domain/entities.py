from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.db import Base



class SportsMan(Base):
    __tablename__ = "sportsman"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer)
    sport_profile_id: Mapped[int] = mapped_column(ForeignKey("sport_profile.id"), index=True, nullable=True)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscription.id"), index=True, nullable=True)
    food_preference: Mapped[str] = mapped_column(String(20), nullable=True)
    training_goal: Mapped[str] = mapped_column(String(20), nullable=True)


    birth_year: Mapped[int] =  mapped_column(Integer, nullable=True)
    height: Mapped[int] =  mapped_column(Integer, nullable=True)
    weight: Mapped[int] =  mapped_column(Integer, nullable=True)
    body_mass_index: Mapped[float] =  mapped_column(Float, nullable=True)


    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sport_profile = relationship("SportProfile", foreign_keys=[sport_profile_id])
    subscription = relationship("Subscription", foreign_keys=[subscription_id])

    def __str__(self):
        return self.name
    

class Subscription(Base):
    __tablename__ = "subscription"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)    
    description: Mapped[str] = mapped_column(String(200))
    type: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __str__(self):
        return self.name
    
class SportProfile(Base):
    __tablename__ = "sport_profile"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ftp: Mapped[str] = mapped_column(String(5))    
    vo2_max: Mapped[str] = mapped_column(String(5))
    training_time: Mapped[float] = mapped_column(Float)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __str__(self):
        return self.name