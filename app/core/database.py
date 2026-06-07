from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Generator


from app.core.config import settings
from app.utils.logger import logger


class Base(DeclarativeBase):
    pass

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=300
)

logger.info("Database Engine Created")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def check_database_connection() -> None:

    try:

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Database Connected Successfully")

    except Exception as ex:
        logger.exception(f"Database Connection Failed: {str(ex)}")
        raise

    