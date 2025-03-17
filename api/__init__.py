from flask import Blueprint
from .routes import register_routes


def create_routes(app):
    """为应用创建和注册路由"""
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    # 注册API路由
    register_routes(api_bp)

    # 将蓝图注册到应用
    app.register_blueprint(api_bp)