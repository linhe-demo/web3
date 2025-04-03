from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix


class IPService:
    @staticmethod
    def get_ip_address():
        app = Flask(__name__)
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2)
        # 可能的代理头列表
        proxy_headers = [
            'X-Forwarded-For',
            'X-Real-IP',
            'CF-Connecting-IP'  # Cloudflare
        ]

        for header in proxy_headers:
            if header in request.headers:
                ips = request.headers[header].split(',')
                # 取第一个IP（可能是最原始的客户端IP）
                ip = ips[0].strip()
                if ip:
                    return ip

        # 如果没有代理头，使用remote_addr
        return request.remote_addr
