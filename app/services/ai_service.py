"""
股票系统 - AI服务
"""
import os
import requests
import json
import logging
from typing import Dict, Any, Optional, List

from flask import current_app


class AIService:
    """AI模型服务封装类"""
    
    def __init__(self, model_name: Optional[str] = None, api_key: Optional[str] = None, api_url: Optional[str] = None):
        """
        初始化AI服务
        
        Args:
            model_name: AI模型名称，例如 'wenxin', 'ernie', 'chatglm'
            api_key: API密钥
            api_url: API URL
        """
        self.model_name = model_name or current_app.config.get('AI_MODEL_NAME', 'wenxin')
        self.api_key = api_key or current_app.config.get('AI_API_KEY', '')
        self.api_url = api_url or current_app.config.get('AI_API_URL', '')
        self.logger = logging.getLogger(__name__)
    
    def _prepare_message(self, prompt: str, system_message: Optional[str] = None) -> List[Dict[str, str]]:
        """
        准备消息格式
        
        Args:
            prompt: 用户输入的提示词
            system_message: 系统消息（指导模型的行为）
            
        Returns:
            List: 格式化的消息列表
        """
        messages = []
        
        # 添加系统消息
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        # 添加用户消息
        messages.append({"role": "user", "content": prompt})
        
        return messages
    
    def _make_api_request(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[str, Any]:
        """
        发送API请求到AI模型服务
        
        Args:
            messages: 消息列表
            temperature: 温度参数，控制回答的随机性
            
        Returns:
            Dict: API响应
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self._get_model_identifier(),
                "messages": messages,
                "temperature": temperature
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            self.logger.error(f"AI API请求失败: {str(e)}")
            return {"error": str(e)}
    
    def _get_model_identifier(self) -> str:
        """
        根据配置的模型名称获取完整的模型标识符
        
        Returns:
            str: 模型标识符
        """
        model_mapping = {
            "wenxin": "ERNIE-Bot-4",  # 百度文言一心
            "ernie": "ERNIE-Bot",     # 百度文心一言
            "chatglm": "chatglm2-6b", # 智谱ChatGLM
            # 可以添加其他模型
        }
        
        return model_mapping.get(self.model_name.lower(), self.model_name)
    
    def analyze_market(self, timeframe: str = "short") -> Dict[str, Any]:
        """
        分析市场趋势
        
        Args:
            timeframe: 时间范围，可选 'short', 'medium', 'long'
            
        Returns:
            Dict: 分析结果
        """
        time_descriptions = {
            "short": "短期（1-7天）",
            "medium": "中期（1-3个月）",
            "long": "长期（3-12个月）"
        }
        
        system_message = (
            "你是一个专业的股市分析师，擅长分析市场趋势和预测可能的走势。"
            "请提供客观、全面和有洞察力的分析，包括可能的上涨因素和风险因素。"
            "请使用专业但通俗的语言，以便非专业投资者也能理解。"
        )
        
        prompt = (
            f"请分析当前市场的总体趋势，并给出{time_descriptions.get(timeframe, '短期')}市场展望。"
            "分析需要包括：\n"
            "1. 总体市场情绪评估\n"
            "2. 主要指数可能的走势\n"
            "3. 值得关注的行业板块\n"
            "4. 市场风险因素\n"
            "5. 投资建议"
        )
        
        messages = self._prepare_message(prompt, system_message)
        response = self._make_api_request(messages)
        
        # 处理响应
        if "error" in response:
            return {
                "success": False,
                "error": response["error"],
                "analysis": "无法获取市场分析，请稍后再试。"
            }
        
        # 提取回复内容
        try:
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # 简单情感分析逻辑
            sentiment = "neutral"
            if "看涨" in content or "积极" in content or "上涨" in content:
                sentiment = "bullish"
            elif "看跌" in content or "谨慎" in content or "下跌" in content:
                sentiment = "bearish"
            
            # 提取关键行业/股票
            import re
            trends = re.findall(r'([\u4e00-\u9fa5]{2,6}(?:板块|行业|股票|概念))', content)
            
            return {
                "success": True,
                "timeframe": timeframe,
                "analysis": content,
                "sentiment": sentiment,
                "trends": trends[:5]  # 最多返回5个趋势
            }
            
        except (KeyError, IndexError) as e:
            self.logger.error(f"处理AI响应时出错: {str(e)}")
            return {
                "success": False,
                "error": "处理响应时出错",
                "analysis": "无法解析分析结果，请稍后再试。"
            }
    
    def analyze_stock(self, code: str, aspects: List[str] = None) -> Dict[str, Any]:
        """
        分析个股
        
        Args:
            code: 股票代码
            aspects: 分析方面，例如 ['technical', 'fundamental', 'sentiment']
            
        Returns:
            Dict: 分析结果
        """
        if aspects is None:
            aspects = ['technical', 'fundamental', 'sentiment']
        
        aspects_map = {
            'technical': '技术面',
            'fundamental': '基本面',
            'sentiment': '市场情绪',
            'trend': '趋势',
            'risk': '风险'
        }
        
        aspects_str = '、'.join([aspects_map.get(a, a) for a in aspects])
        
        system_message = (
            "你是一个专业的股票分析师，擅长分析个股的各个方面。"
            "请提供客观、全面和有深度的分析，包括积极因素和风险因素。"
            "不要过度乐观或悲观，保持中立的专业态度。"
        )
        
        prompt = (
            f"请对股票代码 {code} 进行分析，重点关注以下方面：{aspects_str}。"
            "请包括：\n"
            "1. 该股票近期表现概述\n"
            "2. 主要优势和风险\n"
            "3. 估值分析\n"
            "4. 整体评级（买入/持有/卖出）及理由\n"
            "5. 需要关注的关键指标或事件"
        )
        
        messages = self._prepare_message(prompt, system_message)
        response = self._make_api_request(messages)
        
        # 处理响应
        if "error" in response:
            return {
                "success": False,
                "error": response["error"],
                "analysis": f"无法获取股票 {code} 的分析，请稍后再试。"
            }
        
        # 提取回复内容
        try:
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # 简单评级提取逻辑
            rating = "hold"  # 默认评级
            if "买入" in content or "推荐" in content:
                rating = "buy"
            elif "卖出" in content or "减持" in content:
                rating = "sell"
            
            return {
                "success": True,
                "code": code,
                "analysis": content,
                "aspects": aspects,
                "rating": rating
            }
            
        except (KeyError, IndexError) as e:
            self.logger.error(f"处理AI响应时出错: {str(e)}")
            return {
                "success": False,
                "error": "处理响应时出错",
                "analysis": f"无法解析股票 {code} 的分析结果，请稍后再试。"
            }
    
    def chat(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        投资智能问答
        
        Args:
            question: 用户问题
            context: 上下文信息
            
        Returns:
            Dict: 回答结果
        """
        if context is None:
            context = {}
        
        system_message = (
            "你是一个专业的投资顾问和股票市场专家，擅长回答有关股票、基金、投资策略和金融市场的问题。"
            "请提供准确、有帮助的回答，同时注明任何投资都有风险，你的建议仅供参考。"
            "如果你不确定答案，请诚实地说出来，不要提供错误信息。"
        )
        
        # 如果有上下文信息，添加到问题中
        context_str = ""
        if context:
            if 'stock_code' in context:
                context_str += f"关于股票 {context['stock_code']} 的问题：\n"
            if 'portfolio_id' in context:
                context_str += f"关于投资组合 #{context['portfolio_id']} 的问题：\n"
        
        prompt = f"{context_str}{question}"
        
        messages = self._prepare_message(prompt, system_message)
        response = self._make_api_request(messages, temperature=0.8)  # 稍高的temperature使回答更自然
        
        # 处理响应
        if "error" in response:
            return {
                "success": False,
                "error": response["error"],
                "answer": "很抱歉，我无法回答这个问题，请稍后再试。"
            }
        
        # 提取回复内容
        try:
            answer = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            return {
                "success": True,
                "question": question,
                "answer": answer
            }
            
        except (KeyError, IndexError) as e:
            self.logger.error(f"处理AI响应时出错: {str(e)}")
            return {
                "success": False,
                "error": "处理响应时出错",
                "answer": "很抱歉，我无法处理这个问题的回答，请稍后再试。"
            }


# 创建服务实例
ai_service = AIService() 