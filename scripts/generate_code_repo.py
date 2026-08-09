#!/usr/bin/env python3
"""Générateur d'un mini-repo Python pour le Code-Reviewer (AT05) de ai-hirekit.

US-DATA-06 — Génère 10 fichiers Python formant un mini-repo FastAPI réaliste.
Le Code-Reviewer (AT05) indexera ce repo comme corpus RAG pour répondre à des
questions comme "Ou est geree l'authentification ?" ou "Que fait la fonction X ?".

Usage:
    python scripts/generate_code_repo.py [--output data/code_repo]

Le script est idempotent (relance = ecrase).
"""

from __future__ import annotations

import argparse
from pathlib import Path

FILES = {}

# ─── 1. config.py ───────────────────────────────────────────────────────────

FILES["config.py"] = '''"""Configuration centrale de l'application Flask.

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
'''

# ─── 2. database.py ──────────────────────────────────────────────────────────

FILES["database.py"] = '''"""Gestion de la base de donnees.

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
'''

# ─── 3. models.py ────────────────────────────────────────────────────────────

FILES["models.py"] = '''"""Modeles SQLAlchemy de l'application.

Definit les entites User, Post et Comment.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """Utilisateur de l'application."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
        }


class Post(Base):
    """Article publie par un utilisateur."""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content[:200],
            "author_id": self.author_id,
            "published": self.published,
        }


class Comment(Base):
    """Commentaire sur un post."""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
'''

# ─── 4. auth.py ──────────────────────────────────────────────────────────────

FILES["auth.py"] = '''"""Authentification et autorisation.

Gestion des JWT, hashing des mots de passe et verification des permissions.
"""
import hashlib
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

from config import Config


def hash_password(password: str) -> str:
    """Hash un mot de passe avec SHA-256 + salt."""
    salt = Config.SECRET_KEY
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verifie qu'un mot de passe correspond au hash."""
    return hash_password(password) == password_hash


def generate_jwt_token(user_id: int) -> str:
    """Genere un token JWT pour un utilisateur."""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=Config.JWT_EXPIRATION),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")


def decode_jwt_token(token: str) -> dict | None:
    """Decode et verifie un token JWT. Retourne le payload ou None."""
    try:
        return jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def require_auth(f):
    """Decorateur: exige un token JWT valide dans le header Authorization."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token manquant"}), 401
        payload = decode_jwt_token(token)
        if payload is None:
            return jsonify({"error": "Token invalide ou expire"}), 401
        request.current_user_id = payload["user_id"]
        return f(*args, **kwargs)
    return decorated


def require_admin(f):
    """Decorateur: exige que l'utilisateur soit administrateur."""
    @wraps(f)
    @require_auth
    def decorated(*args, **kwargs):
        from database import get_db_session
        from models import User
        with get_db_session() as session:
            user = session.query(User).get(request.current_user_id)
            if not user or not user.is_admin:
                return jsonify({"error": "Acces refuse"}), 403
        return f(*args, **kwargs)
    return decorated
'''

# ─── 5. routes.py ────────────────────────────────────────────────────────────

FILES["routes.py"] = '''"""Routes de l'API Flask.

Endpoints CRUD pour les posts, commentaires et utilisateurs.
"""
from flask import Blueprint, request, jsonify

from auth import require_auth, require_admin
from database import get_db_session
from models import User, Post, Comment
from errors import NotFoundError, ValidationError, handle_error

bp = Blueprint("routes", __name__)


@bp.route("/health", methods=["GET"])
def health_check():
    """Endpoint de health check pour le monitoring."""
    return jsonify({"status": "ok", "service": "blog-api"})


@bp.route("/posts", methods=["GET"])
def list_posts():
    """Liste tous les posts publies."""
    with get_db_session() as session:
        posts = session.query(Post).filter_by(published=True).all()
        return jsonify([p.to_dict() for p in posts])


@bp.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id: int):
    """Recupere un post par son ID."""
    with get_db_session() as session:
        post = session.query(Post).get(post_id)
        if not post:
            raise NotFoundError("Post non trouve")
        return jsonify(post.to_dict())


@bp.route("/posts", methods=["POST"])
@require_auth
def create_post():
    """Cree un nouveau post (authentifie)."""
    data = request.get_json()
    if not data or "title" not in data or "content" not in data:
        raise ValidationError("title et content requis")
    with get_db_session() as session:
        post = Post(
            title=data["title"],
            content=data["content"],
            author_id=request.current_user_id,
            published=data.get("published", False),
        )
        session.add(post)
        session.commit()
        return jsonify(post.to_dict()), 201


@bp.route("/posts/<int:post_id>/comments", methods=["POST"])
@require_auth
def add_comment(post_id: int):
    """Ajoute un commentaire a un post."""
    data = request.get_json()
    if not data or "content" not in data:
        raise ValidationError("content requis")
    with get_db_session() as session:
        post = session.query(Post).get(post_id)
        if not post:
            raise NotFoundError("Post non trouve")
        comment = Comment(
            content=data["content"],
            post_id=post_id,
            author_id=request.current_user_id,
        )
        session.add(comment)
        session.commit()
        return jsonify({"id": comment.id, "content": comment.content}), 201


@bp.route("/users/<int:user_id>", methods=["DELETE"])
@require_admin
def delete_user(user_id: int):
    """Supprime un utilisateur (admin uniquement)."""
    with get_db_session() as session:
        user = session.query(User).get(user_id)
        if not user:
            raise NotFoundError("Utilisateur non trouve")
        session.delete(user)
        session.commit()
        return jsonify({"message": "Utilisateur supprime"}), 200
'''

