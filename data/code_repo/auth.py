"""Authentification et autorisation.

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
