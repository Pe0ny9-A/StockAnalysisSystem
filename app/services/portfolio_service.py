"""
股票系统 - 投资组合服务
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from app import db
from app.models.portfolio import Portfolio, PortfolioHolding
from app.models.transaction import Transaction, TransactionType
from app.services.stock_service import get_stock_data

# 日志配置
logger = logging.getLogger(__name__)


def get_user_portfolios(user_id: int) -> List[Dict[str, Any]]:
    """
    获取用户的所有投资组合
    
    Args:
        user_id: 用户ID
    
    Returns:
        List[Dict]: 投资组合列表
    """
    try:
        portfolios = Portfolio.query.filter_by(user_id=user_id).all()
        
        result = []
        for portfolio in portfolios:
            portfolio_data = {
                'id': portfolio.id,
                'name': portfolio.name,
                'description': portfolio.description,
                'is_default': portfolio.is_default,
                'total_value': portfolio.get_total_value(),
                'total_cost': portfolio.get_total_cost(),
                'total_profit': portfolio.get_total_profit(),
                'profit_percentage': portfolio.get_profit_percentage(),
                'holdings_count': portfolio.holdings.count(),
                'created_at': portfolio.created_at
            }
            result.append(portfolio_data)
            
        return result
    except Exception as e:
        logger.error(f"获取用户投资组合失败: {str(e)}")
        return []


def get_portfolio_detail(portfolio_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    """
    获取投资组合详细信息
    
    Args:
        portfolio_id: 投资组合ID
        user_id: 用户ID (用于权限验证)
    
    Returns:
        Dict: 投资组合详细信息
    """
    try:
        portfolio = Portfolio.query.filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return None
        
        holdings = portfolio.get_holdings_summary()
        
        return {
            'id': portfolio.id,
            'name': portfolio.name,
            'description': portfolio.description,
            'is_default': portfolio.is_default,
            'created_at': portfolio.created_at,
            'total_value': portfolio.get_total_value(),
            'total_cost': portfolio.get_total_cost(),
            'total_profit': portfolio.get_total_profit(),
            'profit_percentage': portfolio.get_profit_percentage(),
            'holdings': holdings
        }
    except Exception as e:
        logger.error(f"获取投资组合详情失败: {str(e)}")
        return None


def create_portfolio(user_id: int, name: str, description: str = None, 
                    is_default: bool = False) -> Optional[Portfolio]:
    """
    创建新投资组合
    
    Args:
        user_id: 用户ID
        name: 投资组合名称
        description: 描述
        is_default: 是否为默认投资组合
    
    Returns:
        Portfolio: 创建的投资组合对象
    """
    try:
        # 如果设置为默认，先将其他投资组合设为非默认
        if is_default:
            Portfolio.query.filter_by(user_id=user_id, is_default=True).update({'is_default': False})
        
        portfolio = Portfolio(
            name=name,
            user_id=user_id,
            description=description,
            is_default=is_default
        )
        
        db.session.add(portfolio)
        db.session.commit()
        return portfolio
    except Exception as e:
        db.session.rollback()
        logger.error(f"创建投资组合失败: {str(e)}")
        return None


def update_portfolio(portfolio_id: int, user_id: int, name: str = None, 
                    description: str = None, is_default: bool = None) -> Tuple[bool, str]:
    """
    更新投资组合信息
    
    Args:
        portfolio_id: 投资组合ID
        user_id: 用户ID (用于权限验证)
        name: 投资组合名称
        description: 描述
        is_default: 是否为默认投资组合
    
    Returns:
        Tuple[bool, str]: (成功状态, 消息)
    """
    try:
        portfolio = Portfolio.query.filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return False, "投资组合不存在或无权限"
        
        if name is not None:
            portfolio.name = name
            
        if description is not None:
            portfolio.description = description
            
        if is_default is not None and is_default and not portfolio.is_default:
            # 如果设置为默认，先将其他投资组合设为非默认
            Portfolio.query.filter_by(user_id=user_id, is_default=True).update({'is_default': False})
            portfolio.is_default = True
        elif is_default is not None:
            portfolio.is_default = is_default
        
        db.session.commit()
        return True, "投资组合更新成功"
    except Exception as e:
        db.session.rollback()
        logger.error(f"更新投资组合失败: {str(e)}")
        return False, f"更新失败: {str(e)}"


def delete_portfolio(portfolio_id: int, user_id: int) -> Tuple[bool, str]:
    """
    删除投资组合
    
    Args:
        portfolio_id: 投资组合ID
        user_id: 用户ID (用于权限验证)
    
    Returns:
        Tuple[bool, str]: (成功状态, 消息)
    """
    try:
        portfolio = Portfolio.query.filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return False, "投资组合不存在或无权限"
        
        # 检查是否有持仓
        if portfolio.holdings.count() > 0:
            return False, "投资组合中存在持仓，无法删除"
        
        # 检查是否为默认投资组合
        if portfolio.is_default:
            # 找到另一个投资组合设为默认
            another_portfolio = Portfolio.query.filter_by(user_id=user_id).filter(
                Portfolio.id != portfolio_id
            ).first()
            
            if another_portfolio:
                another_portfolio.is_default = True
        
        db.session.delete(portfolio)
        db.session.commit()
        return True, "投资组合删除成功"
    except Exception as e:
        db.session.rollback()
        logger.error(f"删除投资组合失败: {str(e)}")
        return False, f"删除失败: {str(e)}"


def add_holding(portfolio_id: int, user_id: int, stock_code: str, 
               quantity: int, average_cost: float) -> Tuple[bool, str, Optional[PortfolioHolding]]:
    """
    添加持仓到投资组合
    
    Args:
        portfolio_id: 投资组合ID
        user_id: 用户ID (用于权限验证)
        stock_code: 股票代码
        quantity: 持有数量
        average_cost: 平均成本
    
    Returns:
        Tuple[bool, str, PortfolioHolding]: (成功状态, 消息, 持仓对象)
    """
    try:
        # 验证投资组合所有权
        portfolio = Portfolio.query.filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return False, "投资组合不存在或无权限", None
        
        # 获取股票信息
        stock_data = get_stock_data(stock_code)
        if 'error' in stock_data:
            return False, f"获取股票信息失败: {stock_data['error']}", None
        
        # 检查是否已存在该股票持仓
        existing = PortfolioHolding.query.filter_by(
            portfolio_id=portfolio_id, stock_code=stock_code
        ).first()
        
        if existing:
            # 更新现有持仓
            old_total_cost = existing.get_total_cost()
            new_total_cost = quantity * average_cost
            
            existing.quantity += quantity
            
            if existing.quantity > 0:
                existing.average_cost = (old_total_cost + new_total_cost) / existing.quantity
            else:
                existing.average_cost = 0
                
            holding = existing
        else:
            # 创建新持仓
            holding = PortfolioHolding(
                portfolio_id=portfolio_id,
                stock_code=stock_code,
                stock_name=stock_data.get('name', '未知'),
                quantity=quantity,
                average_cost=average_cost
            )
            db.session.add(holding)
        
        db.session.commit()
        return True, "持仓添加成功", holding
    except Exception as e:
        db.session.rollback()
        logger.error(f"添加持仓失败: {str(e)}")
        return False, f"添加失败: {str(e)}", None


def update_holding(holding_id: int, user_id: int, quantity: int = None, 
                 average_cost: float = None) -> Tuple[bool, str]:
    """
    更新持仓信息
    
    Args:
        holding_id: 持仓ID
        user_id: 用户ID (用于权限验证)
        quantity: 持有数量
        average_cost: 平均成本
    
    Returns:
        Tuple[bool, str]: (成功状态, 消息)
    """
    try:
        # 验证持仓所有权
        holding = PortfolioHolding.query.join(Portfolio).filter(
            PortfolioHolding.id == holding_id,
            Portfolio.user_id == user_id
        ).first()
        
        if not holding:
            return False, "持仓不存在或无权限"
        
        # 更新数据
        if quantity is not None:
            holding.quantity = quantity
            
        if average_cost is not None:
            holding.average_cost = average_cost
        
        # 如果数量为0，考虑删除持仓
        if holding.quantity == 0:
            db.session.delete(holding)
        
        db.session.commit()
        return True, "持仓更新成功"
    except Exception as e:
        db.session.rollback()
        logger.error(f"更新持仓失败: {str(e)}")
        return False, f"更新失败: {str(e)}"


def delete_holding(holding_id: int, user_id: int) -> Tuple[bool, str]:
    """
    删除持仓
    
    Args:
        holding_id: 持仓ID
        user_id: 用户ID (用于权限验证)
    
    Returns:
        Tuple[bool, str]: (成功状态, 消息)
    """
    try:
        # 验证持仓所有权
        holding = PortfolioHolding.query.join(Portfolio).filter(
            PortfolioHolding.id == holding_id,
            Portfolio.user_id == user_id
        ).first()
        
        if not holding:
            return False, "持仓不存在或无权限"
        
        db.session.delete(holding)
        db.session.commit()
        return True, "持仓删除成功"
    except Exception as e:
        db.session.rollback()
        logger.error(f"删除持仓失败: {str(e)}")
        return False, f"删除失败: {str(e)}"


def get_default_portfolio(user_id: int) -> Optional[Portfolio]:
    """
    获取用户的默认投资组合，如果不存在则创建一个
    
    Args:
        user_id: 用户ID
    
    Returns:
        Portfolio: 默认投资组合
    """
    try:
        # 查找默认投资组合
        portfolio = Portfolio.query.filter_by(user_id=user_id, is_default=True).first()
        
        # 如果不存在默认投资组合，则查找任何一个投资组合
        if not portfolio:
            portfolio = Portfolio.query.filter_by(user_id=user_id).first()
            
        # 如果用户没有任何投资组合，则创建一个默认的
        if not portfolio:
            portfolio = Portfolio(
                name="默认组合",
                user_id=user_id,
                description="系统自动创建的默认投资组合",
                is_default=True
            )
            db.session.add(portfolio)
            db.session.commit()
        elif not portfolio.is_default:
            # 如果找到的不是默认投资组合，将其设为默认
            portfolio.is_default = True
            db.session.commit()
            
        return portfolio
    except Exception as e:
        db.session.rollback()
        logger.error(f"获取默认投资组合失败: {str(e)}")
        return None 