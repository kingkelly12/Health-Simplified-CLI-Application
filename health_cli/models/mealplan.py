from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from health_cli.models.foodentry import FoodEntry
from sqlalchemy.orm import sessionmaker
from health_cli.models.user import User


Base = declarative_base()

class MealPlan(Base):
    __tablename__ = 'meal_plans'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    meal_name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    user = relationship("User", back_populates="meal_plans")
    
    def __repr__(self):
        return f"<MealPlan(id={self.id}, user_id={self.user_id}, meal_name='{self.meal_name}', calories={self.calories}, date={self.date})>"
    
    @classmethod
    def create(cls, session, user_id, meal_name, calories, date):
        meal_plan = cls(user_id=user_id, meal_name=meal_name, calories=calories, date=date)
        session.add(meal_plan)
        session.commit()
        return meal_plan
    
    @classmethod
    def get_by_user(cls, session, user_id):
        return session.query(cls).filter_by(user_id=user_id).all()
    
    @classmethod
    def get_by_date(cls, session, user_id, date):
        return session.query(cls).filter_by(user_id=user_id, date=date).all()
    
    @classmethod
    def update(cls, session, meal_plan_id, meal_name=None, calories=None, date=None):
        meal_plan = session.query(cls).filter_by(id=meal_plan_id).first()
        if meal_plan:
            if meal_name is not None:
                meal_plan.meal_name = meal_name
            if calories is not None:
                meal_plan.calories = calories
            if date is not None:
                meal_plan.date = date
            session.commit()
            return meal_plan
        return None
    
    @classmethod
    def delete(cls, session, meal_plan_id):
        meal_plan = session.query(cls).filter_by(id=meal_plan_id).first()
        if meal_plan:
            session.delete(meal_plan)
            session.commit()
            return True
        return False
