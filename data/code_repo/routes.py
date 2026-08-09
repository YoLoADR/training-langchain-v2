"""Routes de l'API Flask.

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
