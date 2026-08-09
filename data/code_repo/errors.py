"""Gestion des erreurs de l'application.

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
