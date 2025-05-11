"""
AI分析模块控制器初始化文件
"""
from flask import Blueprint

# 创建蓝图
ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

# 导入视图
from app.controllers.ai_controller import views 