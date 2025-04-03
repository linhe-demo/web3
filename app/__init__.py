from flask import Flask
from config import config
from .extensions import db, redis_client, jwt, migrate


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    initialize_extensions(app)

    # 注册蓝图
    register_blueprints(app)

    # 初始化数据库
    with app.app_context():
        db.create_all()

    jwt.init_app(app)
    migrate.init_app(app, db)

    return app


def initialize_extensions(app):
    """初始化Flask扩展"""
    db.init_app(app)
    redis_client.init_app(app)


def register_blueprints(app):
    """注册所有蓝图"""
    from .blueprints.auth import auth_bp
    from .blueprints.api import api_bp
    from .blueprints.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')