"""
股票系统 - 观察列表服务
"""
import logging
from typing import List, Dict, Any, Optional, Tuple

from app import db
from app.models.watchlist import WatchList, WatchListStock
from app.services.stock_service import get_stock_data

# 日志配置
logger = logging.getLogger(__name__)


def get_user_watchlists(user_id: int) -> List[Dict[str, Any]]:
    """
    获取用户的所有观察列表
    
    Args:
        user_id: 用户ID
    
    Returns:
        List[Dict]: 观察列表列表
    """
    try:
        watchlists = WatchList.query.filter_by(user_id=user_id).all()
        
        result = []
        for watchlist in watchlists:
            watchlist_data = {
                'id': watchlist.id,
                'name': watchlist.name,
                'description': watchlist.description,
                'is_default': watchlist.is_default,
                'stocks_count': watchlist.stocks.count(),
                'created_at': watchlist.created_at
            }
            result.append(watchlist_data)
            
        return result
    except Exception as e:
        logger.error(f"获取用户观察列表失败: {str(e)}")
        return []


def get_watchlist_detail(watchlist_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    """
    获取观察列表详细信息及包含的股票
    
    Args:
        watchlist_id: 观察列表ID
        user_id: 用户ID (用于权限验证)
    
    Returns:
        Dict: 观察列表详细信息
    """
    try:
        watchlist = WatchList.query.filter_by(id=watchlist_id, user_id=user_id).first()
        if not watchlist:
            return None
        
        # 获取并处理观察列表中的股票数据
        stocks_data = watchlist.get_stocks_data()
        
        return {
            'id': watchlist.id,
            'name': watchlist.name,
            'description': watchlist.description,
            'is_default': watchlist.is_default,
            'created_at': watchlist.created_at,
            'stocks': stocks_data,
            'stocks_count': len(stocks_data)
        }
    except Exception as e:
        logger.error(f"获取观察列表详情失败: {str(e)}")
        return None


def create_watchlist(user_id: int, name: str, description: str = None, 
                    is_default: bool = False) -> Optional[WatchList]:
    """
    创建新观察列表
    
    Args:
        user_id: 用户ID
        name: 观察列表名称
        description: 描述
        is_default: 是否为默认观察列表
    
    Returns:
        WatchList: 创建的观察列表对象
    """
    try:
        # 如果设置为默认，先将其他观察列表设为非默认
        if is_default:
            WatchList.query.filter_by(user_id=user_id, is_default=True).update({'is_default': False})
        
        watchlist = WatchList(
            name=name,
            user_id=user_id,
            description=description,
            is_default=is_default
        )
        
        db.session.add(watchlist)
        db.session.commit()
        return watchlist
    except Exception as e:
        db.session.rollback()
        logger.error(f"创建观察列表失败: {str(e)}")
        return None


def update_watchlist(watchlist_id: int, user_id: int, name: str = None, 
                    description: str = None, is_default: bool = None) -> Tuple[bool, str]:
    """
    更新观察列表信息
    
    Args:
        watchlist_id: 观察列表ID
        user_id: 用户ID (用于权限验证)
        name: 观察列表名称
        description: 描述
        is_default: 是否为默认观察列表
    
    Returns:
        Tuple[bool, str]: (成功状态, 消息)
    """
    try:
        watchlist = WatchList.query.filter_by(id=watchlist_id, user_id=user_id).first()
        if not watchlist:
            return False, "观察列表不存在或无权限"
        
        if name is not None:
            watchlist.name = name
            
        if description is not None:
            watchlist.description = description
            
        if is_default is not None and is_default and not watchlist.is_default:
            # 如果设置为默认，先将其他观察列表设为非默认
            WatchList.query.filter_by(user_id=user_id, is_default=True).update({'is_default': False})
            watchlist.is_default = True
        elif is_default is not None:
            watchlist.is_default = is_default
        
        db.session.commit()
        return True, "观察列表更新成功"
    except Exception as e:
        db.session.rollback()
        logger.error(f"更新观察列表失败: {str(e)}")
        return False, f"更新失败: {str(e)}"


def delete_watchlist(watchlist_id: int, user_id: int) -> Tuple[bool, str]:
    """
    删除观察列表
    
    Args:
        watchlist_id: 观察列表ID
        user_id: 用户ID (用于权限验证)
    
    Returns:
        Tuple[bool, str]: (成功状态, 消息)
    """
    try:
        watchlist = WatchList.query.filter_by(id=watchlist_id, user_id=user_id).first()
        if not watchlist:
            return False, "观察列表不存在或无权限"
        
        # 检查是否为默认观察列表
        if watchlist.is_default:
            # 找到另一个观察列表设为默认
            another_watchlist = WatchList.query.filter_by(user_id=user_id).filter(
                WatchList.id != watchlist_id
            ).first()
            
            if another_watchlist:
                another_watchlist.is_default = True
        
        db.session.delete(watchlist)
        db.session.commit()
        return True, "观察列表删除成功"
    except Exception as e:
        db.session.rollback()
        logger.error(f"删除观察列表失败: {str(e)}")
        return False, f"删除失败: {str(e)}"


def add_stock_to_watchlist(watchlist_id: int, user_id: int, stock_code: str, 
                          notes: str = None) -> Tuple[bool, str, Optional[WatchListStock]]:
    """
    添加股票到观察列表
    
    Args:
        watchlist_id: 观察列表ID
        user_id: 用户ID (用于权限验证)
        stock_code: 股票代码
        notes: 备注
    
    Returns:
        Tuple[bool, str, WatchListStock]: (成功状态, 消息, 观察列表股票对象)
    """
    try:
        # 验证观察列表所有权
        watchlist = WatchList.query.filter_by(id=watchlist_id, user_id=user_id).first()
        if not watchlist:
            return False, "观察列表不存在或无权限", None
        
        # 检查股票是否已在观察列表中
        existing = watchlist.stocks.filter_by(stock_code=stock_code).first()
        if existing:
            # 更新备注
            if notes is not None:
                existing.notes = notes
                db.session.commit()
            return True, "股票已在观察列表中", existing
        
        # 获取股票信息
        stock_data = get_stock_data(stock_code)
        if 'error' in stock_data:
            return False, f"获取股票信息失败: {stock_data['error']}", None
        
        # 添加到观察列表
        watchlist_stock = watchlist.add_stock(
            stock_code=stock_code,
            stock_name=stock_data.get('name', '未知'),
            notes=notes
        )
        
        db.session.commit()
        return True, "股票添加成功", watchlist_stock
    except Exception as e:
        db.session.rollback()
        logger.error(f"添加股票到观察列表失败: {str(e)}")
        return False, f"添加失败: {str(e)}", None


def remove_stock_from_watchlist(watchlist_id: int, user_id: int, stock_code: str) -> Tuple[bool, str]:
    """
    从观察列表中移除股票
    
    Args:
        watchlist_id: 观察列表ID
        user_id: 用户ID (用于权限验证)
        stock_code: 股票代码
    
    Returns:
        Tuple[bool, str]: (成功状态, 消息)
    """
    try:
        # 验证观察列表所有权
        watchlist = WatchList.query.filter_by(id=watchlist_id, user_id=user_id).first()
        if not watchlist:
            return False, "观察列表不存在或无权限"
        
        # 检查股票是否在观察列表中
        exists = watchlist.stocks.filter_by(stock_code=stock_code).first()
        if not exists:
            return False, "股票不在观察列表中"
        
        # 从观察列表中移除
        result = watchlist.remove_stock(stock_code)
        
        db.session.commit()
        return True, "股票移除成功"
    except Exception as e:
        db.session.rollback()
        logger.error(f"从观察列表移除股票失败: {str(e)}")
        return False, f"移除失败: {str(e)}"


def update_stock_notes(watchlist_id: int, user_id: int, stock_code: str, 
                      notes: str) -> Tuple[bool, str]:
    """
    更新观察列表中股票的备注
    
    Args:
        watchlist_id: 观察列表ID
        user_id: 用户ID (用于权限验证)
        stock_code: 股票代码
        notes: 备注
    
    Returns:
        Tuple[bool, str]: (成功状态, 消息)
    """
    try:
        # 验证观察列表所有权
        watchlist = WatchList.query.filter_by(id=watchlist_id, user_id=user_id).first()
        if not watchlist:
            return False, "观察列表不存在或无权限"
        
        # 检查股票是否在观察列表中
        stock = watchlist.stocks.filter_by(stock_code=stock_code).first()
        if not stock:
            return False, "股票不在观察列表中"
        
        # 更新备注
        stock.notes = notes
        
        db.session.commit()
        return True, "备注更新成功"
    except Exception as e:
        db.session.rollback()
        logger.error(f"更新观察列表股票备注失败: {str(e)}")
        return False, f"更新失败: {str(e)}"


def get_default_watchlist(user_id: int) -> Optional[WatchList]:
    """
    获取用户的默认观察列表，如果不存在则创建一个
    
    Args:
        user_id: 用户ID
    
    Returns:
        WatchList: 默认观察列表
    """
    try:
        # 查找默认观察列表
        watchlist = WatchList.query.filter_by(user_id=user_id, is_default=True).first()
        
        # 如果不存在默认观察列表，则查找任何一个观察列表
        if not watchlist:
            watchlist = WatchList.query.filter_by(user_id=user_id).first()
            
        # 如果用户没有任何观察列表，则创建一个默认的
        if not watchlist:
            watchlist = WatchList(
                name="默认观察",
                user_id=user_id,
                description="系统自动创建的默认观察列表",
                is_default=True
            )
            db.session.add(watchlist)
            db.session.commit()
        elif not watchlist.is_default:
            # 如果找到的不是默认观察列表，将其设为默认
            watchlist.is_default = True
            db.session.commit()
            
        return watchlist
    except Exception as e:
        db.session.rollback()
        logger.error(f"获取默认观察列表失败: {str(e)}")
        return None 