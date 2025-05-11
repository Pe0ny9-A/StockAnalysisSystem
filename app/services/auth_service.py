"""
股票系统 - 认证服务
"""
import re
from typing import Dict, Any

from app.models.user import User


def validate_registration(username: str, email: str, password: str, 
                         password_confirm: str) -> Dict[str, Any]:
    """
    验证用户注册信息
    
    Args:
        username: 用户名
        email: 电子邮箱
        password: 密码
        password_confirm: 确认密码
    
    Returns:
        Dict: 包含验证结果和消息的字典
    """
    # 验证字段非空
    if not all([username, email, password, password_confirm]):
        return {'success': False, 'message': '所有字段都是必填的'}
    
    # 验证用户名格式
    if not re.match(r'^[a-zA-Z0-9_-]{3,20}$', username):
        return {'success': False, 'message': '用户名只能包含字母、数字、下划线和连字符，长度为3-20个字符'}
    
    # 验证用户名是否存在
    if User.query.filter_by(username=username).first():
        return {'success': False, 'message': '该用户名已被使用'}
    
    # 验证邮箱格式
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return {'success': False, 'message': '请输入有效的电子邮箱地址'}
    
    # 验证邮箱是否存在
    if User.query.filter_by(email=email).first():
        return {'success': False, 'message': '该邮箱已被注册'}
    
    # 验证密码长度
    if len(password) < 8:
        return {'success': False, 'message': '密码长度必须至少为8个字符'}
    
    # 验证密码复杂度
    if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
        return {'success': False, 'message': '密码必须包含大写字母、小写字母和数字'}
    
    # 验证两次密码输入是否一致
    if password != password_confirm:
        return {'success': False, 'message': '两次输入的密码不一致'}
    
    # 所有验证通过
    return {'success': True, 'message': '验证通过'}


def validate_login(email: str, password: str) -> Dict[str, Any]:
    """
    验证用户登录信息
    
    Args:
        email: 电子邮箱
        password: 密码
    
    Returns:
        Dict: 包含验证结果、消息和用户对象的字典
    """
    # 验证字段非空
    if not all([email, password]):
        return {'success': False, 'message': '请输入邮箱和密码'}
    
    # 查找用户
    user = User.query.filter_by(email=email).first()
    if not user:
        return {'success': False, 'message': '邮箱或密码错误'}
    
    # 验证密码
    if not user.check_password(password):
        return {'success': False, 'message': '邮箱或密码错误'}
    
    # 验证用户是否被禁用
    if not user.is_active:
        return {'success': False, 'message': '该账户已被禁用，请联系管理员'}
    
    # 验证通过
    return {'success': True, 'message': '登录成功', 'user': user} 