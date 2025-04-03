from app.extensions import redis_client


class RedisService:
    @staticmethod
    def set(key, value, expire=None):
        client = redis_client.get_client()
        client.set(key, value, ex=expire)

    @staticmethod
    def get(key):
        client = redis_client.get_client()
        return client.get(key)

    @staticmethod
    def delete(key):
        client = redis_client.get_client()
        client.delete(key)

    @staticmethod
    def cache_response(key, data, expire=3600):
        """缓存API响应"""
        import json
        client = redis_client.get_client()
        client.setex(key, expire, json.dumps(data))

    @staticmethod
    def get_cached_response(key):
        """获取缓存的API响应"""
        import json
        client = redis_client.get_client()
        data = client.get(key)
        return json.loads(data) if data else None