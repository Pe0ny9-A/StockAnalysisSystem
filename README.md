# StockAnalysisSystem - 股票交易分析系统

一个功能全面的股票交易分析平台，为个人投资者提供专业级分析工具和投资组合管理功能。

![版本](https://img.shields.io/badge/版本-A.1.0-blue)
![测试版](https://img.shields.io/badge/状态-测试版(Alpha)-orange)

## 功能特性

- **实时行情数据** - 支持A股、港股、美股实时行情查询
- **K线图表分析** - 多种技术指标和图表工具
- **投资组合管理** - 创建和管理多个投资组合，跟踪持仓表现
- **模拟交易功能** - 支持买卖交易，记录交易历史
- **个性化仪表盘** - 用户登录后可查看资产概览和市场动态
- **AI智能分析** - 基于人工智能的股票分析和推荐

## 技术栈

- **后端框架**: Python Flask
- **前端技术**: Vue.js + Element Plus
- **数据库**: MySQL + SQLAlchemy ORM
- **图表库**: ECharts
- **实时通信**: Flask-SocketIO
- **AI分析**: 接入第三方AI服务

## 安装指南

### 环境要求

- Python 3.8+
- MySQL 5.7+
- Node.js 14+ (可选，用于前端开发)

### 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/Pe0ny9-A/StockAnalysisSystem.git
cd StockAnalysisSystem
```

2. 创建虚拟环境

```bash
python -m venv venv
# 在Windows上
venv\Scripts\activate
# 在Linux/Mac上
source venv/bin/activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 配置数据库

编辑 `app/config.py` 文件，修改数据库连接信息：

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/stock_system'
```

5. 初始化数据库

```bash
flask db init
flask db migrate
flask db upgrade
```

6. 启动应用

```bash
python run.py
```

访问 http://localhost:5000 即可使用系统。

## 使用说明

### 用户注册与登录

首次使用需要注册账户，登录后即可访问所有功能。

### 查看股票行情

在"股票列表"页面可以浏览和搜索股票，点击股票名称可查看详细信息和K线图。

### 创建投资组合

在"投资组合"页面可以创建新的投资组合，添加股票并设置持仓数量。

### 模拟交易

在股票详情页可以进行买入和卖出操作，所有交易记录将在"交易历史"中显示。

### 个人仪表盘

登录后首页会显示个性化仪表盘，包含资产概览、持仓情况和市场动态。

## 贡献指南

欢迎贡献代码或提出建议！请遵循以下步骤：

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m '添加了某功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 开源协议

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

开发者: Pe0ny9
邮箱: pikachu237325@163.com
GitHub: https://github.com/Pe0ny9-A 