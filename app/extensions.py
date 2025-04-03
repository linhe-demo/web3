from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import redis
from redis import ConnectionPool
from flask_bcrypt import Bcrypt

# MySQL 扩展
db = SQLAlchemy()

jwt = JWTManager()

migrate = Migrate()

bcrypt = Bcrypt()


# Redis 扩展
class RedisClient:
    _pool = None
    _client = None

    @classmethod
    def init_app(cls, app):
        cls._pool = ConnectionPool(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            password=app.config['REDIS_PASSWORD'],
            db=app.config['REDIS_DB'],
            max_connections=20,
            decode_responses=True
        )
        cls._client = redis.Redis(connection_pool=cls._pool)

        try:
            cls._client.ping()
        except redis.RedisError as e:
            app.logger.error(f"Redis connection error: {e}")
            raise

    @classmethod
    def get_client(cls):
        if not cls._client:
            raise RuntimeError("Redis client not initialized")
        return cls._client


redis_client = RedisClient