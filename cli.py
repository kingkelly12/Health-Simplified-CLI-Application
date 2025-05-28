import typer
from typing import Optional
from datetime import date
from rich.console import Console
from database import SessionLocal
from models import User, FoodEntry, Goal

app = typer.Typer(help="Health Simplified CLI - Track your nutrition and meals")
console = Console()

@app.command()
def user_create(name: str):
    """Create a new user"""
    with SessionLocal() as db:
        user = User(name=name)
        db.add(user)
        db.commit()
        console.print(f"[green]✓ Created user: {name}[/green]")

@app.command()
def user_list():
    """List all users"""
    with SessionLocal() as db:
        users = db.query(User).all()
        if not users:
            console.print("[yellow]No users found[/yellow]")
            return
            
        console.print("[bold]Users:[/bold]")
        for user in users:
            console.print(f"- {user.name} (ID: {user.id})")

@app.command()
def entry_add(
    user_name: str = typer.Option(..., "--user", "-u", help="User name"),
    food: str = typer.Option(..., "--food", "-f", help="Food item name"),
    calories: int = typer.Option(..., "--calories", "-c", help="Calorie count"),
    entry_date: Optional[str] = typer.Option(None, "--date", "-d", help="Date (YYYY-MM-DD)")
):
    """Add a food entry"""
    with SessionLocal() as db:
        user = db.query(User).filter_by(name=user_name).first()
        if not user:
            console.print(f"[red]✗ User '{user_name}' not found[/red]")
            raise typer.Exit(1)
            
        date_obj = date.today() if not entry_date else date.fromisoformat(entry_date)
        entry = FoodEntry(
            food=food,
            calories=calories,
            date=date_obj,
            user_id=user.id
        )
        db.add(entry)
        db.commit()
        console.print(f"[green]✓ Added {food} ({calories} cal) for {user_name} on {date_obj}[/green]")

@app.command()
def entry_list(
    user_name: Optional[str] = typer.Option(None, "--user", "-u", help="Filter by user"),
    entry_date: Optional[str] = typer.Option(None, "--date", "-d", help="Filter by date (YYYY-MM-DD)")
):
    """List food entries"""
    with SessionLocal() as db:
        query = db.query(FoodEntry)
        
        if user_name:
            user = db.query(User).filter_by(name=user_name).first()
            if not user:
                console.print(f"[red]✗ User '{user_name}' not found[/red]")
                raise typer.Exit(1)
            query = query.filter_by(user_id=user.id)
            
        if entry_date:
            date_obj = date.fromisoformat(entry_date)
            query = query.filter_by(date=date_obj)
            
        entries = query.all()
        
        if not entries:
            console.print("[yellow]No entries found[/yellow]")
            return
            
        console.print("[bold]Food Entries:[/bold]")
        for entry in entries:
            user = db.query(User).get(entry.user_id)
            console.print(
                f"- ID: {entry.id}, {entry.food} ({entry.calories} cal) "
                f"for {user.name} on {entry.date}"
            )

@app.command()
def goal_set(
    user_name: str = typer.Option(..., "--user", "-u", help="User name"),
    daily: int = typer.Option(..., "--daily", help="Daily calorie goal"),
    weekly: int = typer.Option(..., "--weekly", help="Weekly calorie goal")
):
    """Set nutrition goals for a user"""
    with SessionLocal() as db:
        user = db.query(User).filter_by(name=user_name).first()
        if not user:
            console.print(f"[red]✗ User '{user_name}' not found[/red]")
            raise typer.Exit(1)
            
        goal = db.query(Goal).filter_by(user_id=user.id).first()
        if not goal:
            goal = Goal(user_id=user.id, daily_calories=daily, weekly_calories=weekly)
            db.add(goal)
        else:
            goal.daily_calories = daily
            goal.weekly_calories = weekly
            
        db.commit()
        console.print(
            f"[green]✓ Set goals for {user_name}: "
            f"{daily} daily / {weekly} weekly calories[/green]"
        )

@app.command()
def goal_list(user_name: str = typer.Option(..., "--user", "-u", help="User name")):
    """List user's goals"""
    with SessionLocal() as db:
        user = db.query(User).filter_by(name=user_name).first()
        if not user:
            console.print(f"[red]✗ User '{user_name}' not found[/red]")
            raise typer.Exit(1)
            
        goal = db.query(Goal).filter_by(user_id=user.id).first()
        if not goal:
            console.print(f"[yellow]No goals set for {user_name}[/yellow]")
            return
            
        console.print(f"[bold]Goals for {user_name}:[/bold]")
        console.print(f"- Daily: {goal.daily_calories} calories")
        console.print(f"- Weekly: {goal.weekly_calories} calories")

@app.command()
def report(
    user_name: str = typer.Option(..., "--user", "-u", help="User name"),
    report_date: str = typer.Option(..., "--date", "-d", help="Date (YYYY-MM-DD)")
):
    """Generate daily nutrition report"""
    with SessionLocal() as db:
        user = db.query(User).filter_by(name=user_name).first()
        if not user:
            console.print(f"[red]✗ User '{user_name}' not found[/red]")
            raise typer.Exit(1)
            
        date_obj = date.fromisoformat(report_date)
        entries = db.query(FoodEntry).filter_by(user_id=user.id, date=date_obj).all()
        goal = db.query(Goal).filter_by(user_id=user.id).first()
        
        total_calories = sum(entry.calories for entry in entries)
        
        console.print(f"[bold]Nutrition Report for {user_name} on {report_date}:[/bold]")
        console.print(f"- Total calories consumed: {total_calories}")
        
        if goal:
            console.print(f"- Daily goal: {goal.daily_calories}")
            percentage = (total_calories / goal.daily_calories) * 100
            status = "✓ Under" if percentage < 100 else "✗ Over"
            console.print(f"- Status: {status} goal ({percentage:.1f}%)")

if __name__ == "__main__":
    app()