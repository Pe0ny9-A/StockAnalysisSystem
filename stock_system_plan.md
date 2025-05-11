# 股票系统Web项目规划

## 项目概述
股票系统Web应用将提供股票数据查询、分析和交易功能，帮助用户进行投资决策。本系统主要面向个人投资者，提供模拟交易和实时行情功能，帮助用户在安全环境中学习和实践股票投资策略。

## 核心功能模块

### 1. 用户管理
- **注册/登录/找回密码**
  - 多种注册方式：邮箱、手机号
  - 密码安全策略：强制要求密码复杂度
  - 二次验证：邮箱验证码或短信验证码
  - 找回密码流程：身份验证与重置机制
  - JWT令牌认证：管理用户会话

- **个人资料管理**
  - 个人基本信息：昵称、头像、联系方式
  - 安全设置：修改密码、绑定手机/邮箱
  - 通知设置：自定义通知偏好（邮件、站内信）
  - 操作日志：记录重要账户操作

- **权限控制**
  - 角色划分：普通用户、VIP用户、管理员
  - 功能权限：不同角色可访问的功能模块
  - 数据权限：可查看的数据范围与敏感数据处理

- **账户安全**
  - 异常登录检测：IP异常、设备异常提醒
  - 敏感操作验证：资金操作二次验证
  - 账户锁定机制：连续失败登录处理

### 2. 行情数据展示
- **实时股票价格**
  - 价格推送：使用WebSocket实时更新
  - 自动刷新机制：可配置刷新频率
  - 价格变动可视化：上涨/下跌颜色区分
  - 交易量实时显示：成交量柱状图
  - 盘口信息：买卖五档、盘口分析

- **K线图表**
  - 多时间周期：分钟、小时、日、周、月
  - 图表类型：蜡烛图、美国线、面积图等
  - 缩放与拖拽：交互式查看历史数据
  - 技术指标叠加：可选择多种指标同时显示
  - 绘图工具：趋势线、斐波那契、通道等
  - 自定义设置：颜色、样式个性化配置

- **成交量分析**
  - 量价关系图：价格与成交量对比
  - 大单分析：大额交易识别
  - 主力资金流向：资金流入/流出统计
  - 换手率统计：日/周换手率分析
  - 成交量异常检测：放量缩量提示

- **大盘指数**
  - 主要指数实时行情：上证、深证、创业板等
  - 行业板块指数：各行业涨跌幅对比
  - 市场宽度指标：涨跌家数、强弱指标
  - 热点板块轮动：行业资金流向图
  - 国际市场联动：全球主要指数对比

- **自定义行情监控**
  - 自选股票组合：创建多个自选股分组
  - 条件筛选：按涨跌幅、成交量等条件筛选
  - 行情预警：设置价格突破、量能异常等提醒
  - 数据导出：导出CSV或Excel格式数据

### 3. 个人投资组合
- **自选股管理**
  - 分组管理：创建不同投资主题的分组
  - 批量操作：批量添加、删除自选股
  - 排序与筛选：按自定义规则排序显示
  - 备注功能：为每只股票添加个人备注
  - 关注度统计：热门关注股票排行

- **持仓展示**
  - 持仓明细：股票、持仓数量、成本价
  - 持仓市值：实时计算当前市值
  - 盈亏计算：实时、日、周、月盈亏统计
  - 持仓结构：饼图展示持仓分布
  - 风险评估：波动率、最大回撤计算
  - 历史持仓查询：按时间段查询持仓历史

- **收益分析**
  - 收益概览：总收益、年化收益率
  - 收益构成：投资收益、股息收益
  - 收益曲线：资产价值走势图
  - 与基准对比：与指数、其他用户对比
  - 绩效评估：夏普比率、信息比率等指标
  - 月度/季度/年度报表：定期收益总结

- **交易记录**
  - 交易明细：所有买卖操作记录
  - 交易统计：频率、成功率分析
  - 成本分析：平均建仓成本计算
  - 交易日志：重要交易决策记录
  - 交易复盘：历史交易回顾与分析

- **投资策略管理**
  - 策略创建：定义买入卖出规则
  - 策略回测：历史数据验证策略有效性
  - 策略执行：自动或半自动执行交易
  - 策略优化：参数优化、收益对比

### 4. 交易系统
- **买入/卖出操作**
  - 交易界面：简洁直观的下单界面
  - 多种订单类型：市价单、限价单、止损单
  - 快速交易：一键买入卖出功能
  - 交易确认：重要操作二次确认
  - 资金计算：自动计算手续费、税费
  - 仓位管理：仓位控制与资金分配建议

- **委托单管理**
  - 当日委托：实时显示委托状态
  - 历史委托：可查询任意时间段委托记录
  - 批量操作：批量撤单、修改功能
  - 条件单设置：设置触发价格自动下单
  - 委托转化率：委托成交分析

