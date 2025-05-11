"""
股票系统 - 股票数据服务
"""
import os
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple

from app import db
from app.models.stock import Stock, StockQuote, StockFinancial


# 日志配置
logger = logging.getLogger(__name__)


def get_stock_price(stock_code: str) -> float:
    """
    获取股票当前价格
    
    Args:
        stock_code: 股票代码
    
    Returns:
        float: 当前价格
    """
    try:
        # 优先从数据库获取最新价格
        stock = Stock.query.filter_by(code=stock_code).first()
        if stock:
            quote = stock.get_latest_quote()
            if quote and (datetime.now().date() - quote.date).days <= 7:
                return quote.close_price
        
        # 否则从API获取实时价格
        stock_data = fetch_realtime_stock_data(stock_code)
        if stock_data and 'price' in stock_data:
            return stock_data['price']
        
        # 如果都失败，则返回默认值或抛出异常
        raise ValueError(f"无法获取股票 {stock_code} 的价格")
    except Exception as e:
        logger.error(f"获取股票价格失败: {str(e)}")
        raise


def get_stock_data(stock_code: str) -> Dict[str, Any]:
    """
    获取股票综合数据
    
    Args:
        stock_code: 股票代码
    
    Returns:
        Dict: 股票数据字典
    """
    try:
        # 查询股票基本信息
        stock = Stock.query.filter_by(code=stock_code).first()
        
        # 如果数据库中不存在该股票，则从API获取并保存
        if not stock:
            stock_info = fetch_stock_info(stock_code)
            if not stock_info:
                raise ValueError(f"无法获取股票 {stock_code} 的信息")
                
            stock = Stock(
                code=stock_code,
                name=stock_info.get('name', '未知'),
                market=stock_info.get('market', '未知'),
                full_name=stock_info.get('full_name'),
                industry=stock_info.get('industry')
            )
            db.session.add(stock)
            db.session.commit()
        
        # 获取最新行情
        latest_quote = stock.get_latest_quote()
        if not latest_quote or (datetime.now().date() - latest_quote.date).days > 0:
            # 从API获取最新行情并保存
            try:
                quote_data = fetch_realtime_stock_data(stock_code)
                if quote_data:
                    update_stock_quote(stock.id, quote_data)
                    latest_quote = stock.get_latest_quote()
            except Exception as e:
                logger.warning(f"获取实时行情失败: {str(e)}")
        
        # 构建返回数据
        result = stock.get_basic_info()
        if latest_quote:
            result.update({
                'price': latest_quote.close_price,
                'open': latest_quote.open_price,
                'high': latest_quote.high_price,
                'low': latest_quote.low_price,
                'change': latest_quote.change,
                'change_percent': latest_quote.change_percent,
                'volume': latest_quote.volume,
                'turnover': latest_quote.turnover,
                'date': latest_quote.date.strftime('%Y-%m-%d')
            })
        
        # 获取财务数据
        latest_financial = stock.financials.order_by(StockFinancial.report_date.desc()).first()
        if latest_financial:
            result.update({
                'eps': latest_financial.eps,
                'pe_ratio': latest_financial.pe_ratio,
                'pb_ratio': latest_financial.pb_ratio,
                'roe': latest_financial.roe,
                'dividend_yield': latest_financial.dividend_yield,
                'financial_date': latest_financial.report_date.strftime('%Y-%m-%d')
            })
        
        return result
    except Exception as e:
        logger.error(f"获取股票数据失败: {str(e)}")
        # 返回最小数据集，避免前端错误
        return {
            'stock_code': stock_code,
            'stock_name': '获取失败',
            'error': str(e)
        }


