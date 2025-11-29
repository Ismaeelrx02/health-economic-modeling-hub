"""Database connection and session management"""
import os
from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

# Get database URL from environment variable or use SQLite as fallback
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///health_econ_hub.db')

# PostgreSQL connection string fix for SQLAlchemy 2.0
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Engine configuration based on database type
engine_kwargs = {
    'echo': os.getenv('SQL_ECHO', 'false').lower() == 'true',
    'future': True
}

if DATABASE_URL.startswith('postgresql://'):
    # PostgreSQL specific configuration
    engine_kwargs.update({
        'poolclass': pool.QueuePool,
        'pool_size': int(os.getenv('DB_POOL_SIZE', 5)),
        'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 10)),
        'pool_timeout': int(os.getenv('DB_POOL_TIMEOUT', 30)),
        'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600)),
        'pool_pre_ping': True,  # Verify connections before using
    })
elif DATABASE_URL.startswith('sqlite://'):
    # SQLite specific configuration
    engine_kwargs.update({
        'connect_args': {'check_same_thread': False}
    })

# Create engine
db_engine = create_engine(DATABASE_URL, **engine_kwargs)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Session = scoped_session(SessionLocal)


@contextmanager
def get_db_session():
    """
    Context manager for database sessions.
    Automatically handles commit/rollback and cleanup.
    
    Usage:
        with get_db_session() as session:
            # Your database operations
            result = session.query(Project).all()
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        session.close()


def init_db():
    """
    Initialize database - create all tables.
    Safe to call multiple times.
    """
    from .models import Base
    try:
        Base.metadata.create_all(bind=db_engine)
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def dispose_db():
    """
    Dispose of database engine and connections.
    Call this on application shutdown.
    """
    try:
        Session.remove()
        db_engine.dispose()
        logger.info("Database connections disposed")
    except Exception as e:
        logger.error(f"Error disposing database: {e}")


# For SQLite, enable foreign keys
if DATABASE_URL.startswith('sqlite://'):
    @event.listens_for(db_engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
