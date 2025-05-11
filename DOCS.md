# 项目文档索引

本文档提供了股票交易分析系统的所有文档索引，方便开发者和用户快速查找相关信息。

## 核心文档

1. [README.md](README.md) - 项目概述、功能特性和安装指南
2. [FEATURES.md](FEATURES.md) - 当前已实现功能和计划实现功能
3. [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南和开发规范

## 许可证

* [LICENSE](LICENSE) - MIT开源许可证

## 项目配置

* [requirements.txt](requirements.txt) - Python依赖包列表
* [.gitignore](.gitignore) - Git版本控制忽略文件
* [Dockerfile](Dockerfile) - Docker容器配置
* [docker-compose.yml](docker-compose.yml) - Docker-Compose服务配置
* [env.example](env.example) - 环境变量示例

## 技术架构

股票交易分析系统采用Flask框架构建，使用MySQL数据库存储数据，前端采用Vue.js和Element UI组件库。项目采用模块化设计，主要分为以下模块：

1. **用户模块** - 处理用户注册、登录和个人信息管理
2. **股票模块** - 股票数据获取、存储和展示
3. **投资组合模块** - 用户投资组合管理
4. **交易模块** - 模拟股票交易功能
5. **分析模块** - 股票数据分析和可视化
6. **AI模块** - 智能分析和推荐功能

## 目录结构

```
stock-analysis-system/
├── app/                    # 应用主目录
│   ├── static/             # 静态资源
│   ├── templates/          # 模板文件
│   ├── models/             # 数据模型
│   ├── controllers/        # 控制器/路由
│   ├── services/           # 业务逻辑
│   └── utils/              # 工具函数
├── migrations/             # 数据库迁移
├── logs/                   # 日志文件
├── tests/                  # 测试代码
├── instance/               # 实例配置
└── venv/                   # 虚拟环境
```

## 快速链接

* [已实现功能](FEATURES.md#当前已实现功能)
* [开发计划](FEATURES.md#计划实现功能)
* [代码贡献规范](CONTRIBUTING.md#代码规范)
* [安装指南](README.md#安装指南)
* [技术实现方向](FEATURES.md#技术实现方向) 