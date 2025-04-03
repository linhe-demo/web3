from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import jwt

@jwt.user_identity_loader
def user_identity_lookup(user):
    return str(user.id)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    from app.models.user import User
    identity = jwt_data["sub"]
    return User.query.get(identity)

def generate_tokens(user):
    access_token = create_access_token(
        identity=user,
        additional_claims={"role": "user"}  # 可根据用户角色调整
    )
    refresh_token = create_refresh_token(identity=user)
    return access_token, refresh_token