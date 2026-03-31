# 🛒 电商平台 (E-commerce Platform)

这是一个使用 Flask 构建的简单电商平台，包含产品展示、购物车、订单处理等功能。

## 功能特点

- 📦 产品展示 - 热门电子产品展示
- 🛒 购物车 - 添加、删除商品
- 💳 订单结算 - 模拟结账流程
- 📊 数据处理 - 客户和订单数据管理

## 技术栈

- **后端**: Flask (Python)
- **数据库**: SQLite
- **CI/CD**: GitHub Actions

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动应用

```bash
python app.py
```

访问 http://127.0.0.1:5000

### 3. 运行数据处理

```bash
python clean_and_merge.py
```

## 项目结构

```
├── app.py                 # 主应用
├── clean_and_merge.py     # 数据处理脚本
├── requirements.txt      # 依赖
├── README.md             # 说明文档
└── .github/
    └── workflows/
        └── ecommerce-ci-cd.yml  # CI/CD 工作流
```

## CI/CD Pipeline

项目包含完整的 GitHub Actions 工作流：

1. **代码质量检查** - Lint 检查
2. **单元测试** - Pytest 测试
3. **数据处理** - 自动处理客户和订单数据
4. **应用构建** - 打包应用
5. **部署** - 模拟部署流程

## GitHub Actions 工作流说明

详细的工作流配置见 `.github/workflows/ecommerce-ci-cd.yml`

### 触发条件

- 推送到 main 分支
- 创建 Pull Request

### Jobs 流程

```
lint → test → data-processing → build → deploy
                     ↓
                  report (汇总报告)
```
