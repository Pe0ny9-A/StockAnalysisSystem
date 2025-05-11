"""
观察列表模块视图
"""
from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.controllers.watchlist import watchlist_bp
from app.services.watchlist_service import (
    get_user_watchlists, get_watchlist_detail, create_watchlist,
    update_watchlist, delete_watchlist, add_stock_to_watchlist,
    remove_stock_from_watchlist, update_stock_notes, get_default_watchlist
)
from app.services.stock_service import search_stocks


@watchlist_bp.route('/')
@login_required
def index():
    """观察列表页面"""
    watchlists = get_user_watchlists(current_user.id)
    return render_template('watchlist/index.html', watchlists=watchlists)


@watchlist_bp.route('/detail/<int:watchlist_id>')
@login_required
def detail(watchlist_id):
    """观察列表详情页面"""
    watchlist = get_watchlist_detail(watchlist_id, current_user.id)
    if not watchlist:
        flash('观察列表不存在或无权访问', 'error')
        return redirect(url_for('watchlist.index'))
    return render_template('watchlist/detail.html', watchlist=watchlist)


@watchlist_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """创建观察列表页面"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        is_default = request.form.get('is_default') == 'on'
        
        if not name:
            flash('请输入观察列表名称', 'error')
            return render_template('watchlist/create.html')
            
        watchlist = create_watchlist(
            user_id=current_user.id,
            name=name,
            description=description,
            is_default=is_default
        )
        
        if watchlist:
            flash('观察列表创建成功', 'success')
            return redirect(url_for('watchlist.detail', watchlist_id=watchlist.id))
        else:
            flash('观察列表创建失败', 'error')
            
    return render_template('watchlist/create.html')


@watchlist_bp.route('/add_stock/<int:watchlist_id>', methods=['GET', 'POST'])
@login_required
def add_stock(watchlist_id):
    """添加股票到观察列表页面"""
    if request.method == 'POST':
        stock_code = request.form.get('stock_code')
        notes = request.form.get('notes', '')
        
        if not stock_code:
            flash('请输入股票代码', 'error')
            return render_template('watchlist/add_stock.html', watchlist_id=watchlist_id)
            
        success, message, watchlist_stock = add_stock_to_watchlist(
            watchlist_id=watchlist_id,
            user_id=current_user.id,
            stock_code=stock_code,
            notes=notes
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('watchlist.detail', watchlist_id=watchlist_id))
        else:
            flash(message, 'error')
            
    # 获取股票搜索结果
    keyword = request.args.get('keyword', '')
    stocks = []
    if keyword:
        stocks = search_stocks(keyword)
            
    return render_template('watchlist/add_stock.html', 
                           watchlist_id=watchlist_id, 
                           stocks=stocks,
                           keyword=keyword)


# API接口

@watchlist_bp.route('/api/watchlists')
@login_required
def api_get_watchlists():
    """获取用户观察列表列表API"""
    watchlists = get_user_watchlists(current_user.id)
    return jsonify({
        'status': 'success',
        'data': watchlists
    })


@watchlist_bp.route('/api/watchlists/<int:watchlist_id>')
@login_required
def api_get_watchlist(watchlist_id):
    """获取单个观察列表详情API"""
    watchlist = get_watchlist_detail(watchlist_id, current_user.id)
    if not watchlist:
        return jsonify({
            'status': 'error',
            'message': '观察列表不存在或无权访问'
        }), 404
        
    return jsonify({
        'status': 'success',
        'data': watchlist
    })


@watchlist_bp.route('/api/watchlists', methods=['POST'])
@login_required
def api_create_watchlist():
    """创建观察列表API"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({
            'status': 'error',
            'message': '请提供观察列表名称'
        }), 400
        
    watchlist = create_watchlist(
        user_id=current_user.id,
        name=data.get('name'),
        description=data.get('description', ''),
        is_default=data.get('is_default', False)
    )
    
    if not watchlist:
        return jsonify({
            'status': 'error',
            'message': '观察列表创建失败'
        }), 500
        
    return jsonify({
        'status': 'success',
        'message': '观察列表创建成功',
        'data': {
            'id': watchlist.id,
            'name': watchlist.name
        }
    }), 201


@watchlist_bp.route('/api/watchlists/<int:watchlist_id>', methods=['PUT'])
@login_required
def api_update_watchlist(watchlist_id):
    """更新观察列表API"""
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'message': '请提供更新数据'
        }), 400
        
    success, message = update_watchlist(
        watchlist_id=watchlist_id,
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


@watchlist_bp.route('/api/watchlists/<int:watchlist_id>', methods=['DELETE'])
@login_required
def api_delete_watchlist(watchlist_id):
    """删除观察列表API"""
    success, message = delete_watchlist(watchlist_id, current_user.id)
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': message
        }), 400
        
    return jsonify({
        'status': 'success',
        'message': message
    })


@watchlist_bp.route('/api/watchlists/<int:watchlist_id>/stocks', methods=['POST'])
@login_required
def api_add_stock(watchlist_id):
    """添加股票到观察列表API"""
    data = request.get_json()
    if not data or 'stock_code' not in data:
        return jsonify({
            'status': 'error',
            'message': '请提供股票代码'
        }), 400
        
    success, message, watchlist_stock = add_stock_to_watchlist(
        watchlist_id=watchlist_id,
        user_id=current_user.id,
        stock_code=data.get('stock_code'),
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
            'stock_code': data.get('stock_code')
        }
    }), 201


@watchlist_bp.route('/api/watchlists/<int:watchlist_id>/stocks/<string:stock_code>', methods=['DELETE'])
@login_required
def api_remove_stock(watchlist_id, stock_code):
    """从观察列表移除股票API"""
    success, message = remove_stock_from_watchlist(
        watchlist_id=watchlist_id,
        user_id=current_user.id,
        stock_code=stock_code
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


@watchlist_bp.route('/api/watchlists/<int:watchlist_id>/stocks/<string:stock_code>/notes', methods=['PUT'])
@login_required
def api_update_stock_notes(watchlist_id, stock_code):
    """更新观察列表股票备注API"""
    data = request.get_json()
    if not data or 'notes' not in data:
        return jsonify({
            'status': 'error',
            'message': '请提供备注内容'
        }), 400
        
    success, message = update_stock_notes(
        watchlist_id=watchlist_id,
        user_id=current_user.id,
        stock_code=stock_code,
        notes=data.get('notes')
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