"""
股票系统 - 主页控制器
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.portfolio import Portfolio
from app.models.trade import Trade
from app.models.user import User
from app import db
from sqlalchemy import func
import datetime

# 创建主页蓝图
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首页"""
    return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """用户仪表盘"""
    # 获取用户投资组合
    portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
    
    # 处理投资组合数据
    for portfolio in portfolios:
        # 计算投资组合总资产和收益
        portfolio.total_assets = format(portfolio.calculate_total_assets(), '.2f')
        
        # 收益率
        change_rate = portfolio.calculate_change_rate()
        portfolio.change_rate = f"{change_rate:.2f}%" if change_rate else "0.00%"
        portfolio.status = "up" if change_rate and change_rate > 0 else "down"
        
        # 获取持仓数量
        portfolio.stock_count = portfolio.get_stock_count()
    
    # 获取最近的交易记录（最多5条）
    recent_trades = Trade.query.filter_by(user_id=current_user.id).order_by(Trade.trade_date.desc()).limit(5).all()
    
    # 处理交易记录数据
    for trade in recent_trades:
        trade.trade_date = trade.trade_date.strftime('%Y-%m-%d')
        trade.price = format(trade.price, '.2f')
    
    # 获取用户资产概览
    # 计算总资产
    total_assets = 0
    available_cash = current_user.balance if current_user.balance else 0
    
    # 计算今日盈亏和总收益
    today_profit = 0
    total_profit = 0
    
    # 总资产变化率
    total_change = 0
    total_change_class = ""
    
    # 总收益率
    total_profit_rate = 0
    total_profit_class = ""
    total_profit_change_class = ""
    
    # 如果有投资组合，计算相关数据
    if portfolios:
        # 计算总资产
        total_assets = sum(float(portfolio.total_assets) for portfolio in portfolios)
        
        # 向数据模板传递计算结果
        total_assets = format(total_assets + available_cash, '.2f')
        available_cash = format(available_cash, '.2f')
        
        # 假设数据：今日盈亏和总收益
        # 实际项目中应该从数据库获取或计算
        today_profit = "125.36"
        today_profit_class = "price-up"
        
        total_profit = "1265.78"
        total_profit_class = "price-up"
        total_profit_rate = "8.72%"
        total_profit_change_class = "price-up"
        
        total_change = "1.32%"
        total_change_class = "price-up"
    else:
        total_assets = format(available_cash, '.2f')
        available_cash = format(available_cash, '.2f')
    
    return render_template('dashboard/index.html',
                         portfolios=portfolios,
                         recent_trades=recent_trades,
                         total_assets=total_assets,
                         available_cash=available_cash,
                         today_profit=today_profit,
                         today_profit_class=today_profit_class,
                         total_profit=total_profit,
                         total_profit_class=total_profit_class,
                         total_profit_rate=total_profit_rate,
                         total_profit_change_class=total_profit_change_class,
                         total_change=total_change,
                         total_change_class=total_change_class)


@main_bp.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')


@main_bp.route('/help')
def help_page():
    """帮助页面"""
    return render_template('help.html') 