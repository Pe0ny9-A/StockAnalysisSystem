"""
股票系统 - 交易记录模型
"""
from datetime import datetime
from typing import List, Dict, Any

from app import db


class Trade(db.Model):
    """交易记录模型"""
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(20), nullable=False)
    stock_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    trade_type = db.Column(db.String(10), nullable=False)  # 'buy' or 'sell'
    trade_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    commission = db.Column(db.Float, default=0.0)
    
    # 外键关系
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    
    def __init__(self, user_id: int, portfolio_id: int, stock_code: str, stock_name: str, 
                price: float, quantity: int, trade_type: str, commission: float = 0.0):
        """初始化交易记录实例"""
        self.user_id = user_id
        self.portfolio_id = portfolio_id
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.price = price
        self.quantity = quantity
        self.trade_type = trade_type
        self.commission = commission
        
        # 计算交易总金额（含手续费）
        self.total_amount = (price * quantity) + commission
    
    @classmethod
    def get_user_trades(cls, user_id: int, limit: int = None) -> List['Trade']:
        """获取用户的交易记录"""
        query = cls.query.filter_by(user_id=user_id).order_by(cls.trade_date.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @classmethod
    def get_portfolio_trades(cls, portfolio_id: int, limit: int = None) -> List['Trade']:
        """获取投资组合的交易记录"""
        query = cls.query.filter_by(portfolio_id=portfolio_id).order_by(cls.trade_date.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @property
    def type(self) -> str:
        """获取交易类型的中文名称"""
        return "买入" if self.trade_type == "buy" else "卖出"
    
    @property
    def formatted_date(self) -> str:
        """获取格式化的交易日期"""
        return self.trade_date.strftime('%Y-%m-%d')
    
    @property
    def formatted_total(self) -> str:
        """获取格式化的交易总额"""
        return f"{self.total_amount:.2f}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'stock_code': self.stock_code,
            'stock_name': self.stock_name,
            'price': self.price,
            'quantity': self.quantity,
            'trade_type': self.trade_type,
            'type': self.type,
            'trade_date': self.formatted_date,
            'total_amount': self.total_amount,
            'commission': self.commission,
            'user_id': self.user_id,
            'portfolio_id': self.portfolio_id,
        }
    
    def __repr__(self) -> str:
        """返回交易记录的字符串表示"""
        action = "Buy" if self.trade_type == "buy" else "Sell"
        return f"<Trade {action} {self.quantity} shares of {self.stock_code} at {self.price}>" 