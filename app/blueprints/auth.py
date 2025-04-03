import os
from flask import Blueprint, jsonify, request, render_template, url_for
from app.services.auth_service import AuthService
from app.services.ip_service import IPService
from app.models.user import User
from app.extensions import db, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def default():
    return render_template('login/index.html')


@auth_bp.route('/login', methods=['POST'])
def login():
    # 获取请求参数
    params = request.get_json()
    if not params or 'username' not in params or 'password' not in params:
        return jsonify({
            "code": 400,
            "message": "用户名和密码不能为空",
            "data": None
        })
    # 查询用户
    user = User.query.filter_by(username=params.get('username')).first()
    if user is None:
        return jsonify({
            "code": 403,
            "message": "用户不存在",
            "data": None
        })

    # 验证密码（修正参数顺序和加盐方式）
    salted_password = os.getenv('LOGIN_KEY', '') + params.get('password')
    if not bcrypt.check_password_hash(user.password, salted_password):
        return jsonify({
            "code": 403,
            "message": "用户名或密码不正确",  # 避免提示太具体
            "data": None
        })

    try:
        # 生成token
        token = AuthService.generate_tokens(user)
        if not token:
            raise ValueError("生成token失败")

        # 更新登录信息
        client_ip = IPService.get_ip_address()
        User.update_ip(user, client_ip)
        return jsonify({
            "code": 200,
            "message": "登录成功",
            "data": {
                "token": token,
                "user_info": {
                    "username": user.username,
                    "last_login": user.last_login_date.isoformat() if user.last_login_date else None
                }
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "message": f"登录失败: {str(e)}",
            "data": None
        })