- **模拟交易**
  - 虚拟资金：初始资金配置
  - 真实行情：基于实时行情进行模拟
  - 交易规则：与实盘交易规则一致
  - 竞赛功能：用户间模拟交易比赛
  - 模拟情景：模拟不同市场环境下的交易

- **资金管理**
  - 资金明细：账户资金流水
  - 入金出金：模拟充值提现操作
  - 资金分析：使用率、周转率分析
  - 风险控制：单笔交易风险提示
  - 杠杆配置：配资杠杆模拟（如适用）

- **交易通知**
  - 委托成交通知：及时推送成交结果
  - 价格预警：价格达到预设值通知
  - 异常交易提醒：大额交易、频繁交易提示
  - 通知渠道：站内信、邮件、短信等
  - 定制化通知：自定义通知条件和频率

### 5. 分析工具
- **技术指标(MACD/KDJ等)**
  - 常用指标：MA、MACD、KDJ、RSI等
  - 自定义指标：创建组合指标
  - 指标参数调整：修改计算周期等参数
  - 指标预警：设置指标交叉等预警条件
  - 指标模板：保存常用指标组合

- **基本面数据**
  - 财务报表：季报、年报数据展示
  - 财务比率：盈利能力、偿债能力等
  - 估值指标：PE、PB、PS等估值参数
  - 行业对比：同行业公司数据对比
  - 股东信息：主要股东、持股变动
  - 公司概况：公司简介、高管、业务范围

- **新闻资讯整合**
  - 市场动态：大盘、行业最新动态
  - 个股新闻：关注股票的相关新闻
  - 公告信息：上市公司公告集成
  - 研报摘要：券商研究报告摘要
  - 资讯筛选：自定义关键词筛选
  - 情绪分析：市场情绪指标监控

- **量化分析**
  - 因子分析：多因子模型构建
  - 相关性分析：股票间相关性计算
  - 风险评估：VaR、最大回撤等计算
  - 策略回测：历史数据策略验证
  - 指标扫描：按指标条件筛选股票

- **市场热度分析**
  - 热门概念：当前市场热点追踪
  - 社交媒体分析：舆情监控与分析
  - 机构关注度：机构持仓与评级追踪
  - 板块轮动：行业资金流向分析
  - 热度排行：交易活跃度、关注度排名

### 6. AI智能分析

- **智能投顾服务**
  - 智能资产配置：基于用户风险偏好自动配置资产
  - 个性化投资建议：根据用户画像生成投资策略
  - 智能再平衡：自动检测并建议投资组合调整
  - 风险监控：AI持续监控投资组合风险
  - 市场异常检测：识别市场异常波动并提供应对建议

- **AI行情预测**
  - 价格走势预测：短期和中期价格趋势预测
  - 波动率预测：未来波动率估计与风险评估
  - 关键价位识别：支撑位和阻力位自动识别
  - 趋势转折点预警：识别可能的趋势转折点
  - 置信区间显示：预测结果显示可信度范围

- **智能文本分析**
  - 公告智能解读：自动分析公司公告关键内容
  - 研报摘要生成：长篇研报的关键信息提取
  - 新闻情绪分析：分析新闻报道的市场情绪影响
  - 社交媒体舆情：分析社交平台上的投资者情绪
  - 财报智能分析：自动解读财务报表关键指标变化

- **AI交易策略**
  - 策略生成：基于历史数据自动生成交易策略
  - 策略优化：自动调整策略参数以提高收益率
  - 机器学习模型：多种ML模型用于交易信号生成
  - 深度学习预测：使用神经网络预测市场走势
  - 回测与优化：策略自动回测与风险收益评估

- **智能问答助手**
  - 投资知识库：回答投资相关基础问题
  - 个股咨询：提供特定股票的各方面信息
  - 市场解读：解释市场动向和热点事件
  - 操作建议：提供交易操作的参考意见
  - 自然语言交互：支持自然语言对话方式查询信息

- **第三方AI集成**
  - 多模型接口：支持连接多种AI大模型(百度文言一心、硅基流动等)
  - API密钥管理：用户可配置自己的API密钥
  - 模型选择器：根据任务特点自动选择最合适的模型
  - 成本控制：Token使用量监控与限制
  - 自定义提示词：可定制化的AI提示模板

### 7. 系统设置与帮助
- **偏好设置**
  - 界面定制：主题、布局、颜色设置
  - 数据显示：自定义表格显示字段
  - 通知设置：推送时间、方式设置
  - 图表默认设置：默认周期、指标设置
  - AI功能配置：设置AI分析频率和范围

- **账户安全设置**
  - 登录保护：二次验证开关
  - 交易密码：单独的交易密码设置
  - 安全日志：账户安全操作记录
  - IP白名单：限制登录IP范围
  - AI权限设置：控制AI访问用户数据的权限范围

