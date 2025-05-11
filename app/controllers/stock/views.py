"""
股票模块视图
"""
from flask import render_template, jsonify, request
from flask_login import login_required, current_user

from app.controllers.stock import stock_bp
from app.services.stock_service import (
    get_stock_data, get_stock_k_line, get_stock_price,
    search_stocks
)


@stock_bp.route('/')
@login_required
def index():
    """股票列表页面"""
    return render_template('stock/index.html')


@stock_bp.route('/detail/<string:code>')
@login_required
def detail(code):
    """股票详情页面"""
    stock_data = get_stock_data(code)
    return render_template('stock/detail.html', stock=stock_data)


@stock_bp.route('/search')
@login_required
def search():
    """搜索股票页面"""
    keyword = request.args.get('keyword', '')
    stocks = []
    if keyword:
        stocks = search_stocks(keyword)
    return render_template('stock/search.html', stocks=stocks, keyword=keyword)


# API接口

@stock_bp.route('/api/stocks/<string:code>')
@login_required
def api_get_stock(code):
    """获取股票数据API"""
    stock_data = get_stock_data(code)
    if 'error' in stock_data:
        return jsonify({
            'status': 'error',
            'message': stock_data['error']
        }), 404
        
    return jsonify({
        'status': 'success',
        'data': stock_data
    })


@stock_bp.route('/api/stocks/<string:code>/price')
@login_required
def api_get_stock_price(code):
    """获取股票价格API"""
    try:
        price = get_stock_price(code)
        return jsonify({
            'status': 'success',
            'data': {
                'code': code,
                'price': price
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 404


@stock_bp.route('/api/stocks/<string:code>/kline')
@login_required
def api_get_kline(code):
    """获取K线数据API"""
    period = request.args.get('period', 'daily')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', 90, type=int)
    
    kline_data = get_stock_k_line(
        stock_code=code,
        period=period,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )
    
    return jsonify({
        'status': 'success',
        'data': {
            'code': code,
            'period': period,
            'kline': kline_data
        }
    })


@stock_bp.route('/api/stocks/search')
@login_required
def api_search_stocks():
    """搜索股票API"""
    keyword = request.args.get('keyword', '')
    limit = request.args.get('limit', 10, type=int)
    
    if not keyword:
        return jsonify({
            'status': 'error',
            'message': '请提供搜索关键词'
        }), 400
    
    stocks = search_stocks(keyword, limit)
    
    return jsonify({
        'status': 'success',
        'data': stocks
    }) 