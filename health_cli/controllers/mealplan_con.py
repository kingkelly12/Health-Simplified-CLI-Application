from datetime import date, timedelta
from sqlalchemy.orm import Session
from rich.table import Table
from rich.console import Console
from models import MealPlan, User

console = Console()

class MealPlanController:
    def __init__(self, db: Session):
        self.db = db

    def create_plan(self, user_id: int, start_date: date, days: int = 7):
        """Generate a weekly meal plan template"""
        existing = self.db.query(MealPlan).filter_by(
            user_id=user_id, 
            start_date=start_date
        ).first()
        
        if existing:
            console.print("[yellow]Plan already exists for this week[/yellow]")
            return existing

        plan = MealPlan(
            user_id=user_id,
            start_date=start_date,
            end_date=start_date + timedelta(days=days-1)
        )
        self.db.add(plan)
        self.db.commit()
        return plan

    def display_plan(self, user_id: int, week_start: date):
        """Render meal plan in a table"""
        plan = self.db.query(MealPlan).filter_by(
            user_id=user_id,
            start_date=week_start
        ).first()

        if not plan:
            console.print("[red]No plan found for this week[/red]")
            return

        table = Table(title=f"Meal Plan {week_start} to {plan.end_date}")
        table.add_column("Day")
        table.add_column("Breakfast")
        table.add_column("Lunch")
        table.add_column("Dinner")
        
        current_date = week_start
        while current_date <= plan.end_date:
            meals = plan.meals.get(current_date, {})
            table.add_row(
                current_date.strftime("%A"),
                meals.get("breakfast", "-"),
                meals.get("lunch", "-"),
                meals.get("dinner", "-")
            )
            current_date += timedelta(days=1)
        
        console.print(table)