- **帮助与教程**
  - 新手引导：交互式使用指南
  - 功能说明：各模块详细说明文档
  - 视频教程：操作示范视频
  - 常见问题：FAQ与问题解答
  - 交易知识：投资与交易基础知识
  - AI功能指南：AI工具使用教程

- **反馈与支持**
  - 问题反馈：错误报告与建议提交
  - 客服支持：在线客服交流
  - 社区讨论：用户间交流平台
  - 版本更新：更新日志与公告

## 技术栈（一体化架构）

### 框架选择
- 主框架：Python Flask
- 模板引擎：Jinja2
- 前端库：Vue.js (CDN方式引入，非SPA模式)
- UI组件：Element UI
- 图表库：TradingView (轻量级版本)
- 数据库：MySQL
- ORM：SQLAlchemy
- 实时通信：Flask-SocketIO
- AI集成：OpenAI API、百度文心API、讯飞星火API等

### AI集成架构

- **模型接入层**
  - 多API适配器：支持各大模型API标准
  - 密钥管理：安全存储和使用API密钥
  - 请求限流：控制API请求频率与数量
  - 响应缓存：缓存通用问题的响应结果
  - 负载均衡：在多个模型间分配请求

- **AI中间件服务**
  - 提示词工程：优化提示词以获得更准确的结果
  - 上下文管理：维护对话历史与上下文信息
  - 结果解析：解析和格式化AI返回结果
  - 错误处理：处理API错误与超时情况
  - 功能路由：将不同任务分配给最适合的模型

- **数据准备与处理**
  - 数据清洗：准备AI输入数据
  - 格式转换：转换各类数据为模型可接受格式
  - 数据增强：添加必要的上下文信息
  - 敏感信息过滤：移除个人敏感信息
  - 批处理机制：高效处理大量数据请求

### 优势
- 简化部署流程，无需分别部署前后端服务
- 降低开发复杂度，适合初次接触此类项目的开发者
- 页面渲染由服务端完成，利于SEO
- 降低前后端数据交互成本
- AI分析提供高附加值服务，增强系统竞争力

## 功能流程与交互

### 用户注册与登录流程
1. 用户访问系统首页，点击"注册"按钮
2. 填写用户名、邮箱、密码等基本信息
3. 系统发送验证邮件到用户邮箱
4. 用户验证邮箱后，账户激活完成
5. 返回登录页面，输入账号密码登录
6. 登录成功后进入系统主界面

### 股票查询与添加自选流程
1. 用户在搜索框输入股票代码或名称
2. 系统实时显示匹配的股票列表
3. 用户点击感兴趣的股票查看详情
4. 股票详情页显示实时价格、K线图等信息
5. 用户点击"添加自选"按钮
6. 系统提示添加成功，并更新自选股列表

### 模拟交易操作流程
1. 用户在股票详情页点击"买入"按钮
2. 系统弹出交易界面，默认显示当前价格
3. 用户输入购买数量，系统计算预估金额
4. 用户确认交易信息，点击"确认买入"
5. 系统验证资金是否充足，执行买入操作
6. 交易成功后，更新持仓信息和资金余额
7. 系统发送交易成功通知

### 投资组合分析流程
1. 用户进入"我的组合"页面
2. 系统显示当前持仓概览和收益统计
3. 用户可选择不同时间段查看收益曲线
4. 点击"分析"按钮，系统生成详细分析报告
5. 报告包含收益构成、风险指标、业绩归因等
6. 用户可导出报告或设置定期发送功能

### AI智能分析流程
1. 用户在股票详情页点击"AI分析"按钮
2. 系统显示分析选项（基本面分析、技术分析、舆情分析等）
3. 用户选择所需分析类型后，系统开始处理
4. 系统调用相应的第三方AI模型进行分析
5. 分析完成后，以可视化图表和自然语言呈现结果
6. 用户可保存分析结果或根据建议执行操作
7. 系统记录分析历史，供用户后续参考

## AI分析具体应用场景

### 个股深度分析
- **应用场景**：用户需要全面了解某只股票的投资价值
- **功能流程**：
  1. 用户选择目标股票，点击"AI深度分析"
  2. 系统收集该股票的基本面数据、技术指标、新闻舆情等
  3. 调用AI模型进行综合分析，生成投资建议报告
  4. 以易懂的语言和可视化方式呈现分析结果
  5. 提供风险提示和潜在投资机会分析

### 市场情绪分析
- **应用场景**：判断整体市场情绪，辅助大盘走势判断
- **功能流程**：
  1. 系统自动收集金融新闻、社交媒体讨论等数据
  2. AI模型分析文本内容，提取市场情绪指标
  3. 生成市场情绪指数，并与历史数据对比
  4. 向用户展示市场情绪变化趋势和异常点
  5. 提供情绪指标与市场走势的关联分析

