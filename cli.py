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
    """Set nutrition goals"""
    user = db.query(User).filter_by(name=user_name).first()
    if not user:
        typer.echo(f"Error: User {user_name} not found", err=True)
        raise typer.Exit(1)
    goal = Goal(daily_calories=daily, weekly_calories=weekly, user_id=user.id)
    db.add(goal)
    db.commit()
    typer.echo(f"Set goals for {user_name}: {daily} daily, {weekly} weekly")

@app.command()
def report(user_name: str, report_date: str = str(date.today())):
    """Show daily report"""
    user = db.query(User).filter_by(name=user_name).first()
    if not user:
        typer.echo(f"Error: User {user_name} not found", err=True)
        raise typer.Exit(1)
    
    total = sum(e.calories for e in db.query(FoodEntry)
                .filter_by(user_id=user.id, date=report_date))
    typer.echo(f"Report for {user_name} on {report_date}:")
    typer.echo(f"Total calories: {total}")

if __name__ == "__main__":
    app()