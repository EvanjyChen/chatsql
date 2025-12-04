# ChatSQL 项目文件结构说明

本文档详细说明 ChatSQL 项目中每个文件的作用和功能。

## 📁 项目概述

ChatSQL 是一个交互式 SQL 学习平台，包含：
- **后端**: Django REST API (Python)
- **前端**: React + TypeScript + Vite
- **功能**: SQL 练习、AI 导师、查询执行和验证

---

## 🔧 根目录配置文件

### `manage.py`
**作用**: Django 项目管理入口文件
- Django 项目的命令行工具入口
- 用于运行服务器、执行迁移、创建超级用户等
- 设置 Django 配置模块为 `chatsql.settings`

### `requirements.txt`
**作用**: Python 依赖包列表
- 列出所有后端需要的 Python 包
- 包含: Django, Django REST Framework, PyMySQL, OpenAI, CORS headers 等
- 使用 `pip install -r requirements.txt` 安装依赖

### `README.md`
**作用**: 项目说明文档
- 快速开始指南
- API endpoints 列表
- 安装和运行步骤

### `package.json` (根目录)
**作用**: Node.js 项目配置（如果存在）
- 可能包含根目录级别的脚本或工具配置

---

## 🎯 Django 主应用 (`chatsql/`)

### `chatsql/settings.py`
**作用**: Django 项目核心配置文件
- **数据库配置**: 支持 MySQL（生产）和 SQLite（开发）
- **应用注册**: 注册 `exercises`, `ai_tutor`, `frontend` 等应用
- **中间件**: CORS、安全、会话等中间件配置
- **REST Framework**: JSON 渲染器和解析器配置
- **环境变量**: 从 `.env` 文件加载配置（DEBUG, SECRET_KEY, 数据库凭证等）
- **OpenAI 模式**: 支持 'mock'（模拟）和 'real'（真实）两种模式

### `chatsql/urls.py`
**作用**: 项目主 URL 路由配置
- 定义所有 API endpoints 的路由
- 包含:
  - `/api/schemas/` - 获取数据库模式列表
  - `/api/exercises/` - 获取练习题列表
  - `/api/exercises/<id>/` - 获取练习详情
  - `/api/exercises/<id>/execute/` - 执行 SQL 查询
  - `/api/exercises/<id>/submit/` - 提交并验证答案
  - `/api/exercises/<id>/ai/` - AI 导师对话
  - `/` - 前端首页

### `chatsql/wsgi.py`
**作用**: WSGI 应用入口（生产环境）
- Web Server Gateway Interface 配置
- 用于部署到生产服务器（如 Gunicorn, uWSGI）

### `chatsql/asgi.py`
**作用**: ASGI 应用入口（异步支持）
- Asynchronous Server Gateway Interface 配置
- 支持 WebSocket 和异步请求（如使用 Daphne）

### `chatsql/__init__.py`
**作用**: Python 包初始化文件
- 标识 `chatsql` 为一个 Python 包

---

## 📚 练习题应用 (`exercises/`)

### `exercises/models.py`
**作用**: 数据模型定义
- **DatabaseSchema**: 数据库模式模型
  - 存储模式信息（HR, Ecommerce, School）
  - 包含 schema_sql（建表语句）和 seed_sql（种子数据）
- **Exercise**: 练习题模型
  - 标题、描述、难度、预期 SQL、初始查询、提示、标签等
- **UserProgress**: 用户进度跟踪
  - 记录用户完成状态、尝试次数、最后查询等
  - 支持匿名（session_id）和认证用户
- **ChatHistory**: AI 对话历史
  - 存储用户消息和 AI 回复

### `exercises/admin.py`
**作用**: Django Admin 后台管理配置
- 为所有模型注册管理界面
- 配置列表显示、搜索、过滤等功能
- 方便管理员在后台管理数据

### `exercises/views.py`
**作用**: API 视图函数/类
- **SchemaListView**: 获取所有数据库模式列表
- **ExerciseListView**: 获取练习题列表（支持按模式、难度筛选）
- **ExerciseDetailView**: 获取单个练习题的详细信息
- **ExecuteQueryView**: 执行用户 SQL 查询（不验证答案）
  - 验证查询安全性
  - 执行查询并返回结果
  - 跟踪用户尝试次数
- **SubmitQueryView**: 提交并验证 SQL 查询答案
  - 执行用户查询和预期查询
  - 比较结果并返回是否正确
  - 更新用户完成状态

### `exercises/services/executor.py`
**作用**: SQL 查询执行器
- **SQLExecutor 类**: 安全的 SQL 执行服务
  - **安全验证**: 只允许 SELECT 查询，阻止危险关键字（DROP, DELETE, UPDATE 等）
  - **查询执行**: 连接到指定的练习数据库执行查询
  - **结果比较**: 比较用户查询结果和预期结果
  - **错误处理**: 捕获并返回 SQL 错误信息
  - **性能限制**: 最大执行时间 5 秒，最多返回 1000 行