### 个性化投资建议
- **应用场景**：根据用户风险偏好和投资目标提供定制化建议
- **功能流程**：
  1. 用户完成风险评估问卷，设定投资目标
  2. AI分析用户交易历史和偏好
  3. 结合市场状况，生成个性化资产配置方案
  4. 推荐符合用户风险偏好的具体投资标的
  5. 定期优化和调整投资建议

## 项目结构

```
stock_system/
├── app/
│   ├── static/                 # 静态资源
│   │   ├── css/                # 样式文件
│   │   ├── js/                 # JavaScript文件
│   │   │   ├── components/     # Vue组件
│   │   │   ├── charts/         # 图表相关
│   │   │   └── utils/          # 工具函数
│   │   └── img/                # 图片资源
│   ├── templates/              # 模板文件
│   │   ├── base.html           # 基础模板
│   │   ├── auth/               # 认证相关页面
│   │   ├── dashboard/          # 主面板页面
│   │   ├── stock/              # 股票详情页面
│   │   ├── portfolio/          # 投资组合页面
│   │   ├── trading/            # 交易页面
│   │   └── ai_analysis/        # AI分析页面
│   ├── models/                 # 数据模型
│   │   ├── user.py             # 用户模型
│   │   ├── stock.py            # 股票模型
│   │   ├── portfolio.py        # 组合模型
│   │   ├── trading.py          # 交易模型
│   │   └── ai_analysis.py      # AI分析模型
│   ├── controllers/            # 控制器/路由
│   │   ├── auth.py             # 认证相关
│   │   ├── main.py             # 主页及通用路由
│   │   ├── stock.py            # 股票数据相关
│   │   ├── portfolio.py        # 投资组合相关
│   │   ├── trading.py          # 交易相关
│   │   └── ai_controller.py    # AI功能控制器
│   ├── services/               # 业务逻辑
│   │   ├── stock_data.py       # 股票数据服务
│   │   ├── portfolio.py        # 组合管理服务
│   │   ├── trading.py          # 交易服务
│   │   └── ai_service.py       # AI分析服务
│   ├── utils/                  # 工具函数
│   │   ├── data_fetcher.py     # 数据获取
│   │   ├── calculator.py       # 指标计算
│   │   └── ai_connector.py     # AI API连接器
│   ├── __init__.py             # 应用初始化
│   ├── config.py               # 配置文件
│   └── extensions.py           # 扩展模块初始化
├── migrations/                 # 数据库迁移文件
├── tests/                      # 测试代码
├── venv/                       # 虚拟环境
├── requirements.txt            # 依赖管理
├── run.py                      # 应用入口
└── .env                        # 环境变量
```

## 核心依赖

```
# 后端框架
Flask>=2.2.0
Flask-SQLAlchemy>=3.0.0
Flask-Migrate>=4.0.0
Flask-Login>=0.6.0
Flask-WTF>=1.1.0
Flask-SocketIO>=5.3.0
SQLAlchemy>=2.0.0
pymysql>=1.0.2
pandas>=1.5.0
numpy>=1.24.0
requests>=2.28.0
python-dotenv>=1.0.0

# 前端依赖通过CDN方式引入，无需在Python依赖中体现
# 主要包括Vue.js、Element UI、ECharts/TradingView等
```

## 页面与路由设计

### 主要页面结构

1. **认证页面**
   - 登录：`/auth/login`
   - 注册：`/auth/register`
   - 找回密码：`/auth/reset-password`

2. **主面板**
   - 仪表盘：`/dashboard`
   - 市场概览：`/dashboard/market`

3. **股票相关**
   - 股票列表：`/stocks`
   - 股票详情：`/stocks/<symbol>`
   - 行情分析：`/stocks/<symbol>/analysis`

4. **投资组合**
   - 组合列表：`/portfolios`
   - 组合详情：`/portfolios/<id>`
   - 持仓分析：`/portfolios/<id>/analysis`

5. **交易中心**
   - 交易主页：`/trading`
   - 委托下单：`/trading/order`
   - 委托记录：`/trading/orders`
   - 成交历史：`/trading/history`

6. **用户中心**
   - 个人资料：`/user/profile`
   - 账户设置：`/user/settings`

## 前端实现

### 模板设计

