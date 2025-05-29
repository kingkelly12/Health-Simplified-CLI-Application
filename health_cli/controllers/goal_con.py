from sqlalchemy.orm import Session
from rich.console import Console
from models import Goal, User

console = Console()

class GoalController:
    def __init__(self, db: Session):
        self.db = db

    def set_goals(self, user_id: int, daily: int, weekly: int):
        """Create or update user goals"""
        goal = self.db.query(Goal).filter_by(user_id=user_id).first()
        
        if goal:
            goal.daily_calories = daily
            goal.weekly_calories = weekly
        else:
            goal = Goal(
                user_id=user_id,
                daily_calories=daily,
                weekly_calories=weekly
            )
            self.db.add(goal)
        
        self.db.commit()
        return goal

    def check_progress(self, user_id: int, current_calories: int):
        """Compare intake against goals"""
        goal = self.db.query(Goal).filter_by(user_id=user_id).first()
        if not goal:
            return None
        
        return {
            "daily": {
                "target": goal.daily_calories,
                "remaining": max(0, goal.daily_calories - current_calories)
            },
            "weekly": {
                "target": goal.weekly_calories,
                "remaining": max(0, goal.weekly_calories - current_calories)
            }
        }