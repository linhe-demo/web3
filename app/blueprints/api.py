from flask import Blueprint, jsonify
from app.services.redis_service import RedisService
from app.models.user import User

api_bp = Blueprint('api', __name__)


@api_bp.route('/user/<username>')
def get_user(username):
    # 先尝试从Redis缓存获取
    cache_key = f'user:{username}'
    cached_data = RedisService.get_cached_response(cache_key)
    if cached_data:
        return jsonify(cached_data)

    # 缓存未命中，查询数据库
    user = User.query.filter_by(username=username).first_or_404()
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email
    }

    # 缓存结果
    RedisService.cache_response(cache_key, user_data)

    return jsonify(user_data)