import typer
from datetime import date
from .database import SessionLocal
from .models import User, FoodEntry, Goal

app = typer.Typer()
db = SessionLocal()

@app.command()
def user_create(name: str):
    """Create a new user"""
    user = User(name=name)
    db.add(user)
    db.commit()
    typer.echo(f"Created user: {name}")

@app.command()
def entry_add(user_name: str, food: str, calories: int, entry_date: str = str(date.today())):
    """Add food entry"""
    user = db.query(User).filter_by(name=user_name).first()
    if not user:
        typer.echo(f"Error: User {user_name} not found", err=True)
        raise typer.Exit(1)
    entry = FoodEntry(food=food, calories=calories, date=entry_date, user_id=user.id)
    db.add(entry)
    db.commit()
    typer.echo(f"Added {food} ({calories} cal) for {user_name}")

@app.command()
def goal_set(user_name: str, daily: int, weekly: int):
    """Set/update nutrition goals"""
    user = db.query(User).filter_by(name=user_name).first()
    if not user:
        typer.echo(f"Error: User {user_name} not found", err=True)
        raise typer.Exit(1)
    
    goal = db.query(Goal).filter_by(user_id=user.id).first()
    if goal:
        goal.daily_calories = daily
        goal.weekly_calories = weekly
    else:
        goal = Goal(daily_calories=daily, weekly_calories=weekly, user_id=user.id)
        db.add(goal)
    
    db.commit()
    typer.echo(f"Goals set for {user_name}: {daily} daily / {weekly} weekly calories")

@app.command()
def report(user_name: str, report_date: str = str(date.today())):
    """Generate daily nutrition report"""
    user = db.query(User).filter_by(name=user_name).first()
    if not user:
        typer.echo(f"Error: User {user_name} not found", err=True)
        raise typer.Exit(1)
    
    entries = db.query(FoodEntry).filter_by(user_id=user.id, date=report_date).all()
    goal = db.query(Goal).filter_by(user_id=user.id).first()
    
    total = sum(e.calories for e in entries)
    typer.echo(f"\nDaily Report for {user_name} ({report_date})")
    typer.echo(f"• Total calories: {total}")
    
    if goal:
        status = "Under" if total <= goal.daily_calories else f"Over by {total - goal.daily_calories}"
        typer.echo(f"• Daily goal: {goal.daily_calories} ({status})")
    
    if entries:
        typer.echo("\nFood Entries:")
        for entry in entries:
            typer.echo(f"- {entry.food}: {entry.calories} cal")
            
@app.command()
def meal_plan(user_name: str, week_start: str):
    """Generate simple weekly meal plan"""
    user = db.query(User).filter_by(name=user_name).first()
    if not user:
        typer.echo(f"Error: User {user_name} not found", err=True)
        raise typer.Exit(1)
    
    goal = db.query(Goal).filter_by(user_id=user.id).first()
    target = goal.daily_calories if goal else 2000
    
    typer.echo(f"\nWeekly Meal Plan for {user_name} (Week {week_start})")
    typer.echo(f"Daily target: ~{target} calories\n")
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days:
        typer.echo(f"{day}:")
        typer.echo("- Breakfast: [Add meal]")
        typer.echo("- Lunch: [Add meal]")
        typer.echo("- Dinner: [Add meal]")
        typer.echo(f"- Snacks: [Add snacks] (~{target//10} cal)\n")

if __name__ == "__main__":
    app()