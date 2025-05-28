from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from health_cli.models.foodentry import FoodEntry
from sqlalchemy.orm import sessionmaker
from health_cli.models.user import User

Base = declarative_base()

class FoodEntry(Base):
    __tablename__ = 'food_entries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    food_name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    user = relationship("User", back_populates="entries")
    
    def __repr__(self):
        return f"<FoodEntry(id={self.id}, user_id={self.user_id}, food_name='{self.food_name}', calories={self.calories}, date={self.date})>"
    
    @classmethod
    def create(cls, session, user_id, food_name, calories, date):
        food_entry = cls(user_id=user_id, food_name=food_name, calories=calories, date=date)
        session.add(food_entry)
        session.commit()
        return food_entry
    
    @classmethod
    def get_by_user(cls, session, user_id):
        return session.query(cls).filter_by(user_id=user_id).all()
    
    @classmethod
    def get_by_date(cls, session, user_id, date):
        return session.query(cls).filter_by(user_id=user_id, date=date).all()
    
    @classmethod
    def update(cls, session, food_entry_id, food_name=None, calories=None, date=None):
        food_entry = session.query(cls).filter_by(id=food_entry_id).first()
        if food_entry:
            if food_name is not None:
                food_entry.food_name = food_name
            if calories is not None:
                food_entry.calories = calories
            if date is not None:
                food_entry.date = date
            session.commit()
            return food_entry
        return None
    
    @classmethod
    def delete(cls, session, food_entry_id):
        food_entry = session.query(cls).filter_by(id=food_entry_id).first()
        if food_entry:
            session.delete(food_entry)
            session.commit()
            return True
        return False