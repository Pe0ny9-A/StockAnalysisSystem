"""
交易模块蓝图
"""
from flask import Blueprint

# 创建交易蓝图
trading_bp = Blueprint('trading', __name__, url_prefix='/trading')

# 导入路由
from app.controllers.trading import views 