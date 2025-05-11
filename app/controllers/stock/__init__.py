"""
股票模块控制器初始化文件
"""
from flask import Blueprint

# 创建蓝图
stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

# 导入视图
from app.controllers.stock import views 