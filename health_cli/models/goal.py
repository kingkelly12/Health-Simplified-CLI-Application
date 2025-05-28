from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from health_cli.models.user import User
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

Base = declarative_base()

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    daily_calories = Column(Integer)
    weekly_calories = Column(Integer)
    user = relationship("User", back_populates="goals")
    
    def __repr__(self):
        return f"<Goal(id={self.id}, user_id={self.user_id}, daily_calories={self.daily_calories}, weekly_calories={self.weekly_calories})>"
    
    @classmethod
    def create(cls, session: Session, user_id: int, daily_calories: int, weekly_calories: int):
        goal = cls(user_id=user_id, daily_calories=daily_calories, weekly_calories=weekly_calories)
        session.add(goal)
        session.commit()
        return goal
    
    @classmethod
    def get_by_user(cls, session: Session, user_id: int):
        return session.query(cls).filter_by(user_id=user_id).first()
    
    @classmethod
    def update(cls, session: Session, user_id: int, daily_calories: int = None, weekly_calories: int = None):
        goal = session.query(cls).filter_by(user_id=user_id).first()
        if goal:
            if daily_calories is not None:
                goal.daily_calories = daily_calories
            if weekly_calories is not None:
                goal.weekly_calories = weekly_calories
            session.commit()
            return goal
        return None
    
    @classmethod
    def delete(cls, session: Session, user_id: int):
        goal = session.query(cls).filter_by(user_id=user_id).first()
        if goal:
            session.delete(goal)
            session.commit()
            return True
        return False