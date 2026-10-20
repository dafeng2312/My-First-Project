from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

# Define the local database URL (Creates a file named dataforge.db in your root)
DATABASE_URL = "sqlite:///dataforge.db"

# Create the core engine that talks to SQLite
engine = create_engine(DATABASE_URL, echo=False)

# Create a configured "Session" class to handle transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Creates all tables defined in models.py if they don't exist yet.
    This will be triggered by our setup script or main pipeline execution.
    """
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """
    Context manager helper / generator to yield safe database sessions.
    Ensures transactions are closed properly even if errors happen.
    """
    session = SessionLocal()
    try:
        return session
    except Exception:
        session.close()
        raise
