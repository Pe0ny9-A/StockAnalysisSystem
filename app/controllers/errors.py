"""
股票系统 - 错误处理控制器
"""
from flask import render_template


def register_error_handlers(app):
    """注册错误处理器到应用"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        """404 - 页面未找到"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """403 - 权限不足"""
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        """500 - 服务器错误"""
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """400 - 错误请求"""
        return render_template('errors/400.html'), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        """401 - 未授权"""
        return render_template('errors/401.html'), 401 