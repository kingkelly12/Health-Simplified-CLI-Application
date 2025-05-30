from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User

def test_user_creation():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    user = User(name="test_user")
    db.add(user)
    db.commit()
    assert user.id is not None
    db.close()
