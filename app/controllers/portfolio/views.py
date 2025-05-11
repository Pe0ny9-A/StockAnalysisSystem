"""
投资组合模块视图
"""
from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.controllers.portfolio import portfolio_bp
from app.services.portfolio_service import (
    get_user_portfolios, get_portfolio_detail, create_portfolio,
    update_portfolio, delete_portfolio, add_holding, update_holding,
    delete_holding, get_default_portfolio
)

# 视图路由

@portfolio_bp.route('/')
@login_required
def index():
    """投资组合列表页面"""
    return render_template('portfolio/index.html')


@portfolio_bp.route('/detail/<int:portfolio_id>')
@login_required
def detail(portfolio_id):
    """投资组合详情页面"""
    portfolio = get_portfolio_detail(portfolio_id, current_user.id)
    if not portfolio:
        flash('投资组合不存在或无权访问', 'error')
        return redirect(url_for('portfolio.index'))
    return render_template('portfolio/detail.html', portfolio=portfolio)


@portfolio_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """创建投资组合页面"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        is_default = request.form.get('is_default') == 'on'
        
        if not name:
            flash('请输入投资组合名称', 'error')
            return render_template('portfolio/create.html')
            
        portfolio = create_portfolio(
            user_id=current_user.id,
            name=name,
            description=description,
            is_default=is_default
        )
        
        if portfolio:
            flash('投资组合创建成功', 'success')
            return redirect(url_for('portfolio.detail', portfolio_id=portfolio.id))
        else:
            flash('投资组合创建失败', 'error')
            
    return render_template('portfolio/create.html')


# API接口

@portfolio_bp.route('/api/portfolios')
@login_required
def api_get_portfolios():
    """获取用户投资组合列表API"""
    portfolios = get_user_portfolios(current_user.id)
    return jsonify({
        'status': 'success',
        'data': portfolios
    })


@portfolio_bp.route('/api/portfolios/<int:portfolio_id>')
@login_required
def api_get_portfolio(portfolio_id):
    """获取单个投资组合详情API"""
    portfolio = get_portfolio_detail(portfolio_id, current_user.id)
    if not portfolio:
        return jsonify({
            'status': 'error',
            'message': '投资组合不存在或无权访问'
        }), 404
        
    return jsonify({
        'status': 'success',
        'data': portfolio
    })


@portfolio_bp.route('/api/portfolios', methods=['POST'])
@login_required
def api_create_portfolio():
    """创建投资组合API"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({
            'status': 'error',
            'message': '请提供投资组合名称'
        }), 400
        
    portfolio = create_portfolio(
        user_id=current_user.id,
        name=data.get('name'),
        description=data.get('description', ''),
        is_default=data.get('is_default', False)
    )
    
    if not portfolio:
        return jsonify({
            'status': 'error',
            'message': '投资组合创建失败'
        }), 500
        
    return jsonify({
        'status': 'success',
        'message': '投资组合创建成功',
        'data': {
            'id': portfolio.id,
            'name': portfolio.name
        }
    }), 201


@portfolio_bp.route('/api/portfolios/<int:portfolio_id>', methods=['PUT'])
@login_required
def api_update_portfolio(portfolio_id):
    """更新投资组合API"""
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'message': '请提供更新数据'
        }), 400
        
    success, message = update_portfolio(
        portfolio_id=portfolio_id,
        user_id=current_user.id,
        name=data.get('name'),
        description=data.get('description'),
        is_default=data.get('is_default')
    )
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': message
        }), 400
        
    return jsonify({
        'status': 'success',
        'message': message
    })


@portfolio_bp.route('/api/portfolios/<int:portfolio_id>', methods=['DELETE'])
@login_required
def api_delete_portfolio(portfolio_id):
    """删除投资组合API"""
    success, message = delete_portfolio(portfolio_id, current_user.id)
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': message
        }), 400
        
    return jsonify({
        'status': 'success',
        'message': message
    })


@portfolio_bp.route('/api/portfolios/<int:portfolio_id>/holdings', methods=['POST'])
@login_required
def api_add_holding(portfolio_id):
    """添加持仓API"""
    data = request.get_json()
    if not data or 'stock_code' not in data or 'quantity' not in data or 'average_cost' not in data:
        return jsonify({
            'status': 'error',
            'message': '请提供股票代码、数量和平均成本'
        }), 400
        
    success, message, holding = add_holding(
        portfolio_id=portfolio_id,
        user_id=current_user.id,
        stock_code=data.get('stock_code'),
        quantity=data.get('quantity'),
        average_cost=data.get('average_cost')
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
            'id': holding.id if holding else None,
            'stock_code': data.get('stock_code')
        }
    }), 201


@portfolio_bp.route('/api/holdings/<int:holding_id>', methods=['PUT'])
@login_required
def api_update_holding(holding_id):
    """更新持仓API"""
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'message': '请提供更新数据'
        }), 400
        
    success, message = update_holding(
        holding_id=holding_id,
        user_id=current_user.id,
        quantity=data.get('quantity'),
        average_cost=data.get('average_cost')
    )
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': message
        }), 400
        
    return jsonify({
        'status': 'success',
        'message': message
    })


@portfolio_bp.route('/api/holdings/<int:holding_id>', methods=['DELETE'])
@login_required
def api_delete_holding(holding_id):
    """删除持仓API"""
    success, message = delete_holding(holding_id, current_user.id)
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': message
        }), 400
        
    return jsonify({
        'status': 'success',
        'message': message
    })


@portfolio_bp.route('/watchlist')
@login_required
def watchlist():
    """自选股页面"""
    return render_template('portfolio/watchlist.html')


@portfolio_bp.route('/api/watchlist/add', methods=['POST'])
@login_required
def add_to_watchlist():
    """添加股票到自选股"""
    data = request.json
    stock_code = data.get('stock_code')
    
    # TODO: 添加自选股逻辑
    
    return jsonify({'status': 'success', 'message': '已添加到自选股'})


@portfolio_bp.route('/api/watchlist/remove', methods=['POST'])
@login_required
def remove_from_watchlist():
    """从自选股中删除股票"""
    data = request.json
    stock_code = data.get('stock_code')
    
    # TODO: 删除自选股逻辑
    
    return jsonify({'status': 'success', 'message': '已从自选股中删除'}) 