def get_stock_k_line(stock_code: str, period: str = 'daily', 
                    start_date: Optional[str] = None, 
                    end_date: Optional[str] = None,
                    limit: int = 90) -> List[Dict[str, Any]]:
    """
    获取股票K线数据
    
    Args:
        stock_code: 股票代码
        period: 周期，如'daily', 'weekly', 'monthly'
        start_date: 开始日期，格式'YYYY-MM-DD'
        end_date: 结束日期，格式'YYYY-MM-DD'
        limit: 数据条数限制
    
    Returns:
        List[Dict]: K线数据列表
    """
    try:
        stock = Stock.query.filter_by(code=stock_code).first()
        if not stock:
            raise ValueError(f"股票 {stock_code} 不存在")
        
        # 解析日期
        end_dt = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else datetime.now().date()
        if start_date:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            # 默认获取最近limit天的数据
            start_dt = end_dt - timedelta(days=limit * 2)  # 乘2是为了兼顾非交易日
        
        # 查询数据库中的K线数据
        quotes = stock.quotes.filter(
            StockQuote.date >= start_dt,
            StockQuote.date <= end_dt
        ).order_by(StockQuote.date).all()
        
        # 如果数据不足，尝试从API获取并保存
        if len(quotes) < min(limit, (end_dt - start_dt).days / 2):
            try:
                kline_data = fetch_stock_kline(stock_code, period, start_date, end_date)
                if kline_data:
                    bulk_update_stock_quotes(stock.id, kline_data)
                    # 重新查询
                    quotes = stock.quotes.filter(
                        StockQuote.date >= start_dt,
                        StockQuote.date <= end_dt
                    ).order_by(StockQuote.date).all()
            except Exception as e:
                logger.warning(f"获取K线数据失败: {str(e)}")
        
        # 转换为前端所需格式
        result = [quote.to_dict() for quote in quotes[-limit:]]
        return result
    except Exception as e:
        logger.error(f"获取股票K线数据失败: {str(e)}")
        return []


