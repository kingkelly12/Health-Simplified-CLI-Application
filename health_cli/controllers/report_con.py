from datetime import date, timedelta
from sqlalchemy.orm import Session
from rich.table import Table
from rich.console import Console
from models import FoodEntry, Goal

console = Console()

class ReportGenerator:
    def __init__(self, db: Session):
        self.db = db

    def daily_report(self, user_id: int, report_date: date):
        """Generate daily nutrition summary"""
        entries = self.db.query(FoodEntry).filter_by(
            user_id=user_id,
            date=report_date
        ).all()
        
        total = sum(entry.calories for entry in entries)
        goal = self.db.query(Goal).filter_by(user_id=user_id).first()
        
        return {
            "date": report_date,
            "total_calories": total,
            "goal": goal.daily_calories if goal else None,
            "entries": entries
        }

    def weekly_summary(self, user_id: int, start_date: date):
        """Generate weekly overview"""
        end_date = start_date + timedelta(days=6)
        entries = self.db.query(FoodEntry).filter(
            FoodEntry.user_id == user_id,
            FoodEntry.date >= start_date,
            FoodEntry.date <= end_date
        ).all()
        
        daily_totals = {}
        current_date = start_date
        while current_date <= end_date:
            daily_entries = [e for e in entries if e.date == current_date]
            daily_totals[current_date] = sum(e.calories for e in daily_entries)
            current_date += timedelta(days=1)
        
        return {
            "week_start": start_date,
            "week_end": end_date,
            "daily_totals": daily_totals,
            "weekly_total": sum(daily_totals.values())
        }