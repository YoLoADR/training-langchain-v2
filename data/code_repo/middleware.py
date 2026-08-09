"""Middleware de l'application Flask.

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
