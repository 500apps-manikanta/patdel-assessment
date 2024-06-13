"""Database SQL connection"""

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from sqlalchemy.engine.url import URL


def get_engine():
    """Engine which will be used everywhere"""
    engine_url = URL.create(
        drivername="mysql+pymysql",
        username="root",
        password="root",
        host="localhost",
        database="fastapitest",
    )
    return create_engine(
        url=engine_url,
        connect_args={"ssl": {"ssl-mode": True}},
        pool_pre_ping=True,
        pool_use_lifo=True,
        pool_recycle=3600,
    )


engine = get_engine()


def create_db_tables():
    """Create all tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get Session"""
    with Session(engine) as session:
        yield session
