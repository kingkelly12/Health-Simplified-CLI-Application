import os
from pathlib import Path

# Database Configuration
DB_DIR = Path.home() / ".health_cli"
DB_DIR.mkdir(exist_ok=True, parents=True)

# Database Engine Configuration
DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()

if DB_ENGINE == "postgresql":
    DATABASE_URL = (
        f"postgresql://"
        f"{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'health_tracker')}"
    )
else:
    # Default to SQLite
    DB_FILE = DB_DIR / "health_tracker.db"
    DATABASE_URL = f"sqlite:///{DB_FILE}"

# SQLAlchemy-specific configuration
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))