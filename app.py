from flask import Flask
from flask_cors import CORS
from api import create_routes


def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)

    # 启用CORS
    CORS(app)

    # 注册路由
    create_routes(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)