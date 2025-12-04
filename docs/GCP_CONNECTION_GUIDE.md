# GCP Cloud SQL 连接配置指南

本文档说明如何获取 GCP Cloud SQL 的连接信息并配置到项目中。

## 📍 在 GCP 控制台查看连接信息

### 步骤 1: 进入 Cloud SQL 控制台
1. 访问 [Google Cloud Console](https://console.cloud.google.com)
2. 选择你的项目
3. 在左侧菜单找到 **SQL**（或搜索 "Cloud SQL"）
4. 点击你的 MySQL 实例名称

### 步骤 2: 查看连接信息
在实例详情页面，你会看到以下信息：

#### **连接名称（Connection Name）**
- 格式：`项目ID:区域:实例名`
- 示例：`my-project:us-central1:my-mysql-instance`
- 位置：在页面顶部的实例名称下方

#### **IP 地址（IP Address）**
在 **"概览"（Overview）** 标签页，找到 **"连接"（Connectivity）** 部分：

- **公共 IP（Public IP）**：
  - 如果已启用，会显示一个公网 IP 地址（如：`34.123.45.67`）
  - 这是你本地开发时需要的 IP
  - 如果显示 "None"，需要先启用公共 IP（见下方说明）

- **私有 IP（Private IP）**：
  - 仅在 GCP 内部网络使用（如 GCE 虚拟机）
  - 本地开发通常不需要

#### **端口（Port）**
- MySQL 默认端口：**3306**
- 可以在 **"连接"（Connections）** 标签页确认

---

## 🔧 配置 `.env` 文件

根据你在 GCP 控制台看到的信息，在项目根目录的 `.env` 文件中配置：

### 情况 A: 使用公共 IP（本地开发推荐）

```env
# GCP Cloud SQL 连接信息
WS_DB_HOST=34.169.52.137          # 替换为你的公共 IP
WS_DB_PORT=3306                  # MySQL 默认端口
WS_DB_USER=your_username         # 数据库用户名
WS_DB_PASSWORD=your_password     # 数据库密码
```

### 情况 B: 使用 Cloud SQL Auth Proxy（更安全）

如果你使用 Cloud SQL Auth Proxy，则：

```env
WS_DB_HOST=127.0.0.1             # 本地代理地址
WS_DB_PORT=3306                  # 代理监听的端口
WS_DB_USER=your_username
WS_DB_PASSWORD=your_password
```

---

## 🔐 启用公共 IP（如果还没有）

如果你的实例没有公共 IP，需要启用：

1. 在 Cloud SQL 实例页面，点击 **"编辑"（Edit）**
2. 展开 **"连接"（Connections）** 部分
3. 勾选 **"公共 IP"（Public IP）**
4. 点击 **"保存"（Save）**
5. 等待几分钟，实例会重启并分配公共 IP

---

## 🛡️ 配置授权网络（允许你的 IP 访问）

启用公共 IP 后，需要将你的本地 IP 加入授权网络：

1. 在实例页面，点击 **"连接"（Connections）** 标签页
2. 在 **"授权网络"（Authorized networks）** 部分，点击 **"添加网络"（Add network）**
3. 输入你的公网 IP（可以在 [whatismyip.com](https://whatismyip.com) 查看）
4. 给这个网络起个名字（如：`我的本地开发机`）
5. 点击 **"添加"（Add）**

**注意**：如果你的 IP 是动态的（会变化），每次 IP 变化后都需要重新添加。

---

## 🧪 测试连接

配置完成后，可以使用以下方法测试连接：

### 方法 1: 使用 MySQL 客户端

```bash
mysql -h <WS_DB_HOST> -P <WS_DB_PORT> -u <WS_DB_USER> -p <WS_DB_PASSWORD> -e "SHOW DATABASES;"
```

### 方法 2: 使用 Python 测试脚本

创建 `test_connection.py`：

```python
import pymysql

try:
    connection = pymysql.connect(
        host='你的WS_DB_HOST',
        port=3306,
        user='你的WS_DB_USER',
        password='你的WS_DB_PASSWORD',
        database='WS1'  # 测试连接 WS1 数据库
    )
    print("✅ 连接成功！")
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print(f"数据库 WS1 中的表: {tables}")
    connection.close()
except Exception as e:
    print(f"❌ 连接失败: {e}")
```

运行：
```bash
python test_connection.py
```

---

## 📝 完整 `.env` 示例

```env
# 主数据库（如果需要）
DB_NAME=main_db
DB_USER=common_user
DB_PASSWORD=common_password
DB_HOST=34.123.45.67
DB_PORT=3306

# GCP Workshop 数据库（WS1-WS11）
WS_DB_USER=common_user
WS_DB_PASSWORD=common_password
WS_DB_HOST=34.123.45.67          # 你的 Cloud SQL 公共 IP
WS_DB_PORT=3306

# 如果数据库名不是 WS1/WS2...，可以单独指定：
# WS1_DB_NAME=actual_ws1_name
# WS2_DB_NAME=actual_ws2_name
# ...
```

---

## 🚨 常见问题

### Q: 连接被拒绝（Connection refused）
- 检查 IP 是否在授权网络中
- 检查防火墙规则
- 确认实例正在运行

### Q: 找不到主机（Host not found）
- 检查 `WS_DB_HOST` 是否正确
- 确认公共 IP 已启用

### Q: 访问被拒绝（Access denied）
- 检查用户名和密码是否正确
- 确认该用户有权限访问 WS1-WS11 数据库

### Q: 超时（Timeout）
- 检查网络连接
- 如果使用代理，确认代理正在运行
- 检查 Cloud SQL 实例是否正常运行

---

## 📚 相关资源

- [Cloud SQL 文档](https://cloud.google.com/sql/docs/mysql)
- [连接 Cloud SQL](https://cloud.google.com/sql/docs/mysql/connect-overview)
- [使用 Cloud SQL Auth Proxy](https://cloud.google.com/sql/docs/mysql/connect-admin-proxy)

