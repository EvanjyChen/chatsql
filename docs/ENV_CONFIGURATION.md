# .env 文件配置说明

## ⚠️ 重要提示

**必须设置 `DB_NAME` 才能启用 MySQL 配置（包括 WS1-WS11）**

Django 的 `settings.py` 中有这样的逻辑：
- 如果设置了 `DB_NAME`，会使用 MySQL 配置（包括 WS1-WS11）
- 如果没有设置 `DB_NAME`，会回退到 SQLite（WS1-WS11 配置不会生效）

## 📝 .env 文件模板

在项目根目录创建 `.env` 文件，内容如下：

```env
# Django 基础配置
SECRET_KEY=change-me-to-a-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI 配置（可选）
OPENAI_MODE=mock
# OPENAI_API_KEY=your-api-key-here

# ============================================
# 数据库配置
# ============================================
# 重要：必须设置 DB_NAME 才能启用 MySQL 配置（包括 WS1-WS11）
# 如果只使用 WS1-WS11，可以设置一个占位值（如：main_db）
DB_NAME=main_db
DB_USER=your_main_db_user
DB_PASSWORD=your_main_db_password
DB_HOST=your_main_db_host
DB_PORT=3306

# ============================================
# GCP Cloud SQL Workshop 数据库配置 (WS1-WS11)
# ============================================
# 这 11 个数据库共用同一套连接信息
WS_DB_HOST=34.169.52.137          # 你的 GCP Cloud SQL 公共 IP
WS_DB_PORT=3306                   # MySQL 默认端口
WS_DB_USER=your_ws_db_user       # 数据库用户名
WS_DB_PASSWORD=your_ws_db_password # 数据库密码

# 如果 GCP 上的数据库名不是 WS1/WS2...，可以单独指定：
# WS1_DB_NAME=actual_ws1_name
# WS2_DB_NAME=actual_ws2_name
# ... (以此类推)

# ============================================
# 练习数据库配置（可选，如果使用）
# ============================================
# PRACTICE_DB_USER=your_practice_user
# PRACTICE_DB_PASSWORD=your_practice_password
# PRACTICE_DB_HOST=your_practice_host
```

## 🔧 配置步骤

1. **在项目根目录创建 `.env` 文件**
   ```bash
   cd /path/to/chatsql-main
   touch .env
   ```

2. **复制上面的模板内容到 `.env` 文件**

3. **填入你的实际配置值**：
   - `WS_DB_HOST`: 你的 GCP Cloud SQL 公共 IP（如：`34.169.52.137`）
   - `WS_DB_USER`: 数据库用户名
   - `WS_DB_PASSWORD`: 数据库密码
   - `DB_NAME`: **必须设置**（可以是任意值，如 `main_db`，只要启用 MySQL 配置即可）

4. **保存文件**

## ✅ 验证配置

运行测试脚本验证配置：

```bash
python test_gcp_connection.py
```

如果看到所有数据库连接成功，说明配置正确。

## 🚨 常见问题

### Q: 为什么测试显示 "数据库 'WS1' 未在 settings.DATABASES 中配置"？

**A:** 这是因为没有设置 `DB_NAME`。Django 只有在设置了 `DB_NAME` 时才会加载 MySQL 配置（包括 WS1-WS11）。

**解决方法**：在 `.env` 文件中添加 `DB_NAME=main_db`（或任意值）。

### Q: 环境变量没有被加载？

**A:** 检查以下几点：
1. `.env` 文件是否在项目根目录（与 `manage.py` 同级）
2. `.env` 文件格式是否正确（每行一个变量，格式：`KEY=value`）
3. 没有多余的空格或引号（除非值本身需要引号）

### Q: 连接被拒绝？

**A:** 检查：
1. GCP Cloud SQL 实例是否正在运行
2. 你的 IP 是否在授权网络中
3. `WS_DB_HOST` 是否正确（公共 IP）
4. 用户名和密码是否正确

