# GCP Cloud SQL 添加授权网络指南

## 📍 步骤 1: 获取你的公网 IP

### 方法 1: 使用命令行（推荐）

在终端运行以下命令之一：

```bash
curl https://api.ipify.org
```

或者：

```bash
curl https://ifconfig.me
```

### 方法 2: 使用浏览器

访问以下任一网站：
- https://whatismyip.com
- https://www.whatismyipaddress.com
- https://api.ipify.org

## 📝 步骤 2: 在 GCP 控制台添加授权网络

### 详细步骤：

1. **打开 Google Cloud Console**
   - 访问：https://console.cloud.google.com
   - 确保选择了正确的项目：**DB-GROUP10**

2. **进入 Cloud SQL 实例页面**
   - 在左侧导航菜单中，点击 **SQL**（数据库图标）
   - 或者搜索 "Cloud SQL"
   - 点击你的实例：**final-project-db**

3. **打开连接设置**
   - 在实例详情页面，点击顶部标签页中的 **"连接"（Connections）**
   - 或者点击左侧菜单中的 **"连接"**

4. **添加授权网络**
   - 在 **"授权网络"（Authorized networks）** 部分
   - 点击 **"+ 添加网络"（+ Add network）** 按钮

5. **填写网络信息**
   - **网络名称（Name）**：输入一个描述性名称，例如：
     - `我的本地开发机`
     - `Local Development`
     - `MacBook Pro`
   - **网络（Network）**：输入你的公网 IP 地址
     - 格式：`xxx.xxx.xxx.xxx/32`
     - 例如：`123.45.67.89/32`
     - **注意**：`/32` 表示只允许这个特定的 IP 地址

6. **保存**
   - 点击 **"添加"（Add）** 按钮
   - 等待几秒钟，授权网络会被添加到列表中

## ✅ 步骤 3: 验证连接

添加授权网络后，等待 1-2 分钟让配置生效，然后运行测试脚本：

```bash
python test_gcp_connection.py
```

如果连接成功，你会看到所有数据库的连接测试通过。

## 🚨 常见问题

### Q: 为什么需要 `/32`？

**A:** `/32` 是 CIDR 表示法，表示只允许这个特定的 IP 地址。如果你使用 `/24`，会允许整个 IP 段（256 个 IP），安全性较低。

### Q: 我的 IP 地址会变化怎么办？

**A:** 如果你的 IP 是动态的（每次连接网络都会变化），你有几个选择：

1. **每次 IP 变化后重新添加**（适合偶尔使用）
2. **使用 Cloud SQL Auth Proxy**（推荐，更安全且不需要添加 IP）
   - 安装：`gcloud components install cloud-sql-proxy`
   - 运行：`cloud-sql-proxy db-group10-475223:us-central1:final-project-db --port=3306`
   - 然后 `.env` 中设置 `WS_DB_HOST=127.0.0.1`

3. **使用 VPN 或固定 IP**（适合企业环境）

### Q: 添加后仍然无法连接？

**A:** 检查以下几点：
- 确认 IP 地址格式正确（包含 `/32`）
- 等待 1-2 分钟让配置生效
- 确认实例正在运行（状态为绿色）
- 检查防火墙设置
- 确认用户名和密码正确

### Q: 如何删除授权网络？

**A:** 
1. 在授权网络列表中，找到要删除的网络
2. 点击该行右侧的 **"删除"（Delete）** 图标（垃圾桶图标）
3. 确认删除

## 📸 截图说明

如果你需要更详细的截图指导，可以参考：
- [GCP Cloud SQL 文档 - 授权网络](https://cloud.google.com/sql/docs/mysql/configure-ip)

## 🔐 安全建议

1. **只添加必要的 IP**：只添加你实际使用的 IP 地址
2. **定期清理**：删除不再使用的授权网络
3. **使用描述性名称**：方便识别和管理
4. **考虑使用 Cloud SQL Auth Proxy**：更安全，不需要暴露公共 IP

