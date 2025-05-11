"""
交易模块视图
"""
from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.controllers.trading import trading_bp
from app.services.trading_service import (
    execute_buy, execute_sell, get_user_transactions,
    get_transaction_detail, get_transaction_stats
)
from app.services.portfolio_service import get_portfolio_detail, get_default_portfolio


@trading_bp.route('/')
@login_required
def index():
    """交易首页"""
    return render_template('trading/index.html')


@trading_bp.route('/history')
@login_required
def history():
    """交易历史记录页面"""
    transactions = get_user_transactions(current_user.id)
    return render_template('trading/history.html', transactions=transactions)


@trading_bp.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    """买入股票页面"""
    if request.method == 'POST':
        portfolio_id = request.form.get('portfolio_id', type=int)
        stock_code = request.form.get('stock_code')
        quantity = request.form.get('quantity', type=int)
        price = request.form.get('price', type=float)
        commission = request.form.get('commission', 0, type=float)
        notes = request.form.get('notes', '')
        
        # 验证输入
        if not all([stock_code, quantity, price]):
            flash('请完整填写交易信息', 'error')
            return render_template('trading/buy.html')
            
        # 获取默认投资组合
        if not portfolio_id:
            portfolio = get_default_portfolio(current_user.id)
            if portfolio:
                portfolio_id = portfolio.id
        
        # 执行买入
        success, message, transaction = execute_buy(
            user_id=current_user.id,
            portfolio_id=portfolio_id,
            stock_code=stock_code,
            quantity=quantity,
            price=price,
            commission=commission,
            notes=notes
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('trading.history'))
        else:
            flash(message, 'error')
    
    # 获取用户的投资组合列表
    return render_template('trading/buy.html')


@trading_bp.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    """卖出股票页面"""
    if request.method == 'POST':
        portfolio_id = request.form.get('portfolio_id', type=int)
        stock_code = request.form.get('stock_code')
        quantity = request.form.get('quantity', type=int)
        price = request.form.get('price', type=float)
        commission = request.form.get('commission', 0, type=float)
        tax = request.form.get('tax', 0, type=float)
        notes = request.form.get('notes', '')
        
        # 验证输入
        if not all([portfolio_id, stock_code, quantity, price]):
            flash('请完整填写交易信息', 'error')
            return render_template('trading/sell.html')
        
        # 执行卖出
        success, message, transaction = execute_sell(
            user_id=current_user.id,
            portfolio_id=portfolio_id,
            stock_code=stock_code,
            quantity=quantity,
            price=price,
            commission=commission,
            tax=tax,
            notes=notes
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('trading.history'))
        else:
            flash(message, 'error')
    
    # 获取用户的投资组合列表
    return render_template('trading/sell.html')


@trading_bp.route('/stats')
@login_required
def stats():
    """交易统计页面"""
    period = request.args.get('period', 'all')
    portfolio_id = request.args.get('portfolio_id', type=int)
    
    stats_data = get_transaction_stats(
        user_id=current_user.id,
        portfolio_id=portfolio_id,
        period=period
    )
    
    return render_template('trading/stats.html', stats=stats_data)


# API接口

@trading_bp.route('/api/transactions')
@login_required
def api_get_transactions():
    """获取交易记录API"""
    portfolio_id = request.args.get('portfolio_id', type=int)
    stock_code = request.args.get('stock_code')
    limit = request.args.get('limit', 50, type=int)
    
    transactions = get_user_transactions(
        user_id=current_user.id,
        portfolio_id=portfolio_id,
        stock_code=stock_code,
        limit=limit
    )
    
    return jsonify({
        'status': 'success',
        'data': transactions
    })


@trading_bp.route('/api/transactions/<int:transaction_id>')
@login_required
def api_get_transaction(transaction_id):
    """获取单个交易详情API"""
    transaction = get_transaction_detail(transaction_id, current_user.id)
    if not transaction:
        return jsonify({
            'status': 'error',
            'message': '交易记录不存在或无权访问'
        }), 404
        
    return jsonify({
        'status': 'success',
        'data': transaction
    })


@trading_bp.route('/api/transactions/stats')
@login_required
def api_get_stats():
    """获取交易统计数据API"""
    period = request.args.get('period', 'all')
    portfolio_id = request.args.get('portfolio_id', type=int)
    
    stats_data = get_transaction_stats(
        user_id=current_user.id,
        portfolio_id=portfolio_id,
        period=period
    )
    
    return jsonify({
        'status': 'success',
        'data': stats_data
    })


@trading_bp.route('/api/transactions/buy', methods=['POST'])
@login_required
def api_execute_buy():
    """执行买入交易API"""
    data = request.get_json()
    if not data or not all(k in data for k in ['stock_code', 'quantity', 'price']):
        return jsonify({
            'status': 'error',
            'message': '请提供完整的交易信息'
        }), 400
    
    portfolio_id = data.get('portfolio_id')
    if not portfolio_id:
        # 使用默认投资组合
        portfolio = get_default_portfolio(current_user.id)
        if portfolio:
            portfolio_id = portfolio.id
    
    success, message, transaction = execute_buy(
        user_id=current_user.id,
        portfolio_id=portfolio_id,
        stock_code=data.get('stock_code'),
        quantity=data.get('quantity'),
        price=data.get('price'),
        commission=data.get('commission', 0),
        tax=data.get('tax', 0),
        notes=data.get('notes', '')
    )
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': message
        }), 400
    
    return jsonify({
        'status': 'success',
        'message': message,
        'data': {
            'transaction_id': transaction.id if transaction else None
        }
    }), 201


@trading_bp.route('/api/transactions/sell', methods=['POST'])
@login_required
def api_execute_sell():
    """执行卖出交易API"""
    data = request.get_json()
    if not data or not all(k in data for k in ['portfolio_id', 'stock_code', 'quantity', 'price']):
        return jsonify({
            'status': 'error',
            'message': '请提供完整的交易信息'
        }), 400
    
    success, message, transaction = execute_sell(
        user_id=current_user.id,
        portfolio_id=data.get('portfolio_id'),
        stock_code=data.get('stock_code'),
        quantity=data.get('quantity'),
        price=data.get('price'),
        commission=data.get('commission', 0),
        tax=data.get('tax', 0),
        notes=data.get('notes', '')
    )
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': message
        }), 400
    
    return jsonify({
        'status': 'success',
        'message': message,
        'data': {
            'transaction_id': transaction.id if transaction else None
        }
    }), 201