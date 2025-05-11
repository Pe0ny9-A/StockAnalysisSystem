"""
股票系统 - 股票模型
"""
from datetime import datetime
from typing import Dict, Any, List, Optional

from app import db


class Stock(db.Model):
    """股票基本信息模型"""
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(200))
    market = db.Column(db.String(20), nullable=False)  # 市场: SH(上海), SZ(深圳), HK(香港)
    industry = db.Column(db.String(50))
    is_index = db.Column(db.Boolean, default=False)  # 是否为指数
    is_active = db.Column(db.Boolean, default=True)  # 是否活跃(未退市)
    listing_date = db.Column(db.Date)  # 上市日期
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    quotes = db.relationship('StockQuote', backref='stock', lazy='dynamic',
                           cascade='all, delete-orphan')
    financials = db.relationship('StockFinancial', backref='stock', lazy='dynamic',
                               cascade='all, delete-orphan')
    
    def __init__(self, code: str, name: str, market: str, **kwargs):
        """初始化股票实例"""
        self.code = code
        self.name = name
        self.market = market
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def get_latest_quote(self) -> Optional['StockQuote']:
        """获取最新行情"""
        return self.quotes.order_by(StockQuote.date.desc()).first()
    
    def get_basic_info(self) -> Dict[str, Any]:
        """获取股票基本信息"""
        return {
            'code': self.code,
            'name': self.name,
            'full_name': self.full_name,
            'market': self.market,
            'industry': self.industry,
            'is_index': self.is_index,
            'listing_date': self.listing_date
        }
    
    def __repr__(self) -> str:
        """返回股票的字符串表示"""
        return f"<Stock {self.code} {self.name}>"


class StockQuote(db.Model):
    """股票行情数据模型"""
    __tablename__ = 'stock_quotes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    open_price = db.Column(db.Float)
    close_price = db.Column(db.Float)
    high_price = db.Column(db.Float)
    low_price = db.Column(db.Float)
    volume = db.Column(db.BigInteger)  # 成交量
    turnover = db.Column(db.Float)  # 成交额
    change = db.Column(db.Float)  # 涨跌额
    change_percent = db.Column(db.Float)  # 涨跌幅
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键关系
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    
    # 组合唯一约束，确保每个股票每天只有一条记录
    __table_args__ = (
        db.UniqueConstraint('stock_id', 'date', name='uix_stock_quote_date'),
    )
    
    def __init__(self, stock_id: int, date: datetime.date, **kwargs):
        """初始化股票行情数据实例"""
        self.stock_id = stock_id
        self.date = date
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'open': self.open_price,
            'close': self.close_price,
            'high': self.high_price,
            'low': self.low_price,
            'volume': self.volume,
            'turnover': self.turnover,
            'change': self.change,
            'change_percent': self.change_percent
        }
    
    def __repr__(self) -> str:
        """返回股票行情的字符串表示"""
        return f"<StockQuote {self.stock_id} on {self.date}>"


class StockFinancial(db.Model):
    """股票财务数据模型"""
    __tablename__ = 'stock_financials'

    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, nullable=False)  # 报告期
    report_type = db.Column(db.String(20), nullable=False)  # 报告类型: Q1, Q2, Q3, A(年报)
    revenue = db.Column(db.Float)  # 营业收入(百万元)
    net_profit = db.Column(db.Float)  # 净利润(百万元)
    eps = db.Column(db.Float)  # 每股收益(元)
    roe = db.Column(db.Float)  # 净资产收益率(%)
    pe_ratio = db.Column(db.Float)  # 市盈率
    pb_ratio = db.Column(db.Float)  # 市净率
    dividend_yield = db.Column(db.Float)  # 股息率(%)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键关系
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    
    # 组合唯一约束，确保每个股票每个报告期只有一条记录
    __table_args__ = (
        db.UniqueConstraint('stock_id', 'report_date', 'report_type', name='uix_stock_financial_report'),
    )
    
    def __init__(self, stock_id: int, report_date: datetime.date, report_type: str, **kwargs):
        """初始化股票财务数据实例"""
        self.stock_id = stock_id
        self.report_date = report_date
        self.report_type = report_type
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'report_date': self.report_date.strftime('%Y-%m-%d'),
            'report_type': self.report_type,
            'revenue': self.revenue,
            'net_profit': self.net_profit,
            'eps': self.eps,
            'roe': self.roe,
            'pe_ratio': self.pe_ratio,
            'pb_ratio': self.pb_ratio,
            'dividend_yield': self.dividend_yield
        }
    
    def __repr__(self) -> str:
        """返回股票财务数据的字符串表示"""
        return f"<StockFinancial {self.stock_id} {self.report_type} {self.report_date}>" 