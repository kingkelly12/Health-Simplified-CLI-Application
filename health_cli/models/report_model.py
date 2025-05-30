from datetime import date
from sqlalchemy.orm import Session
from rich.table import Table
from .models import FoodEntry, Goal

class NutritionReporter:
    """Minimal nutrition report generator"""
    
    @classmethod
    def daily_report(cls, db: Session, user_id: int, day: date):
        """Generate daily report data"""
        entries = db.query(FoodEntry).filter_by(user_id=user_id, date=day).all()
        goal = db.query(Goal).filter_by(user_id=user_id).first()
        return {
            'date': day,
            'calories': sum(e.calories for e in entries),
            'goal': goal.daily_calories if goal else None,
            'entries': entries
        }

    @classmethod
    def show_report(cls, data: dict):
        """Display basic report table"""
        table = Table(title=f"Nutrition Report - {data['date']}")
        table.add_column("Food"), table.add_column("Calories", justify="right")
        for entry in data['entries']:
            table.add_row(entry.food, str(entry.calories))
        table.add_row("TOTAL", str(data['calories']), style="bold")
        if data['goal']:
            table.add_row("GOAL", str(data['goal']), style="blue")
        return table