# ─── 6. services.py ──────────────────────────────────────────────────────────

FILES["services.py"] = '''"""Services metier de l'application.

Logique metier qui n'est pas dans les routes ni les models.
"""
from datetime import datetime
from database import get_db_session
from models import User, Post, Comment


class UserService:
    """Services lis aux utilisateurs."""

    @staticmethod
    def register_user(email: str, username: str, password: str) -> User:
        """Cree un nouvel utilisateur."""
        from auth import hash_password
        with get_db_session() as session:
            if session.query(User).filter_by(email=email).first():
                raise ValueError("Email deja utilise")
            user = User(
                email=email,
                username=username,
                password_hash=hash_password(password),
            )
            session.add(user)
            session.commit()
            return user

    @staticmethod
    def authenticate(email: str, password: str) -> str | None:
        """Authentifie un utilisateur et retourne un token JWT."""
        from auth import verify_password, generate_jwt_token
        with get_db_session() as session:
            user = session.query(User).filter_by(email=email).first()
            if user and verify_password(password, user.password_hash):
                return generate_jwt_token(user.id)
            return None

    @staticmethod
    def get_user_stats(user_id: int) -> dict:
        """Retourne les statistiques d'un utilisateur."""
        with get_db_session() as session:
            user = session.query(User).get(user_id)
            if not user:
                raise ValueError("Utilisateur non trouve")
            return {
                "posts_count": len(user.posts),
                "comments_count": len(user.comments),
                "member_since": user.created_at.isoformat(),
            }


class PostService:
    """Services lis aux posts."""

    @staticmethod
    def search_posts(query: str, limit: int = 10) -> list[Post]:
        """Recherche des posts par titre ou contenu."""
        with get_db_session() as session:
            return (
                session.query(Post)
                .filter(Post.title.ilike(f"%{query}%") | Post.content.ilike(f"%{query}%"))
                .limit(limit)
                .all()
            )

    @staticmethod
    def get_recent_posts(days: int = 7, limit: int = 20) -> list[Post]:
        """Retourne les posts recents."""
        since = datetime.utcnow().timestamp() - days * 86400
        with get_db_session() as session:
            return (
                session.query(Post)
                .filter(Post.created_at >= datetime.fromtimestamp(since))
                .order_by(Post.created_at.desc())
                .limit(limit)
                .all()
            )
'''

# ─── 7. middleware.py ───────────────────────────────────────────────────────

FILES["middleware.py"] = '''"""Middleware de l'application Flask.

Rate limiting, logging des requetes, gestion CORS.
"""
import time
from collections import defaultdict
from functools import wraps
from flask import request, g, jsonify

from config import Config


# Rate limiting en memoire (pour demo; en prod: Redis)
_request_counts: dict[str, list[float]] = defaultdict(list)


def rate_limit(f):
    """Limite le nombre de requetes par IP et par fenetre de temps."""
    @wraps(f)
    def decorated(*args, **kwargs):
        ip = request.remote_addr
        now = time.time()
        window = 60  # 1 minute
        max_requests = Config.API_RATE_LIMIT

        # Nettoyer les anciens timestamps
        _request_counts[ip] = [t for t in _request_counts[ip] if t > now - window]
        if len(_request_counts[ip]) >= max_requests:
            return jsonify({"error": "Trop de requetes"}), 429

        _request_counts[ip].append(now)
        return f(*args, **kwargs)
    return decorated


def request_logger(f):
    """Log chaque requete avec methode, path et duree."""
    @wraps(f)
    def decorated(*args, **kwargs):
        g.start_time = time.time()
        response = f(*args, **kwargs)
        duration = time.time() - g.start_time
        print(f"[{request.method}] {request.path} - {response[1] if isinstance(response, tuple) else 200} ({duration:.3f}s)")
        return response
    return decorated


def setup_cors(app):
    """Configure les headers CORS pour l'application."""
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
'''