使用Jinja2模板继承机制，构建基础布局:

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{% block title %}股票交易系统{% endblock %}</title>
    <!-- CSS引入 -->
    <link rel="stylesheet" href="https://unpkg.com/element-plus/dist/index.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <div id="app">
        <el-container>
            <!-- 侧边栏 -->
            <el-aside width="200px">
                {% include 'components/sidebar.html' %}
            </el-aside>
            
            <el-container>
                <!-- 顶部导航 -->
                <el-header>
                    {% include 'components/header.html' %}
                </el-header>
                
                <!-- 主要内容区 -->
                <el-main>
                    {% block content %}{% endblock %}
                </el-main>
                
                <!-- 页脚 -->
                <el-footer>
                    {% include 'components/footer.html' %}
                </el-footer>
            </el-container>
        </el-container>
    </div>

    <!-- JS引入 -->
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <script src="https://unpkg.com/element-plus"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 前端Vue组件与服务端结合

在每个页面中，通过Vue来增强前端交互:

```html
<!-- stocks/detail.html -->
{% extends 'base.html' %}

{% block title %}{{ stock.name }} - 股票详情{% endblock %}

{% block content %}
<div id="stock-detail">
    <el-card>
        <template #header>
            <div class="card-header">
                <h2>{{ stock.name }} ({{ stock.symbol }})</h2>
                <el-tag>{{ stock.market }}</el-tag>
            </div>
        </template>
        
        <!-- 价格信息 -->
        <div class="price-info">
            <h3>{% raw %}{{ price }}{% endraw %}</h3>
            <span :class="priceChangeClass">{% raw %}{{ priceChange }}{% endraw %}</span>
        </div>
        
        <!-- K线图表容器 -->
        <div id="chart-container" style="height: 400px;"></div>
        
        <!-- 交易按钮 -->
        <div class="action-buttons">
            <el-button type="success" @click="handleBuy">买入</el-button>
            <el-button type="danger" @click="handleSell">卖出</el-button>
            <el-button type="primary" @click="addToWatchlist">加入自选</el-button>
        </div>
    </el-card>
</div>
{% endblock %}

{% block extra_js %}
<!-- 传递服务端数据到前端 -->
<script>
    const stockData = {{ stock_data|tojson }};
    const historyData = {{ history_data|tojson }};
</script>

<!-- 图表库 -->
<script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>

<!-- 页面特定的Vue组件 -->
<script src="{{ url_for('static', filename='js/components/stock-detail.js') }}"></script>
{% endblock %}
```

对应的Vue组件:

```javascript
// static/js/components/stock-detail.js
const { createApp, ref, computed, onMounted } = Vue;

createApp({
    data() {
        return {
            price: stockData.last_price,
            priceChange: stockData.change,
            chart: null,
            socket: null
        }
    },
    computed: {
        priceChangeClass() {
            return this.priceChange >= 0 ? 'price-up' : 'price-down';
        }
    },
    methods: {
        initChart() {
            const container = document.getElementById('chart-container');
            this.chart = LightweightCharts.createChart(container, {
                width: container.clientWidth,
                height: container.clientHeight
            });
            
            const candleSeries = this.chart.addCandlestickSeries();
            candleSeries.setData(historyData);
        },
        connectWebSocket() {
            this.socket = io('/stock');
            this.socket.on('connect', () => {
                this.socket.emit('subscribe', stockData.symbol);
            });
            
            this.socket.on('price_update', (data) => {
                if (data.symbol === stockData.symbol) {
                    this.price = data.price;
                    this.priceChange = data.change;
                }
            });
        },
        handleBuy() {
            window.location.href = `/trading/order?symbol=${stockData.symbol}&type=buy`;
        },
        handleSell() {
            window.location.href = `/trading/order?symbol=${stockData.symbol}&type=sell`;
        },
        addToWatchlist() {
            fetch('/api/watchlist/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
                },
                body: JSON.stringify({ symbol: stockData.symbol })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.$message.success('已加入自选股');
                } else {
                    this.$message.error(data.message || '操作失败');
                }
            });
        }
    },
    mounted() {
        this.initChart();
        this.connectWebSocket();
        
        // 响应式调整图表大小
        window.addEventListener('resize', () => {
            if (this.chart) {
                this.chart.resize(
                    document.getElementById('chart-container').clientWidth,
                    document.getElementById('chart-container').clientHeight
                );
            }
        });
    },
    beforeUnmount() {
        if (this.socket) {
            this.socket.disconnect();
        }
    }
}).use(ElementPlus).mount('#stock-detail');
```

## 后端实现

### 应用初始化

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO

from .config import Config

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    socketio.init_app(app)

    # 设置登录视图
    login_manager.login_view = 'auth.login'

    # 注册蓝图
    from app.controllers.auth import auth_bp
    from app.controllers.main import main_bp
    from app.controllers.stock import stock_bp
    from app.controllers.portfolio import portfolio_bp
    from app.controllers.trading import trading_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(trading_bp)

    return app
```

### 控制器示例

```python
# app/controllers/stock.py
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user

from app.models.stock import Stock, StockPrice
from app.services.stock_data import StockDataService

