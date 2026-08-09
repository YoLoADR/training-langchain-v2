"""Services metier de l'application.

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
