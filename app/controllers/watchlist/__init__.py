"""
观察列表模块蓝图
"""
from flask import Blueprint

# 创建观察列表蓝图
watchlist_bp = Blueprint('watchlist', __name__, url_prefix='/watchlist')

# 导入路由
from app.controllers.watchlist import views 