stock_bp = Blueprint('stock', __name__, url_prefix='/stocks')
stock_service = StockDataService()

@stock_bp.route('/')
@login_required
def stock_list():
    # 获取股票列表数据
    stocks = Stock.query.all()
    return render_template('stock/list.html', stocks=stocks)

@stock_bp.route('/<symbol>')
@login_required
def stock_detail(symbol):
    # 获取股票详情
    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    
    # 获取最新价格和历史数据
    stock_data = stock_service.get_latest_price(symbol)
    history_data = stock_service.get_history_data(symbol)
    
    return render_template(
        'stock/detail.html', 
        stock=stock, 
        stock_data=stock_data, 
        history_data=history_data
    )

@stock_bp.route('/api/search')
def search_stocks():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': []})
    
    # 搜索股票
    stocks = Stock.query.filter(
        (Stock.symbol.like(f'%{query}%')) | 
        (Stock.name.like(f'%{query}%'))
    ).limit(10).all()
    
    results = [{'symbol': s.symbol, 'name': s.name} for s in stocks]
    return jsonify({'results': results})
```

### 实时数据更新 (Flask-SocketIO)

```python
# app/controllers/realtime.py
from flask_socketio import emit, join_room, leave_room
from app.extensions import socketio
from app.services.stock_data import StockDataService

stock_service = StockDataService()

@socketio.on('connect', namespace='/stock')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect', namespace='/stock')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('subscribe', namespace='/stock')
def handle_subscribe(symbol):
    # 将客户端加入以股票代码命名的房间
    join_room(symbol)
    print(f'Client subscribed to {symbol}')

@socketio.on('unsubscribe', namespace='/stock')
def handle_unsubscribe(symbol):
    # 将客户端从房间中移除
    leave_room(symbol)
    print(f'Client unsubscribed from {symbol}')

# 定时推送股票数据
def push_stock_updates():
    symbols = stock_service.get_active_symbols()
    for symbol in symbols:
        data = stock_service.get_latest_price(symbol)
        socketio.emit('price_update', data, namespace='/stock', room=symbol)
```

## 数据库设计 (MySQL)

### 主要表结构

1. **users**（用户表）
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(200) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

2. **stocks**（股票基本信息表）
```sql
CREATE TABLE stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    market VARCHAR(20) NOT NULL,
    industry VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

3. **stock_prices**（股票价格数据表）
```sql
CREATE TABLE stock_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(18,2) NOT NULL,
    high DECIMAL(18,2) NOT NULL,
    low DECIMAL(18,2) NOT NULL,
    close DECIMAL(18,2) NOT NULL,
    volume BIGINT NOT NULL,
    adj_close DECIMAL(18,2),
    FOREIGN KEY (stock_id) REFERENCES stocks(id),
    UNIQUE KEY (stock_id, date)
);
```

4. **portfolios**（投资组合表）
```sql
CREATE TABLE portfolios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE KEY (user_id, name)
);
```

5. **portfolio_stocks**（组合持仓表）
```sql
CREATE TABLE portfolio_stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    portfolio_id INT NOT NULL,
    stock_id INT NOT NULL,
    quantity INT NOT NULL,
    average_cost DECIMAL(18,2) NOT NULL,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id),
    FOREIGN KEY (stock_id) REFERENCES stocks(id),
    UNIQUE KEY (portfolio_id, stock_id)
);
```

6. **watch_lists**（自选股表）
```sql
CREATE TABLE watch_lists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stock_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (stock_id) REFERENCES stocks(id),
    UNIQUE KEY (user_id, stock_id)
);
```

7. **transactions**（交易记录表）
```sql
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stock_id INT NOT NULL,
    portfolio_id INT NOT NULL,
    type ENUM('buy', 'sell') NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(18,2) NOT NULL,
    total_amount DECIMAL(18,2) NOT NULL,
    status ENUM('pending', 'completed', 'cancelled') NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (stock_id) REFERENCES stocks(id),
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id)
);
```

## 股票数据获取方案

### 免费数据源
1. **Tushare开源版**：中国股市数据
2. **Yahoo Finance API**：全球股市数据
3. **Alpha Vantage**：基础版免费API
4. **新浪财经API**：A股实时行情

