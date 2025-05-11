"""
股票系统 - 认证控制器
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse

from app import db
from app.models.user import User
from app.services.auth_service import validate_registration, validate_login

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    # 已登录用户重定向到首页
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # 处理登录表单提交
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        # 验证登录信息
        validation_result = validate_login(email, password)
        if validation_result['success']:
            user = validation_result['user']
            login_user(user, remember=remember)
            user.update_last_login()
            
            # 重定向到登录前尝试访问的页面，如果有的话
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash(validation_result['message'], 'danger')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    flash('您已成功登出', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    # 已登录用户重定向到首页
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # 处理注册表单提交
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # 验证注册信息
        validation_result = validate_registration(username, email, password, password_confirm)
        if validation_result['success']:
            # 创建新用户
            user = User(
                username=username,
                email=email,
                password=password  # User模型中会自动哈希处理
            )
            db.session.add(user)
            db.session.commit()
            
            flash('注册成功！请登录', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(validation_result['message'], 'danger')
    
    return render_template('auth/register.html')


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    """请求重置密码"""
    # 已登录用户重定向到首页
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # TODO: 实现密码重置请求逻辑
    
    return render_template('auth/reset_password_request.html') 