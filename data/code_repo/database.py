"""Gestion de la base de donnees.

Module d'abstraction pour les operations SQLAlchemy.
"""
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import Config


engine = create_engine(Config.DATABASE_URL, echo=Config.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db_session() -> Session:
    """Context manager pour une session de base de donnees.

    Usage:
        with get_db_session() as session:
            session.query(User).all()
    """
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """Cree toutes les tables definies dans les models."""
    from models import Base
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Supprime toutes les tables (pour les tests)."""
    from models import Base
    Base.metadata.drop_all(bind=engine)
