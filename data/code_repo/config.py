"""Configuration centrale de l'application Flask.

Charge les variables d'environnement et expose les constantes.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration de l'application."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/app")
    JWT_EXPIRATION = int(os.getenv("JWT_EXPIRATION", "3600"))
    JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-change-me")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    API_RATE_LIMIT = int(os.getenv("API_RATE_LIMIT", "100"))
    PROJECT_ROOT = Path(__file__).resolve().parent
    UPLOAD_DIR = PROJECT_ROOT / "uploads"


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "")


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    DATABASE_URL = "sqlite:///test.db"


def get_config(env: str = "development") -> type[Config]:
    """Retourne la classe de configuration selon l'environnement."""
    configs = {
        "production": ProductionConfig,
        "development": DevelopmentConfig,
        "test": TestConfig,
    }
    return configs.get(env, DevelopmentConfig)
