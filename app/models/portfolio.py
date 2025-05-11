"""
股票系统 - 投资组合模型
"""
from datetime import datetime
from typing import List, Dict, Any

from app import db


class Portfolio(db.Model):
    """投资组合模型"""
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键关系
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 关系
    holdings = db.relationship('PortfolioHolding', backref='portfolio', lazy='dynamic', 
                               cascade='all, delete-orphan')
    
    def __init__(self, name: str, user_id: int, description: str = None, is_default: bool = False):
        """初始化投资组合实例"""
        self.name = name
        self.user_id = user_id
        self.description = description
        self.is_default = is_default
    
    def get_total_value(self) -> float:
        """计算投资组合总价值"""
        return sum(holding.get_current_value() for holding in self.holdings)
    
    def get_total_cost(self) -> float:
        """计算投资组合总成本"""
        return sum(holding.get_total_cost() for holding in self.holdings)
    
    def get_total_profit(self) -> float:
        """计算投资组合总收益"""
        return self.get_total_value() - self.get_total_cost()
    
    def get_profit_percentage(self) -> float:
        """计算投资组合收益率"""
        total_cost = self.get_total_cost()
        if total_cost == 0:
            return 0
        return (self.get_total_profit() / total_cost) * 100
    
    def get_holdings_summary(self) -> List[Dict[str, Any]]:
        """获取持仓汇总信息"""
        result = []
        for holding in self.holdings:
            result.append({
                'stock_code': holding.stock_code,
                'stock_name': holding.stock_name,
                'quantity': holding.quantity,
                'average_cost': holding.average_cost,
                'current_price': holding.get_current_price(),
                'current_value': holding.get_current_value(),
                'total_cost': holding.get_total_cost(),
                'profit': holding.get_profit(),
                'profit_percentage': holding.get_profit_percentage()
            })
        return result
    
    def calculate_total_assets(self) -> float:
        """计算投资组合总资产（用于仪表盘）"""
        return self.get_total_value()
    
    def calculate_change_rate(self) -> float:
        """计算投资组合变化率（用于仪表盘）"""
        return self.get_profit_percentage()
    
    def get_stock_count(self) -> int:
        """获取投资组合中的股票数量（用于仪表盘）"""
        return self.holdings.count()
    
    def __repr__(self) -> str:
        """返回投资组合的字符串表示"""
        return f"<Portfolio {self.name} of User {self.user_id}>"


class PortfolioHolding(db.Model):
    """投资组合持仓模型"""
    __tablename__ = 'portfolio_holdings'

    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(20), nullable=False)
    stock_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    average_cost = db.Column(db.Float, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键关系
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    
    def __init__(self, portfolio_id: int, stock_code: str, stock_name: str, 
                quantity: int = 0, average_cost: float = 0):
        """初始化持仓实例"""
        self.portfolio_id = portfolio_id
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.quantity = quantity
        self.average_cost = average_cost
    
    def get_current_price(self) -> float:
        """获取当前股价"""
        # TODO: 从股票数据服务获取最新价格
        from app.services.stock_service import get_stock_price
        try:
            return get_stock_price(self.stock_code)
        except:
            # 临时返回平均成本以避免错误
            return self.average_cost
    
    def get_current_value(self) -> float:
        """计算当前市值"""
        return self.quantity * self.get_current_price()
    
    def get_total_cost(self) -> float:
        """计算总成本"""
        return self.quantity * self.average_cost
    
    def get_profit(self) -> float:
        """计算盈亏金额"""
        return self.get_current_value() - self.get_total_cost()
    
    def get_profit_percentage(self) -> float:
        """计算盈亏比例"""
        total_cost = self.get_total_cost()
        if total_cost == 0:
            return 0
        return (self.get_profit() / total_cost) * 100
    
    def update_after_trade(self, quantity: int, price: float) -> None:
        """交易后更新持仓"""
        if self.quantity + quantity == 0:
            self.average_cost = 0
        elif quantity > 0:  # 买入
            total_cost = self.get_total_cost() + (quantity * price)
            self.quantity += quantity
            self.average_cost = total_cost / self.quantity
        else:  # 卖出，不改变均价
            self.quantity += quantity
    
    def __repr__(self) -> str:
        """返回持仓的字符串表示"""
        return f"<PortfolioHolding {self.stock_code} in Portfolio {self.portfolio_id}>" 