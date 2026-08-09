"""Point d'entree de l'application Flask.

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