### 数据获取服务实现
```python
# app/services/stock_data.py
import requests
import pandas as pd
from datetime import datetime, timedelta
from app import db
from app.models.stock import Stock, StockPrice
from flask import current_app

class StockDataService:
    def __init__(self):
        self.api_key = current_app.config['STOCK_API_KEY']
        self.base_url = current_app.config['STOCK_API_URL']
    
    def fetch_stock_data(self, symbol):
        """获取单个股票数据"""
        try:
            response = requests.get(
                f"{self.base_url}/stock/{symbol}",
                params={"apikey": self.api_key}
            )
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def get_latest_price(self, symbol):
        """获取最新价格"""
        # 实际项目中应该从API获取实时数据
        # 这里简化为从数据库获取最新记录
        stock = Stock.query.filter_by(symbol=symbol).first()
        if not stock:
            return None
        
        latest_price = StockPrice.query.filter_by(
            stock_id=stock.id
        ).order_by(StockPrice.date.desc()).first()
        
        if not latest_price:
            return {
                'symbol': symbol,
                'last_price': 0,
                'change': 0,
                'change_percent': 0,
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        
        # 计算涨跌幅
        prev_price = StockPrice.query.filter(
            StockPrice.stock_id == stock.id,
            StockPrice.date < latest_price.date
        ).order_by(StockPrice.date.desc()).first()
        
        change = 0
        change_percent = 0
        if prev_price:
            change = latest_price.close - prev_price.close
            change_percent = change / prev_price.close * 100
        
        return {
            'symbol': symbol,
            'last_price': latest_price.close,
            'change': change,
            'change_percent': change_percent,
            'updated_at': latest_price.date.strftime('%Y-%m-%d')
        }
    
    def get_history_data(self, symbol, days=90):
        """获取历史K线数据"""
        stock = Stock.query.filter_by(symbol=symbol).first()
        if not stock:
            return []
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        prices = StockPrice.query.filter(
            StockPrice.stock_id == stock.id,
            StockPrice.date >= start_date,
            StockPrice.date <= end_date
        ).order_by(StockPrice.date).all()
        
        # 转换为图表库需要的格式
        return [{
            'time': price.date.strftime('%Y-%m-%d'),
            'open': float(price.open),
            'high': float(price.high),
            'low': float(price.low),
            'close': float(price.close)
        } for price in prices]
    
    def update_stock_data(self):
        """定时更新股票数据"""
        stocks = Stock.query.all()
        for stock in stocks:
            try:
                data = self.fetch_stock_data(stock.symbol)
                if data:
                    self._save_stock_data(stock.id, data)
            except Exception as e:
                current_app.logger.error(f"Error updating {stock.symbol}: {e}")
        
        db.session.commit()
    
    def _save_stock_data(self, stock_id, data):
        """保存股票数据到数据库"""
        # 具体实现取决于API返回的数据格式
        # 这里仅作示例
        for item in data.get('daily_prices', []):
            date = datetime.strptime(item['date'], '%Y-%m-%d')
            
            # 检查记录是否已存在
            existing = StockPrice.query.filter_by(
                stock_id=stock_id, 
                date=date
            ).first()
            
            if existing:
                # 更新现有记录
                existing.open = item['open']
                existing.high = item['high']
                existing.low = item['low']
                existing.close = item['close']
                existing.volume = item['volume']
                existing.adj_close = item.get('adj_close')
            else:
                # 创建新记录
                new_price = StockPrice(
                    stock_id=stock_id,
                    date=date,
                    open=item['open'],
                    high=item['high'],
                    low=item['low'],
                    close=item['close'],
                    volume=item['volume'],
                    adj_close=item.get('adj_close')
                )
                db.session.add(new_price)
```

## 开发与部署路线图

### 第一阶段：基础架构（4周）
1. 初始化Flask项目框架
2. 设计并创建数据库架构
3. 实现用户认证系统
4. 搭建基础UI模板

### 第二阶段：核心功能（6周）
1. 股票数据获取与存储
2. 行情展示与K线图
3. 个人投资组合管理
4. 自选股与基本监控

### 第三阶段：交易功能（4周）
1. 模拟交易系统
2. 委托单管理
3. 交易历史记录
4. 盈亏分析

### 第四阶段：高级功能（6周）
1. 技术指标计算与展示
2. 实时行情推送
3. 预警系统
4. 个性化推荐

### 第五阶段：优化与上线（4周）
1. 性能优化
2. 安全加固
3. 用户体验完善
4. 部署与监控

## 部署方案

### 开发环境
- 本地开发：Flask内置服务器
- 数据库：本地MySQL

### 生产环境
- Web服务器：Nginx
- WSGI服务器：Gunicorn
- 数据库：MySQL
- 缓存：Redis (可选)
- 监控：Prometheus + Grafana (可选)

### 部署步骤
1. 准备服务器环境
2. 安装依赖软件
3. 配置Nginx反向代理
4. 设置Gunicorn服务
5. 配置数据库连接
6. 设置自动化部署脚本

## 建议与注意事项

1. **初期数据源选择**：使用免费API开始，待系统稳定后考虑付费数据源
2. **实时性问题**：A股盘中数据有延迟，需在界面明确标注
3. **技术挑战**：实时数据推送和大量K线数据渲染可能是性能瓶颈
4. **开发重点**：先实现功能，后期再优化性能和UI体验
5. **合规问题**：明确标识为模拟交易，避免触及金融监管红线
6. **一体化架构优势**：降低开发复杂度，便于初学者理解和实现

