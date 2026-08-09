"""Fonctions utilitaires diverses.

Validation, formatting, helpers.
"""
import re
from datetime import datetime
from typing import Any


def validate_email(email: str) -> bool:
    """Valide le format d'un email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
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
