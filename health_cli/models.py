from sqlalchemy import Column, Integer, String, DateTime, Create_engine, ForeignKey
from sqlalcemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    entries = relationship("FoodEntry", back_populates="user")
    goals = relationship("Goal", back_populates="user", uselist=False)
    
class FoodEntry(Base):
    __tablename__ = 'food_entries'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    food_name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="entries")
 