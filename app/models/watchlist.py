"""
股票系统 - 观察列表模型
"""
from datetime import datetime
from typing import List, Dict, Any

from app import db


class WatchList(db.Model):
    """观察列表模型"""
    __tablename__ = 'watchlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键关系
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 关系
    stocks = db.relationship('WatchListStock', backref='watchlist', lazy='dynamic',
                            cascade='all, delete-orphan')
    
    def __init__(self, name: str, user_id: int, description: str = None, is_default: bool = False):
        """初始化观察列表实例"""
        self.name = name
        self.user_id = user_id
        self.description = description
        self.is_default = is_default
    
    def add_stock(self, stock_code: str, stock_name: str, notes: str = None) -> 'WatchListStock':
        """添加股票到观察列表"""
        # 检查是否已存在
        existing = self.stocks.filter_by(stock_code=stock_code).first()
        if existing:
            return existing
            
        # 创建新记录
        stock = WatchListStock(
            watchlist_id=self.id,
            stock_code=stock_code,
            stock_name=stock_name,
            notes=notes
        )
        db.session.add(stock)
        return stock
    
    def remove_stock(self, stock_code: str) -> bool:
        """从观察列表中移除股票"""
        stock = self.stocks.filter_by(stock_code=stock_code).first()
        if stock:
            db.session.delete(stock)
            return True
        return False
    
    def get_stocks_data(self) -> List[Dict[str, Any]]:
        """获取观察列表中所有股票的数据"""
        from app.services.stock_service import get_stock_data
        result = []
        
        for stock in self.stocks:
            try:
                # 获取股票数据
                stock_data = get_stock_data(stock.stock_code)
                stock_data['notes'] = stock.notes
                stock_data['added_at'] = stock.created_at
                result.append(stock_data)
            except Exception as e:
                # 处理获取数据失败的情况
                result.append({
                    'stock_code': stock.stock_code,
                    'stock_name': stock.stock_name,
                    'notes': stock.notes,
                    'added_at': stock.created_at,
                    'error': str(e)
                })
                
        return result
    
    def __repr__(self) -> str:
        """返回观察列表的字符串表示"""
        return f"<WatchList {self.name} of User {self.user_id}>"


class WatchListStock(db.Model):
    """观察列表股票模型"""
    __tablename__ = 'watchlist_stocks'

    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(20), nullable=False)
    stock_name = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键关系
    watchlist_id = db.Column(db.Integer, db.ForeignKey('watchlists.id'), nullable=False)
    
    # 组合唯一约束，确保每个观察列表中的股票代码唯一
    __table_args__ = (
        db.UniqueConstraint('watchlist_id', 'stock_code', name='uix_watchlist_stock'),
    )
    
    def __init__(self, watchlist_id: int, stock_code: str, stock_name: str, notes: str = None):
        """初始化观察列表股票实例"""
        self.watchlist_id = watchlist_id
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.notes = notes
    
    def __repr__(self) -> str:
        """返回观察列表股票的字符串表示"""
        return f"<WatchListStock {self.stock_code} in WatchList {self.watchlist_id}>" 