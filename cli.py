import typer
from datetime import date, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn
from database import SessionLocal
from models import User, FoodEntry, Goal

db = SessionLocal()
app = typer.Typer(rich_markup_mode="markdown")
console = Console()

@app.command()
def dashboard(username: str):
    """Show beautiful nutrition dashboard"""
    with SessionLocal() as db:
        user = db.query(User).filter_by(name=username).first()
        if not user:
            console.print(f"[red]Error: User '{username}' not found[/red]")
            raise typer.Exit(1)

        today = date.today()
        entries = db.query(FoodEntry).filter_by(
            user_id=user.id,
            date=today
        ).all()
        total_calories = sum(e.calories for e in entries)

        goal = db.query(Goal).filter_by(user_id=user.id).first()

        console.print(Panel.fit(
            f"[bold green] {username}'s Nutrition Dashboard[/]",
            subtitle=f" {today.strftime('%A, %B %d')}",
            border_style="blue"
        ))

        if goal:
            with Progress(
                BarColumn(bar_width=50),
                "[progress.percentage]{task.percentage:>3.0f}%",
                expand=True
            ) as progress:
                daily_task = progress.add_task(
                    f" [cyan]Daily:[/] {total_calories}/{goal.daily_calories} cal",
                    total=goal.daily_calories
                )
                progress.update(daily_task, completed=total_calories)

                weekly_entries = db.query(FoodEntry).filter(
                    FoodEntry.user_id == user.id,
                    FoodEntry.date >= today - timedelta(days=7)
                ).all()
                weekly_total = sum(e.calories for e in weekly_entries)
                
                weekly_task = progress.add_task(
                    f" [cyan]Weekly:[/] {weekly_total}/{goal.weekly_calories} cal",
                    total=goal.weekly_calories
                )
                progress.update(weekly_task, completed=weekly_total)

        if entries:
            table = Table(
                title="[bold]Today's Food Entries[/bold]",
                show_header=True,
                header_style="bold magenta",
                show_lines=True
            )
            table.add_column("Food", style="cyan")
            table.add_column("Calories", justify="right", style="green")
            
            for entry in entries:
                table.add_row(entry.food, str(entry.calories))
            
            table.add_row(
                "[bold]TOTAL[/bold]", 
                f"[bold]{total_calories}[/bold]"
            )
            console.print(table)
        else:
            console.print("[yellow]No food entries today[/yellow]")

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
    app(prog_name="health-cli")