from app.models.user import User
from app.extensions import db
from app.utils.jwt_utils import generate_tokens


class AuthService:
    @staticmethod
    def register(username, password, email):
        if User.query.filter_by(username=username).first():
            return None, "Username already exists"

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user, None

    @staticmethod
    def generate_tokens(user):
        access_token, refresh_token = generate_tokens(user)
        return access_token