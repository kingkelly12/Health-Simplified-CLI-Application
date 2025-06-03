from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from health_cli.models.foodentry import FoodEntry
from health_cli.models.goal import Goal
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    entries = relationship("FoodEntry", back_populates="user")
    goals = relationship("Goal", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    
    @classmethod    
    def create(cls, session, username):
        user = cls(username=username)
        session.add(user)
        session.commit()
        return user
    
    @classmethod
    def get_by_username(cls, session, username):
        return session.query(cls).filter_by(username=username).first()
    
    @classmethod
    def get_by_id(cls, session, user_id):
        return session.query(cls).filter_by(id=user_id).first()
    
    @classmethod
    def update(cls, session, user_id, username=None):
        user = session.query(cls).filter_by(id=user_id).first()
        if user:
            if username is not None:
                user.username = username
            session.commit()
            return user
        return None
    
    @classmethod
    def delete(cls, session, user_id):
        user = session.query(cls).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False