# ─── 8. errors.py ────────────────────────────────────────────────────────────

FILES["errors.py"] = '''"""Gestion des erreurs de l'application.

Exceptions personnalisees et handler Flask.
"""
from flask import jsonify


class AppError(Exception):
    """Erreur de base de l'application."""
    status_code = 500
    message = "Erreur interne du serveur"

    def __init__(self, message: str | None = None, status_code: int | None = None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppError):
    """Ressource non trouvee (404)."""
    status_code = 404
    message = "Ressource non trouvee"


class ValidationError(AppError):
    """Erreur de validation (400)."""
    status_code = 400
    message = "Donnees invalides"


class UnauthorizedError(AppError):
    """Acces non autorise (401)."""
    status_code = 401
    message = "Non autorise"


class ForbiddenError(AppError):
    """Acces interdit (403)."""
    status_code = 403
    message = "Acces refuse"


def handle_error(error: AppError):
    """Handler Flask pour les erreurs AppError."""
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response


def register_error_handlers(app):
    """Enregistre les handlers d'erreur sur l'app Flask."""
    app.register_error_handler(NotFoundError, handle_error)
    app.register_error_handler(ValidationError, handle_error)
    app.register_error_handler(UnauthorizedError, handle_error)
    app.register_error_handler(ForbiddenError, handle_error)
    app.register_error_handler(AppError, handle_error)
'''

# ─── 9. utils.py ─────────────────────────────────────────────────────────────

FILES["utils.py"] = '''"""Fonctions utilitaires diverses.

Validation, formatting, helpers.
"""
import re
from datetime import datetime
from typing import Any


def validate_email(email: str) -> bool:
    """Valide le format d'un email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username: str) -> bool:
    """Valide un nom d'utilisateur (3-20 caracteres, alphanumerique + _)."""
    if len(username) < 3 or len(username) > 20:
        return False
    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None


def sanitize_input(text: str, max_length: int = 10000) -> str:
    """Nettoie une entree utilisateur (retire les caracteres dangereux)."""
    text = text.strip()
    if len(text) > max_length:
        text = text[:max_length]
    text = text.replace("<script>", "").replace("</script>", "")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text


def format_date(date: datetime, format_str: str = "%d/%m/%Y") -> str:
    """Formate une date pour l'affichage."""
    return date.strftime(format_str)


def paginate(items: list[Any], page: int = 1, per_page: int = 20) -> dict:
    """Pagine une liste d'items."""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page,
    }


def slugify(text: str) -> str:
    """Convertit un texte en slug URL-safe."""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text
'''

# ─── 10. main.py ─────────────────────────────────────────────────────────────

FILES["main.py"] = '''"""Point d'entree de l'application Flask.

Assemble les composants et demarre le serveur.
"""
from flask import Flask

from config import get_config
from database import init_db
from routes import bp as routes_bp
from middleware import setup_cors, rate_limit, request_logger
from errors import register_error_handlers


def create_app(env: str = "development") -> Flask:
    """Factory: cree et configure l'application Flask."""
    config_class = get_config(env)
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation
    setup_cors(app)
    register_error_handlers(app)
    init_db()

    # Enregistrement des blueprints
    app.register_blueprint(routes_bp)

    # Middleware global
    app.before_request(request_logger)

    # Route de health check protegee par rate limiting
    @app.route("/api/health")
    @rate_limit
    def api_health():
        return {"status": "ok", "version": "1.0.0"}

    return app


if __name__ == "__main__":
    app = create_app("development")
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
'''


def generate_code_repo(output_dir: Path) -> list[str]:
    """Genere les 10 fichiers Python dans output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)

    created = []
    for filename, content in FILES.items():
        file_path = output_dir / filename
        file_path.write_text(content, encoding="utf-8")
        created.append(filename)

    return created


def main():
    parser = argparse.ArgumentParser(description="Genere un mini-repo Python pour ai-hirekit")
    parser.add_argument("--output", default="data/code_repo", help="Dossier de sortie")
    args = parser.parse_args()

    output_dir = Path(args.output)
    print(f"Generation du mini-repo Python dans {output_dir}/ ...")

    created = generate_code_repo(output_dir)

    print(f"  OK: {len(created)} fichiers .py generes")
    for f in created:
        print(f"    - {f}")
    print(f"\nTotal: {len(created)} fichiers generes avec succes.")


if __name__ == "__main__":
    main()