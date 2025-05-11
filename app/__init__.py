"""
股票系统 - Flask应用初始化
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect
from datetime import datetime

from app.config import Config

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
socketio = SocketIO()

def create_app(config_class=Config):
    """创建并配置Flask应用实例"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)

    # 设置登录视图
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录以访问该页面'
    login_manager.login_message_category = 'info'

    # 添加全局上下文处理器，提供now变量给模板
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}

    # 注册蓝图
    from app.controllers.auth import auth_bp
    from app.controllers.main import main_bp
    from app.controllers.stock import stock_bp
    from app.controllers.portfolio import portfolio_bp
    from app.controllers.trading import trading_bp
    from app.controllers.ai_controller import ai_bp
    from app.controllers.watchlist import watchlist_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(trading_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(watchlist_bp)

    # 注册错误处理器
    from app.controllers.errors import register_error_handlers
    register_error_handlers(app)

    return app


from app import models  # 导入模型，确保被识别 