### `exercises/management/commands/apply_seed.py`
**作用**: Django 管理命令 - 应用种子数据
- 从 `DatabaseSchema` 模型中读取 `schema_sql` 和 `seed_sql`
- 在默认数据库中执行这些 SQL 语句
- 用于初始化数据库表和数据
- 使用: `python manage.py apply_seed`

### `exercises/management/commands/setup_demo.py`
**作用**: Django 管理命令 - 设置演示数据
- 创建演示用的超级用户（默认: demo_admin）
- 创建演示用的数据库模式和练习题
- 将超级用户凭证保存到 `docs/superuser.txt`
- 使用: `python manage.py setup_demo`

### `exercises/migrations/`
**作用**: 数据库迁移文件
- Django 自动生成的数据库结构变更记录
- 用于版本控制和数据库同步

---

## 🤖 AI 导师应用 (`ai_tutor/`)

### `ai_tutor/views.py`
**作用**: AI 导师 API 视图
- **ExerciseAIView**: 处理 AI 导师对话请求
  - 接收用户消息、查询、错误信息
  - 调用 OpenAI 服务获取回复
  - 保存对话历史到数据库

### `ai_tutor/services/openai_service.py`
**作用**: OpenAI API 集成服务
- **get_ai_response()**: 获取 AI 回复的主函数
  - **Mock 模式**: 返回预设的模拟回复（默认，节省成本）
  - **Real 模式**: 调用真实的 OpenAI API（需要 API key）
  - 根据 `OPENAI_MODE` 设置选择模式
- **模型**: 使用 `gpt-4o-mini`（成本较低）
- **限制**: 最大 150 tokens，温度 0.2（更确定性）

---

## 🎨 前端应用 (`frontend/`)

### `frontend/views.py`
**作用**: Django 前端视图
- **IndexView**: 渲染前端 HTML 模板
- 提供简单的演示页面（使用传统 Django 模板）

### `frontend/templates/frontend/index.html`
**作用**: 简单的前端演示页面
- 包含基本的 SQL 编辑器（textarea）
- 查询执行和结果显示
- AI 聊天界面
- 支持懒加载 Monaco Editor

### `frontend/urls.py`
**作用**: 前端 URL 路由
- 定义前端页面的路由

---

## ⚛️ React 前端应用 (`chatsql-frontend/`)

### `chatsql-frontend/package.json`
**作用**: Node.js 项目配置
- 定义项目依赖和脚本
- **依赖**: React, TypeScript, Vite, Monaco Editor, Axios, Tailwind CSS
- **脚本**: `dev`（开发）, `build`（构建）, `preview`（预览）

### `chatsql-frontend/vite.config.ts`
**作用**: Vite 构建工具配置
- 配置 React 插件
- 开发服务器端口: 3000
- **代理配置**: 将 `/api` 请求代理到 `http://localhost:8000`
- 解决开发环境跨域问题

### `chatsql-frontend/src/main.tsx`
**作用**: React 应用入口文件
- 创建 React 根节点
- 渲染 `App` 组件
- 导入全局样式

### `chatsql-frontend/src/App.tsx`
**作用**: React 主应用组件
- 应用根组件
- 渲染 `Layout` 组件

### `chatsql-frontend/src/types/index.ts`
**作用**: TypeScript 类型定义
- 定义所有前端使用的数据类型接口
- 包括: `DatabaseSchema`, `Exercise`, `QueryResult`, `SubmitResult`, `AIResponse`, `ChatMessage` 等

### `chatsql-frontend/src/services/api.ts`
**作用**: API 服务层
- 封装所有后端 API 调用
- 使用 Axios 创建 HTTP 客户端
- **函数**:
  - `getSchemas()`: 获取数据库模式列表
  - `getExercises()`: 获取练习题列表
  - `getExercise()`: 获取练习详情
  - `executeQuery()`: 执行查询
  - `submitQuery()`: 提交查询
  - `getAIResponse()`: 获取 AI 回复
- **Mock 数据**: 包含模拟数据用于演示模式
- **错误处理**: API 失败时回退到 mock 数据

### `chatsql-frontend/src/components/Layout.tsx`
**作用**: 主布局组件
- 应用的主要布局结构
- 使用 `react-split` 实现可调整大小的面板
- **布局**:
  - 左侧: 问题描述 (`ProblemDescription`)
  - 中间: 代码编辑器 (`CodeEditor`) + 结果面板 (`ResultPanel`)
  - 右侧: AI 聊天 (`AIChat`)
- 管理应用状态（选中的练习、代码、查询结果等）

### `chatsql-frontend/src/components/CodeEditor.tsx`
**作用**: SQL 代码编辑器组件
- 使用 Monaco Editor（VS Code 的编辑器）
- SQL 语法高亮
- **功能**:
  - 编辑 SQL 查询
  - "Run" 按钮: 执行查询
  - "Submit" 按钮: 提交并验证答案
- 显示练习标题和难度

### `chatsql-frontend/src/components/AIChat.tsx`
**作用**: AI 聊天组件
- 与 AI 导师对话的界面
- **功能**:
  - 发送消息给 AI
  - 显示对话历史
  - 自动滚动到最新消息
  - 支持 Enter 键发送
- 接收用户查询和错误信息作为上下文

