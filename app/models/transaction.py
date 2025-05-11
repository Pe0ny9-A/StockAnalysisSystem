"""
股票系统 - 交易模型
"""
from datetime import datetime
from enum import Enum
from typing import Dict, Any

from app import db


class TransactionType(Enum):
    """交易类型枚举"""
    BUY = 'buy'
    SELL = 'sell'


class Transaction(db.Model):
    """交易记录模型"""
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(20), nullable=False)
    stock_name = db.Column(db.String(100), nullable=False)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    commission = db.Column(db.Float, default=0)
    tax = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    executed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键关系
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    
    def __init__(self, user_id: int, portfolio_id: int, stock_code: str, stock_name: str,
                transaction_type: TransactionType, quantity: int, price: float,
                commission: float = 0, tax: float = 0, notes: str = None,
                executed_at: datetime = None):
        """初始化交易记录实例"""
        self.user_id = user_id
        self.portfolio_id = portfolio_id
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.transaction_type = transaction_type
        self.quantity = quantity
        self.price = price
        self.total_amount = quantity * price
        self.commission = commission
        self.tax = tax
        self.notes = notes
        self.executed_at = executed_at or datetime.utcnow()
    
    def get_net_amount(self) -> float:
        """计算交易净额"""
        # 买入为负，卖出为正
        direction = -1 if self.transaction_type == TransactionType.BUY else 1
        return direction * self.total_amount - self.commission - self.tax
    
    def get_transaction_info(self) -> Dict[str, Any]:
        """获取交易详细信息"""
        return {
            'id': self.id,
            'stock_code': self.stock_code,
            'stock_name': self.stock_name,
            'transaction_type': self.transaction_type.value,
            'quantity': self.quantity,
            'price': self.price,
            'total_amount': self.total_amount,
            'commission': self.commission,
            'tax': self.tax,
            'net_amount': self.get_net_amount(),
            'notes': self.notes,
            'executed_at': self.executed_at,
            'portfolio_id': self.portfolio_id
        }
    
    @classmethod
    def create_buy_transaction(cls, user_id: int, portfolio_id: int, stock_code: str, 
                             stock_name: str, quantity: int, price: float, **kwargs) -> 'Transaction':
        """创建买入交易记录"""
        return cls(
            user_id=user_id,
            portfolio_id=portfolio_id,
            stock_code=stock_code,
            stock_name=stock_name,
            transaction_type=TransactionType.BUY,
            quantity=quantity,
            price=price,
            **kwargs
        )
    
    @classmethod
    def create_sell_transaction(cls, user_id: int, portfolio_id: int, stock_code: str, 
                              stock_name: str, quantity: int, price: float, **kwargs) -> 'Transaction':
        """创建卖出交易记录"""
        return cls(
            user_id=user_id,
            portfolio_id=portfolio_id,
            stock_code=stock_code,
            stock_name=stock_name,
            transaction_type=TransactionType.SELL,
            quantity=quantity,
            price=price,
            **kwargs
        )
    
    def __repr__(self) -> str:
        """返回交易记录的字符串表示"""
        return f"<Transaction {self.transaction_type.value} {self.quantity} {self.stock_code} at {self.price}>" 