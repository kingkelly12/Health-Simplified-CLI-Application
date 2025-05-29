from datetime import date
from sqlalchemy.orm import Session
from rich.console import Console
from models import FoodEntry, User

console = Console()

class FoodEntryController:
    def __init__(self, db: Session):
        self.db = db

    def add_entry(self, user_id: int, food: str, calories: int, entry_date: date = None):
        """Record a new food entry"""
        if not entry_date:
            entry_date = date.today()
            
        entry = FoodEntry(
            user_id=user_id,
            food=food,
            calories=calories,
            date=entry_date
        )
        self.db.add(entry)
        self.db.commit()
        return entry

    def get_entries(self, user_id: int, start_date: date, end_date: date = None):
        """Retrieve entries within date range"""
        if not end_date:
            end_date = start_date
            
        return self.db.query(FoodEntry).filter(
            FoodEntry.user_id == user_id,
            FoodEntry.date >= start_date,
            FoodEntry.date <= end_date
        ).order_by(FoodEntry.date).all()