from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
print("DATABASE URL:", settings.DATABASE_URL)
print("ENGINE:", engine.url)

def ensure_meetings_schema():
    """Add lightweight columns for existing SQLite installations."""
    inspector = inspect(engine)
    if "meetings" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("meetings")}
    if "pinned" not in columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE meetings ADD COLUMN pinned BOOLEAN NOT NULL DEFAULT 0"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
