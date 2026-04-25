"""
SQLAlchemy database setup and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQLALCHEMY_ECHO,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session in FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
