from sqlalchemy import Column, Integer, String, DateTime, Create_engine, ForeignKey
from sqlalcemy.orm import declarative_base, relationship, sessionmaker


class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    daily_calories = Column(Integer)
    weekly_calories = Column(Integer)
    user = relationship("User", back_populates="goals")