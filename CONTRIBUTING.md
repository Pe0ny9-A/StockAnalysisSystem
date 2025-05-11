# 贡献指南

感谢您对股票交易分析系统的贡献兴趣！本文档提供了参与项目开发的指南。

## 行为准则

请尊重所有项目参与者。遵循开源社区的礼仪和规范，保持专业和友好的交流氛围。

## 如何贡献

以下是您可以参与贡献的几种方式：

### 报告问题

如果您发现了bug或有功能建议，请在GitHub issues页面提交问题报告。提交前请：

1. 搜索已有issues，避免重复提交
2. 使用清晰的标题描述问题
3. 提供详细的复现步骤、预期行为和实际行为
4. 如可能，附上截图或错误日志

### 提交代码

1. Fork项目仓库
2. 创建功能分支（`git checkout -b feature/my-feature`）
3. 提交变更（`git commit -m '功能：添加新特性'`）
4. 推送到分支（`git push origin feature/my-feature`）
5. 创建Pull Request

### 代码审查

帮助审查其他贡献者提交的代码也是一种贡献方式。请提供建设性的反馈，关注代码质量和项目规范。

## 开发规范

### Git提交规范

提交信息应使用中文，格式为：`<类型>: <描述>`

类型包括：
- **功能**: 新功能
- **修复**: Bug修复
- **文档**: 文档更新
- **样式**: 代码格式调整（不影响代码运行）
- **重构**: 代码重构
- **测试**: 添加测试
- **构建**: 构建系统或外部依赖变更

例如：`功能: 添加股票筛选功能`

### Python代码规范

- 遵循PEP 8编码规范
- 使用类型注解增强代码可读性
- 每个函数必须有文档字符串(docstring)
- 最大行长度限制为88个字符

### 前端代码规范

- 使用ES6+语法
- Vue组件使用组合式API
- CSS采用BEM命名规范
- 静态资源使用统一路径前缀

## 开发环境设置

1. 克隆仓库
```bash
git clone https://github.com/Pe0ny9-A/StockAnalysisSystem.git
cd StockAnalysisSystem
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
复制`.env.example`创建`.env`文件，填写必要的配置信息。

5. 初始化数据库
```bash
flask db init
flask db migrate
flask db upgrade
```

6. 运行开发服务器
```bash
python run.py
```

## 分支策略

- `main`: 主分支，保持可部署状态
- `develop`: 开发分支，新功能合并到此分支
- `feature/*`: 功能分支，用于开发新功能
- `bugfix/*`: 缺陷修复分支
- `release/*`: 发布准备分支
- `hotfix/*`: 紧急修复分支

## 测试

提交前请确保通过所有测试：

```bash
pytest
```

对于新功能，请添加相应的单元测试和集成测试。

## 文档

代码变更应同步更新相关文档。对于API变更，请更新API文档。

## 许可证

通过贡献代码，您同意您的贡献将在MIT许可证下发布。

感谢您的贡献！ 