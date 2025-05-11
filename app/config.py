"""
股票系统 - 配置文件
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(basedir), '.env'))


class Config:
    """基础配置类"""
    # 安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change-in-production'
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 上传文件配置
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # 股票数据API配置
    STOCK_API_KEY = os.environ.get('STOCK_API_KEY') or ''
    STOCK_API_URL = os.environ.get('STOCK_API_URL') or ''
    
    # AI模型配置
    AI_API_KEY = os.environ.get('AI_API_KEY') or ''
    AI_API_URL = os.environ.get('AI_API_URL') or ''
    AI_MODEL_NAME = os.environ.get('AI_MODEL_NAME') or 'wenxin'  # 默认使用百度文言一心
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or os.path.join(basedir, '..', 'logs', 'app.log')


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'dev.db')


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """生产环境配置"""
    # 生产环境必须设置SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        # 仅在FLASK_ENV确实为production时才报错
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError("Production config requires SECRET_KEY environment variable")
        else:
            SECRET_KEY = 'dev-secret-key-please-change-in-production'
        
    # 数据库配置，生产环境推荐使用MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://user:password@localhost/stock_system'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 