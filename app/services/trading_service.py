"""
股票系统 - 交易服务
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

from app import db
from app.models.transaction import Transaction, TransactionType
from app.models.portfolio import Portfolio, PortfolioHolding
from app.services.stock_service import get_stock_data
from app.services.portfolio_service import get_default_portfolio

# 日志配置
logger = logging.getLogger(__name__)


def execute_buy(user_id: int, portfolio_id: int, stock_code: str, 
               quantity: int, price: float, commission: float = 0, 
               tax: float = 0, notes: str = None) -> Tuple[bool, str, Optional[Transaction]]:
    """
    执行买入交易
    
    Args:
        user_id: 用户ID
        portfolio_id: 投资组合ID
        stock_code: 股票代码
        quantity: 数量
        price: 价格
        commission: 佣金
        tax: 税费
        notes: 备注
    
    Returns:
        Tuple[bool, str, Transaction]: (成功状态, 消息, 交易对象)
    """
    try:
        # 验证投资组合所有权
        portfolio = Portfolio.query.filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            # 使用默认组合
            portfolio = get_default_portfolio(user_id)
            if not portfolio:
                return False, "投资组合不存在且无法创建默认组合", None
        
        # 获取股票信息
        stock_data = get_stock_data(stock_code)
        if 'error' in stock_data:
            return False, f"获取股票信息失败: {stock_data['error']}", None
        
        # 创建交易记录
        transaction = Transaction.create_buy_transaction(
            user_id=user_id,
            portfolio_id=portfolio.id,
            stock_code=stock_code,
            stock_name=stock_data.get('name', '未知'),
            quantity=quantity,
            price=price,
            commission=commission,
            tax=tax,
            notes=notes
        )
        
        db.session.add(transaction)
        
        # 更新或创建持仓
        holding = PortfolioHolding.query.filter_by(
            portfolio_id=portfolio.id, stock_code=stock_code
        ).first()
        
        if holding:
            # 更新持仓
            holding.update_after_trade(quantity, price)
        else:
            # 创建新持仓
            holding = PortfolioHolding(
                portfolio_id=portfolio.id,
                stock_code=stock_code,
                stock_name=stock_data.get('name', '未知'),
                quantity=quantity,
                average_cost=price
            )
            db.session.add(holding)
        
        db.session.commit()
        return True, "买入交易执行成功", transaction
    except Exception as e:
        db.session.rollback()
        logger.error(f"执行买入交易失败: {str(e)}")
        return False, f"交易失败: {str(e)}", None


def execute_sell(user_id: int, portfolio_id: int, stock_code: str, 
                quantity: int, price: float, commission: float = 0, 
                tax: float = 0, notes: str = None) -> Tuple[bool, str, Optional[Transaction]]:
    """
    执行卖出交易
    
    Args:
        user_id: 用户ID
        portfolio_id: 投资组合ID
        stock_code: 股票代码
        quantity: 数量
        price: 价格
        commission: 佣金
        tax: 税费
        notes: 备注
    
    Returns:
        Tuple[bool, str, Transaction]: (成功状态, 消息, 交易对象)
    """
    try:
        # 验证投资组合所有权
        portfolio = Portfolio.query.filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return False, "投资组合不存在或无权限", None
        
        # 验证持仓
        holding = PortfolioHolding.query.filter_by(
            portfolio_id=portfolio.id, stock_code=stock_code
        ).first()
        
        if not holding:
            return False, "该投资组合中不存在此股票持仓", None
        
        if holding.quantity < quantity:
            return False, "持仓数量不足", None
        
        # 获取股票信息
        stock_data = get_stock_data(stock_code)
        if 'error' in stock_data:
            return False, f"获取股票信息失败: {stock_data['error']}", None
        
        # 创建交易记录
        transaction = Transaction.create_sell_transaction(
            user_id=user_id,
            portfolio_id=portfolio.id,
            stock_code=stock_code,
            stock_name=stock_data.get('name', holding.stock_name),
            quantity=quantity,
            price=price,
            commission=commission,
            tax=tax,
            notes=notes
        )
        
        db.session.add(transaction)
        
        # 更新持仓
        holding.update_after_trade(-quantity, price)
        
        # 如果卖出后数量为0，删除持仓
        if holding.quantity == 0:
            db.session.delete(holding)
        
        db.session.commit()
        return True, "卖出交易执行成功", transaction
    except Exception as e:
        db.session.rollback()
        logger.error(f"执行卖出交易失败: {str(e)}")
        return False, f"交易失败: {str(e)}", None


def get_user_transactions(user_id: int, portfolio_id: int = None, 
                         stock_code: str = None, limit: int = 50) -> List[Dict[str, Any]]:
    """
    获取用户交易记录
    
    Args:
        user_id: 用户ID
        portfolio_id: 投资组合ID(可选)
        stock_code: 股票代码(可选)
        limit: 返回结果数量限制
    
    Returns:
        List[Dict]: 交易记录列表
    """
    try:
        query = Transaction.query.filter_by(user_id=user_id)
        
        if portfolio_id:
            query = query.filter_by(portfolio_id=portfolio_id)
            
        if stock_code:
            query = query.filter_by(stock_code=stock_code)
        
        transactions = query.order_by(Transaction.executed_at.desc()).limit(limit).all()
        
        result = []
        for transaction in transactions:
            transaction_data = transaction.get_transaction_info()
            result.append(transaction_data)
            
        return result
    except Exception as e:
        logger.error(f"获取用户交易记录失败: {str(e)}")
        return []


def get_transaction_detail(transaction_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    """
    获取交易详情
    
    Args:
        transaction_id: 交易ID
        user_id: 用户ID(用于权限验证)
    
    Returns:
        Dict: 交易详细信息
    """
    try:
        transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
        if not transaction:
            return None
            
        return transaction.get_transaction_info()
    except Exception as e:
        logger.error(f"获取交易详情失败: {str(e)}")
        return None


def get_transaction_stats(user_id: int, portfolio_id: int = None, 
                         period: str = 'all') -> Dict[str, Any]:
    """
    获取交易统计信息
    
    Args:
        user_id: 用户ID
        portfolio_id: 投资组合ID(可选)
        period: 时间段 ('all', 'year', 'month', 'week')
    
    Returns:
        Dict: 统计信息
    """
    try:
        query = Transaction.query.filter_by(user_id=user_id)
        
        if portfolio_id:
            query = query.filter_by(portfolio_id=portfolio_id)
        
        # 添加时间过滤
        if period == 'year':
            year_start = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            query = query.filter(Transaction.executed_at >= year_start)
        elif period == 'month':
            month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            query = query.filter(Transaction.executed_at >= month_start)
        elif period == 'week':
            today = datetime.now().date()
            week_start = today - timedelta(days=today.weekday())
            query = query.filter(Transaction.executed_at >= week_start)
        
        transactions = query.all()
        
        # 计算统计数据
        total_buy = sum(t.total_amount for t in transactions if t.transaction_type == TransactionType.BUY)
        total_sell = sum(t.total_amount for t in transactions if t.transaction_type == TransactionType.SELL)
        total_commission = sum(t.commission for t in transactions)
        total_tax = sum(t.tax for t in transactions)
        total_fee = total_commission + total_tax
        net_cash_flow = total_sell - total_buy - total_fee
        transaction_count = len(transactions)
        buy_count = sum(1 for t in transactions if t.transaction_type == TransactionType.BUY)
        sell_count = sum(1 for t in transactions if t.transaction_type == TransactionType.SELL)
        
        # 获取交易的股票数
        stock_codes = set(t.stock_code for t in transactions)
        stock_count = len(stock_codes)
        
        # 统计最活跃的股票
        if transactions:
            from collections import Counter
            stock_counter = Counter(t.stock_code for t in transactions)
            most_active_stocks = stock_counter.most_common(5)
            most_active = [{'code': code, 'name': next((t.stock_name for t in transactions if t.stock_code == code), ''), 'count': count} 
                          for code, count in most_active_stocks]
        else:
            most_active = []
        
        return {
            'total_buy': total_buy,
            'total_sell': total_sell,
            'total_commission': total_commission,
            'total_tax': total_tax,
            'total_fee': total_fee,
            'net_cash_flow': net_cash_flow,
            'transaction_count': transaction_count,
            'buy_count': buy_count,
            'sell_count': sell_count,
            'stock_count': stock_count,
            'period': period,
            'most_active_stocks': most_active
        }
    except Exception as e:
        logger.error(f"获取交易统计失败: {str(e)}")
        return {
            'error': str(e),
            'total_buy': 0,
            'total_sell': 0,
            'total_fee': 0,
            'net_cash_flow': 0,
            'transaction_count': 0
        } 