def search_stocks(keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    搜索股票
    
    Args:
        keyword: 搜索关键词
        limit: 返回结果限制
    
    Returns:
        List[Dict]: 股票列表
    """
    try:
        # 先从数据库中搜索
        stocks = Stock.query.filter(
            (Stock.code.like(f'%{keyword}%')) | 
            (Stock.name.like(f'%{keyword}%'))
        ).limit(limit).all()
        
        # 如果结果太少，可以考虑从API获取更多
        if len(stocks) < limit:
            try:
                api_results = fetch_stock_search(keyword, limit - len(stocks))
                if api_results:
                    for result in api_results:
                        # 检查是否已存在
                        if not Stock.query.filter_by(code=result['code']).first():
                            stock = Stock(
                                code=result['code'],
                                name=result['name'],
                                market=result.get('market', '未知')
                            )
                            db.session.add(stock)
                    db.session.commit()
                    
                    # 重新查询
                    stocks = Stock.query.filter(
                        (Stock.code.like(f'%{keyword}%')) | 
                        (Stock.name.like(f'%{keyword}%'))
                    ).limit(limit).all()
            except Exception as e:
                logger.warning(f"API搜索股票失败: {str(e)}")
        
        # 构建返回结果
        result = []
        for stock in stocks:
            stock_data = {
                'code': stock.code,
                'name': stock.name,
                'market': stock.market
            }
            
            # 获取最新价格
            latest_quote = stock.get_latest_quote()
            if latest_quote:
                stock_data.update({
                    'price': latest_quote.close_price,
                    'change_percent': latest_quote.change_percent
                })
                
            result.append(stock_data)
            
        return result
    except Exception as e:
        logger.error(f"搜索股票失败: {str(e)}")
        return []


# 以下是与外部API交互的函数

def fetch_stock_info(stock_code: str) -> Dict[str, Any]:
    """
    从API获取股票基本信息
    
    Args:
        stock_code: 股票代码
    
    Returns:
        Dict: 股票基本信息
    """
    # TODO: 实现实际的API调用
    # 由于目前没有实际的API，这里返回模拟数据
    logger.info(f"使用模拟数据替代API调用: fetch_stock_info({stock_code})")
    
    # 模拟常见股票数据
    mock_data = {
        '600000': {'name': '浦发银行', 'market': 'SH', 'industry': '银行', 'full_name': '上海浦东发展银行股份有限公司'},
        '601398': {'name': '工商银行', 'market': 'SH', 'industry': '银行', 'full_name': '中国工商银行股份有限公司'},
        '000001': {'name': '平安银行', 'market': 'SZ', 'industry': '银行', 'full_name': '平安银行股份有限公司'},
        '601288': {'name': '农业银行', 'market': 'SH', 'industry': '银行', 'full_name': '中国农业银行股份有限公司'},
        '601988': {'name': '中国银行', 'market': 'SH', 'industry': '银行', 'full_name': '中国银行股份有限公司'},
        '600519': {'name': '贵州茅台', 'market': 'SH', 'industry': '白酒', 'full_name': '贵州茅台酒股份有限公司'},
        '000858': {'name': '五粮液', 'market': 'SZ', 'industry': '白酒', 'full_name': '宜宾五粮液股份有限公司'},
        '601318': {'name': '中国平安', 'market': 'SH', 'industry': '保险', 'full_name': '中国平安保险(集团)股份有限公司'},
        '600036': {'name': '招商银行', 'market': 'SH', 'industry': '银行', 'full_name': '招商银行股份有限公司'},
        '000651': {'name': '格力电器', 'market': 'SZ', 'industry': '家电', 'full_name': '珠海格力电器股份有限公司'},
        '600887': {'name': '伊利股份', 'market': 'SH', 'industry': '食品饮料', 'full_name': '内蒙古伊利实业集团股份有限公司'},
        '601857': {'name': '中国石油', 'market': 'SH', 'industry': '石油石化', 'full_name': '中国石油天然气股份有限公司'},
    }
    
    # 提供一个默认的股票信息
    default_info = {
        'name': f'未知股票{stock_code}',
        'market': '未知',
        'industry': '未知',
        'full_name': f'未知股票{stock_code}'
    }
    
    return mock_data.get(stock_code, default_info)


def fetch_realtime_stock_data(stock_code: str) -> Dict[str, Any]:
    """
    从API获取股票实时数据
    
    Args:
        stock_code: 股票代码
    
    Returns:
        Dict: 股票实时数据
    """
    # TODO: 实现实际的API调用
    # 由于目前没有实际的API，这里返回模拟数据
    logger.info(f"使用模拟数据替代API调用: fetch_realtime_stock_data({stock_code})")
    
    import random
    from datetime import datetime, timedelta
    
    # 随机生成一个合理的价格
    base_price = 10.0 + (hash(stock_code) % 1000) / 10.0
    price = round(base_price * (1 + random.uniform(-0.05, 0.05)), 2)
    
    # 基于价格生成其他数据
    open_price = round(price * (1 + random.uniform(-0.02, 0.02)), 2)
    high_price = round(max(open_price, price) * (1 + random.uniform(0, 0.02)), 2)
    low_price = round(min(open_price, price) * (1 - random.uniform(0, 0.02)), 2)
    
    # 生成涨跌幅
    prev_close = round(price / (1 + random.uniform(-0.05, 0.05)), 2)
    change = round(price - prev_close, 2)
    change_percent = round(change / prev_close * 100, 2)
    
    # 生成成交量和成交额
    volume = random.randint(10000, 10000000)
    turnover = round(volume * price / 100, 2)
    
    # 当前日期，如果是周末则取最近的周五
    today = datetime.now().date()
    if today.weekday() > 4:  # 0是周一，5是周六，6是周日
        today = today - timedelta(days=today.weekday() - 4)
    
    return {
        'stock_code': stock_code,
        'date': today.strftime('%Y-%m-%d'),
        'price': price,
        'open': open_price,
        'high': high_price,
        'low': low_price,
        'prev_close': prev_close,
        'change': change,
        'change_percent': change_percent,
        'volume': volume,
        'turnover': turnover
    }


def fetch_stock_kline(stock_code: str, period: str = 'daily', 
                    start_date: Optional[str] = None, 
                    end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    从API获取股票K线数据
    
    Args:
        stock_code: 股票代码
        period: 周期，如'daily', 'weekly', 'monthly'
        start_date: 开始日期，格式'YYYY-MM-DD'
        end_date: 结束日期，格式'YYYY-MM-DD'
    
    Returns:
        List[Dict]: K线数据列表
    """
    # TODO: 实现实际的API调用
    # 由于目前没有实际的API，这里返回模拟数据
    logger.info(f"使用模拟数据替代API调用: fetch_stock_kline({stock_code}, {period}, {start_date}, {end_date})")
    
    import random
    
    # 解析日期
    end_dt = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else datetime.now().date()
    # 如果是周末，调整到最近的工作日
    if end_dt.weekday() > 4:
        end_dt = end_dt - timedelta(days=end_dt.weekday() - 4)
        
    if start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        # 默认获取30个交易日的数据
        start_dt = end_dt - timedelta(days=30 * 7 // 5)  # 考虑周末和节假日
    
    # 基于股票代码生成一个基础价格
    base_price = 10.0 + (hash(stock_code) % 1000) / 10.0
    current_price = base_price
    
    result = []
    current_dt = start_dt
    
    while current_dt <= end_dt:
        # 跳过周末
        if current_dt.weekday() < 5:  # 0-4为周一至周五
            # 随机生成涨跌幅
            change_percent = random.uniform(-2.0, 2.0)
            close_price = round(current_price * (1 + change_percent / 100), 2)
            
            # 生成开盘价、最高价和最低价
            open_price = round(current_price * (1 + random.uniform(-1.0, 1.0) / 100), 2)
            high_price = round(max(open_price, close_price) * (1 + random.uniform(0, 1.0) / 100), 2)
            low_price = round(min(open_price, close_price) * (1 - random.uniform(0, 1.0) / 100), 2)
            
            # 生成成交量
            volume = random.randint(5000000, 50000000)
            
            # 生成成交额
            turnover = round(volume * (open_price + close_price) / 2 / 10000, 2)
            
            # 计算涨跌额
            change = round(close_price - current_price, 2)
            
            result.append({
                'date': current_dt.strftime('%Y-%m-%d'),
                'open': open_price,
                'close': close_price,
                'high': high_price,
                'low': low_price,
                'volume': volume,
                'turnover': turnover,
                'change': change,
                'change_percent': round(change_percent, 2)
            })
            
            current_price = close_price
            
        current_dt += timedelta(days=1)
    
    return result


def fetch_stock_search(keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    从API搜索股票
    
    Args:
        keyword: 搜索关键词
        limit: 返回结果限制
    
    Returns:
        List[Dict]: 股票列表
    """
    # TODO: 实现实际的API调用
    # 由于目前没有实际的API，这里返回模拟数据
    logger.info(f"使用模拟数据替代API调用: fetch_stock_search({keyword}, {limit})")
    
    # 模拟搜索结果
    all_stocks = [
        {'code': '600000', 'name': '浦发银行', 'market': 'SH'},
        {'code': '601398', 'name': '工商银行', 'market': 'SH'},
        {'code': '000001', 'name': '平安银行', 'market': 'SZ'},
        {'code': '601288', 'name': '农业银行', 'market': 'SH'},
        {'code': '601988', 'name': '中国银行', 'market': 'SH'},
        {'code': '600519', 'name': '贵州茅台', 'market': 'SH'},
        {'code': '000858', 'name': '五粮液', 'market': 'SZ'},
        {'code': '601318', 'name': '中国平安', 'market': 'SH'},
        {'code': '600036', 'name': '招商银行', 'market': 'SH'},
        {'code': '000651', 'name': '格力电器', 'market': 'SZ'},
        {'code': '600887', 'name': '伊利股份', 'market': 'SH'},
        {'code': '601857', 'name': '中国石油', 'market': 'SH'},
    ]
    
    # 根据关键词过滤
    filtered_stocks = []
    for stock in all_stocks:
        if keyword.lower() in stock['code'].lower() or keyword.lower() in stock['name'].lower():
            filtered_stocks.append(stock)
    
    return filtered_stocks[:limit]


# 辅助函数

def update_stock_quote(stock_id: int, quote_data: Dict[str, Any]) -> None:
    """
    更新股票行情数据
    
    Args:
        stock_id: 股票ID
        quote_data: 行情数据
    """
    try:
        # 解析日期
        if 'date' in quote_data:
            date = datetime.strptime(quote_data['date'], '%Y-%m-%d').date()
        else:
            date = datetime.now().date()
        
        # 查找是否已存在该日期的行情
        quote = StockQuote.query.filter_by(stock_id=stock_id, date=date).first()
        
        if not quote:
            # 创建新行情记录
            quote = StockQuote(
                stock_id=stock_id,
                date=date,
                open_price=quote_data.get('open'),
                close_price=quote_data.get('price') or quote_data.get('close'),
                high_price=quote_data.get('high'),
                low_price=quote_data.get('low'),
                volume=quote_data.get('volume'),
                turnover=quote_data.get('turnover'),
                change=quote_data.get('change'),
                change_percent=quote_data.get('change_percent')
            )
            db.session.add(quote)
        else:
            # 更新已有行情
            quote.open_price = quote_data.get('open', quote.open_price)
            quote.close_price = quote_data.get('price') or quote_data.get('close', quote.close_price)
            quote.high_price = quote_data.get('high', quote.high_price)
            quote.low_price = quote_data.get('low', quote.low_price)
            quote.volume = quote_data.get('volume', quote.volume)
            quote.turnover = quote_data.get('turnover', quote.turnover)
            quote.change = quote_data.get('change', quote.change)
            quote.change_percent = quote_data.get('change_percent', quote.change_percent)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"更新股票行情失败: {str(e)}")
        raise


def bulk_update_stock_quotes(stock_id: int, quotes_data: List[Dict[str, Any]]) -> None:
    """
    批量更新股票行情数据
    
    Args:
        stock_id: 股票ID
        quotes_data: 行情数据列表
    """
    try:
        # 收集所有日期
        dates = [datetime.strptime(q['date'], '%Y-%m-%d').date() for q in quotes_data]
        
        # 查询已存在的记录
        existing_quotes = {
            q.date: q for q in StockQuote.query.filter(
                StockQuote.stock_id == stock_id,
                StockQuote.date.in_(dates)
            ).all()
        }
        
        # 批量添加或更新
        for quote_data in quotes_data:
            date = datetime.strptime(quote_data['date'], '%Y-%m-%d').date()
            
            if date in existing_quotes:
                # 更新已有记录
                quote = existing_quotes[date]
                quote.open_price = quote_data.get('open', quote.open_price)
                quote.close_price = quote_data.get('close', quote.close_price)
                quote.high_price = quote_data.get('high', quote.high_price)
                quote.low_price = quote_data.get('low', quote.low_price)
                quote.volume = quote_data.get('volume', quote.volume)
                quote.turnover = quote_data.get('turnover', quote.turnover)
                quote.change = quote_data.get('change', quote.change)
                quote.change_percent = quote_data.get('change_percent', quote.change_percent)
            else:
                # 创建新记录
                quote = StockQuote(
                    stock_id=stock_id,
                    date=date,
                    open_price=quote_data.get('open'),
                    close_price=quote_data.get('close'),
                    high_price=quote_data.get('high'),
                    low_price=quote_data.get('low'),
                    volume=quote_data.get('volume'),
                    turnover=quote_data.get('turnover'),
                    change=quote_data.get('change'),
                    change_percent=quote_data.get('change_percent')
                )
                db.session.add(quote)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"批量更新股票行情失败: {str(e)}")
        raise 