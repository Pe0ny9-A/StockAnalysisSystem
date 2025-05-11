"""
投资组合模块控制器初始化文件
"""
from flask import Blueprint

# 创建蓝图
portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

# 导入视图
from app.controllers.portfolio import views 