## 版本管理 (Git)

### 配置与规范

1. **仓库初始化**
```bash
git init
git add .
git commit -m "初始化股票系统项目"
git remote add origin <远程仓库URL>
git push -u origin main
```

2. **分支管理策略**
   - `main`/`master`: 主分支，稳定版本
   - `dev`: 开发分支，功能集成测试
   - `feature/<功能名>`: 新功能开发
   - `bugfix/<问题描述>`: 缺陷修复
   - `release/<版本号>`: 预发布版本

3. **提交信息规范**
```
<类型>(<范围>): <简短描述>

<详细描述>

<关联的问题单>
```
   - 类型: feat(新功能)、fix(修复)、docs(文档)、style(格式)、refactor(重构)、test(测试)、chore(杂项)
   - 范围: 模块名称，如 auth、stock、portfolio 等
   - 例如: `feat(stock): 添加K线图表显示功能`

4. **.gitignore 配置**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# 开发环境
.env
.venv
.idea/
.vscode/
*.swp
*.swo

# 项目特定
instance/
.webassets-cache
.coverage
.pytest_cache/
logs/
*.log
```

## Docker化部署

### 项目容器化

1. **Dockerfile**
```dockerfile
# 基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app
ENV FLASK_ENV=production

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

2. **docker-compose.yml**
```yaml
version: '3.8'

services:
  web:
    build: .
    restart: always
    depends_on:
      - db
    environment:
      - FLASK_APP=app
      - FLASK_ENV=production
      - DATABASE_URL=mysql+pymysql://user:password@db:3306/stocksystem
      - SECRET_KEY=${SECRET_KEY}
      - STOCK_API_KEY=${STOCK_API_KEY}
      - STOCK_API_URL=${STOCK_API_URL}
    volumes:
      - ./:/app
    ports:
      - "5000:5000"

  db:
    image: mysql:8.0
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=stocksystem
      - MYSQL_USER=user
      - MYSQL_PASSWORD=password
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
    command: --default-authentication-plugin=mysql_native_password

volumes:
  mysql_data:
```

3. **.dockerignore**
```
.git
.gitignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
venv
env
.env
.venv
.pytest_cache
.coverage
htmlcov
.tox
.idea
.vscode
*.swp
*.swo
node_modules
```

### 开发环境

开发环境使用 Docker Compose 配置：

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  web:
    build: .
    restart: always
    depends_on:
      - db
    environment:
      - FLASK_APP=app
      - FLASK_ENV=development
      - FLASK_DEBUG=1
      - DATABASE_URL=mysql+pymysql://user:password@db:3306/stocksystem
      - SECRET_KEY=dev_secret_key
    volumes:
      - ./:/app
    ports:
      - "5000:5000"
    command: flask run --host=0.0.0.0

  db:
    image: mysql:8.0
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=stocksystem
      - MYSQL_USER=user
      - MYSQL_PASSWORD=password
    volumes:
      - mysql_data_dev:/var/lib/mysql
    ports:
      - "3306:3306"

volumes:
  mysql_data_dev:
```

### 生产环境

生产环境配置示例：

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  web:
    build: .
    restart: always
    depends_on:
      - db
    environment:
      - FLASK_APP=app
      - FLASK_ENV=production
      - DATABASE_URL=mysql+pymysql://user:password@db:3306/stocksystem
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./:/app
    ports:
      - "5000:5000"
    command: gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app

  db:
    image: mysql:8.0
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=stocksystem
      - MYSQL_USER=user
      - MYSQL_PASSWORD=password
    volumes:
      - mysql_data_prod:/var/lib/mysql
    ports:
      - "3306:3306"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - web

volumes:
  mysql_data_prod:
```

### 容器化优势

1. **环境一致性**：确保开发、测试和生产环境的一致性
2. **快速部署**：简化应用的部署和迁移过程
3. **伸缩性**：易于进行水平扩展和负载均衡
4. **隔离性**：应用及其依赖被封装，避免了环境冲突
5. **资源效率**：比传统虚拟机更加轻量级，资源利用率更高

### CI/CD 集成

1. **GitHub Actions 示例配置**
```yaml
# .github/workflows/docker-deploy.yml
name: Docker Build and Deploy

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies and run tests
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest
        pytest
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v2
      with:
        context: .
        push: ${{ github.event_name != 'pull_request' }}
        tags: ${{ secrets.DOCKER_REGISTRY }}/stock-system:latest

  deploy:
    needs: build
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_KEY }}
        script: |
          cd /path/to/app
          docker-compose -f docker-compose.prod.yml pull
          docker-compose -f docker-compose.prod.yml up -d 