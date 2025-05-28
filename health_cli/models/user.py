from sqlalchemy import Column, Integer, String, DateTime, Create_engine, ForeignKey
from sqlalcemy.orm import declarative_base, relationship, sessionmaker

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    entries = relationship("FoodEntry", back_populates="user")
    goals = relationship("Goal", back_populates="user", uselist=False)