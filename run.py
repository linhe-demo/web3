from flask_cors import CORS
from app import create_app

# 允许所有域名跨域访问（不推荐生产环境使用）
# CORS(app)

app = create_app()

CORS(app,
    origins=["http://localhost:5000"],  # 指定允许的域名
    methods=["GET", "POST", "PUT", "DELETE"],  # 允许的HTTP方法
    allow_headers=["Content-Type", "Authorization"],  # 允许的请求头
    expose_headers=["X-Custom-Header"],  # 暴露给前端的响应头
    supports_credentials=True  # 允许携带cookie
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)