### `chatsql-frontend/src/components/ProblemDescription.tsx`
**作用**: 问题描述组件
- 显示当前练习题的详细信息
- 包括: 标题、描述、难度、提示、标签等

### `chatsql-frontend/src/components/ProblemList.tsx`
**作用**: 练习题列表组件
- 显示所有可用的练习题
- 支持筛选和选择

### `chatsql-frontend/src/components/ProblemModal.tsx`
**作用**: 练习题选择模态框
- 弹出窗口显示练习题列表
- 允许用户选择不同的练习题

### `chatsql-frontend/src/components/ResultPanel.tsx`
**作用**: 结果显示面板
- 显示查询执行结果
- 以表格形式展示数据
- 显示执行时间和行数
- 显示提交验证结果（正确/错误）

### `chatsql-frontend/src/components/Header.tsx`
**作用**: 页面头部组件
- 应用标题和导航
- 演示模式切换按钮
- 打开练习题列表的按钮

### `chatsql-frontend/src/index.css`
**作用**: 全局样式文件
- Tailwind CSS 导入
- 自定义样式

### `chatsql-frontend/tailwind.config.cjs`
**作用**: Tailwind CSS 配置
- 配置 Tailwind 主题和插件

### `chatsql-frontend/postcss.config.cjs`
**作用**: PostCSS 配置
- 配置 CSS 处理工具（Tailwind, Autoprefixer）

### `chatsql-frontend/tsconfig.json`
**作用**: TypeScript 配置
- TypeScript 编译器选项
- 路径别名、模块解析等配置

---

## 📝 文档目录 (`docs/`)

### `docs/superuser.txt`
**作用**: 超级用户凭证文件
- 由 `setup_demo` 命令自动生成
- 包含演示用的管理员用户名和密码

### `docs/POSTMAN_TESTING_GUIDE.md`
**作用**: Postman API 测试指南
- 详细的 API 测试步骤
- 每个端点的请求示例和预期响应

---

## 🛠️ 脚本文件 (`scripts/`)

### `scripts/run_demo.sh`
**作用**: 演示环境启动脚本
- **功能**:
  - 创建 Python 虚拟环境
  - 安装后端依赖
  - 运行数据库迁移
  - 创建演示数据
  - 安装前端依赖
  - 启动 Django 和 Vite 开发服务器
- **参数**:
  - `--no-start`: 只设置，不启动服务器
  - `--no-front`: 跳过前端设置
  - `--no-back`: 跳过后端设置

---

## 🗄️ 数据库文件

### `db.sqlite3`
**作用**: SQLite 数据库文件（开发环境）
- 当没有配置 MySQL 时使用的默认数据库
- 存储所有应用数据（模式、练习、用户进度等）

---

## 📦 其他文件

### `.env` / `.env.example`
**作用**: 环境变量配置文件
- 存储敏感信息（数据库凭证、API keys 等）
- `.env.example` 是模板文件，不应包含真实凭证

### `venv/`
**作用**: Python 虚拟环境目录
- 包含项目隔离的 Python 包
- 不应提交到版本控制

### `__pycache__/`
**作用**: Python 字节码缓存
- Python 自动生成的编译文件
- 不应提交到版本控制

---

## 🔄 数据流概览

1. **用户在前端输入 SQL 查询**
   - `CodeEditor.tsx` → `api.ts` → Django API

2. **后端处理查询**
   - `urls.py` → `views.py` → `executor.py` → MySQL/SQLite

3. **返回结果**
   - 数据库 → `executor.py` → `views.py` → JSON → 前端

4. **AI 对话**
   - `AIChat.tsx` → `api.ts` → `ExerciseAIView` → `openai_service.py` → OpenAI API

5. **用户进度跟踪**
   - `views.py` → `UserProgress` 模型 → 数据库

---

## 🚀 启动流程

1. **后端启动**:
   ```bash
   python manage.py runserver
   ```

2. **前端启动**:
   ```bash
   cd chatsql-frontend
   npm run dev
   ```

3. **或使用脚本**:
   ```bash
   ./scripts/run_demo.sh
   ```

---

## 📌 关键文件总结

| 文件 | 作用 | 重要性 |
|------|------|--------|
| `chatsql/settings.py` | 项目配置 | ⭐⭐⭐⭐⭐ |
| `chatsql/urls.py` | API 路由 | ⭐⭐⭐⭐⭐ |
| `exercises/models.py` | 数据模型 | ⭐⭐⭐⭐⭐ |
| `exercises/views.py` | API 视图 | ⭐⭐⭐⭐⭐ |
| `exercises/services/executor.py` | SQL 执行器 | ⭐⭐⭐⭐⭐ |
| `ai_tutor/services/openai_service.py` | AI 服务 | ⭐⭐⭐⭐ |
| `chatsql-frontend/src/components/Layout.tsx` | 主布局 | ⭐⭐⭐⭐⭐ |
| `chatsql-frontend/src/services/api.ts` | API 客户端 | ⭐⭐⭐⭐⭐ |

---

本文档提供了项目文件的全面概览。如需更详细的信息，请查看各个文件的代码注释。



