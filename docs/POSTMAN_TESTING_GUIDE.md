# Postman API 测试指南

本指南将帮助您使用 Postman 测试 ChatSQL 项目的所有 API endpoints。

## 前置准备

1. **启动 Django 服务器**
   ```bash
   python manage.py runserver
   ```
   默认服务器地址：`http://localhost:8000`

2. **确保数据库已初始化**
   - 运行迁移：`python manage.py migrate`
   - 如有需要，运行种子数据：`python manage.py apply_seed`

## 基础配置

### 设置环境变量（可选但推荐）

在 Postman 中创建一个新环境，设置以下变量：
- `base_url`: `http://localhost:8000`
- `exercise_id`: `1` (用于测试，实际值根据您的数据调整)

## API Endpoints 测试

### 1. GET /api/schemas/

**获取所有数据库模式列表**

**请求配置：**
- **方法**: `GET`
- **URL**: `http://localhost:8000/api/schemas/`
- **Headers**: 无需特殊 headers

**测试步骤：**
1. 在 Postman 中创建新请求
2. 选择方法为 `GET`
3. 输入 URL: `http://localhost:8000/api/schemas/`
4. 点击 "Send"

**预期响应：**
```json
[
  {
    "id": 1,
    "name": "employees",
    "display_name": "Employees DB",
    "description": "Demo employees schema",
    "exercise_count": 3
  }
]
```

---

### 2. GET /api/exercises/

**获取所有练习题列表（支持筛选）**

**请求配置：**
- **方法**: `GET`
- **URL**: `http://localhost:8000/api/exercises/`
- **Headers**: 无需特殊 headers
- **查询参数（可选）**:
  - `schema_id`: 按模式 ID 筛选（例如：`?schema_id=1`）
  - `difficulty`: 按难度筛选（例如：`?difficulty=easy`）

**测试步骤：**
1. 创建新请求，方法选择 `GET`
2. 输入 URL: `http://localhost:8000/api/exercises/`
3. 可选：在 "Params" 标签页添加查询参数
   - Key: `schema_id`, Value: `1`
   - Key: `difficulty`, Value: `easy`
4. 点击 "Send"

**示例 URL：**
- 获取所有练习：`http://localhost:8000/api/exercises/`
- 按模式筛选：`http://localhost:8000/api/exercises/?schema_id=1`
- 按难度筛选：`http://localhost:8000/api/exercises/?difficulty=easy`
- 组合筛选：`http://localhost:8000/api/exercises/?schema_id=1&difficulty=easy`

**预期响应：**
```json
[
  {
    "id": 1,
    "title": "Two erSum (SQL demo)",
    "difficulty": "easy",
    "schema": "Employees DB",
    "tags": ["select", "join"],
    "completed": false
  },
  {
    "id": 2,
    "title": "Count by Department",
    "difficulty": "easy",
    "schema": "Employees DB",
    "tags": ["aggregate"],
    "completed": false
  }
]
```

---

### 3. GET /api/exercises/<id>/

**获取特定练习题的详细信息**

**请求配置：**
- **方法**: `GET`
- **URL**: `http://localhost:8000/api/exercises/1/` (将 `1` 替换为实际的练习 ID)
- **Headers**: 无需特殊 headers

**测试步骤：**
1. 创建新请求，方法选择 `GET`
2. 输入 URL: `http://localhost:8000/api/exercises/1/`
   - 注意：URL 末尾的 `/` 是必需的
3. 点击 "Send"

**预期响应：**
```json
{
  "id": 1,
  "title": "Two Sum (SQL demo)",
  "description": "Find pairs of employees in the same department.",
  "difficulty": "easy",
  "initial_query": "SELECT id, name, dept FROM employees",
  "hints": [
    {
      "level": 1,
      "text": "Start with a simple SELECT"
    }
  ],
  "schema": {
    "id": 1,
    "name": "employees",
    "display_name": "Employees DB",
    "db_name": "employees"
  },
  "tags": ["select", "join"]
}
```

---

### 4. POST /api/exercises/<id>/execute/

**执行 SQL 查询（不验证答案）**

**请求配置：**
- **方法**: `POST`
- **URL**: `http://localhost:8000/api/exercises/1/execute/` (将 `1` 替换为实际的练习 ID)
- **Headers**:
  - `Content-Type`: `application/json`
- **Body** (raw JSON):
  ```json
  {
    "query": "SELECT id, name, dept FROM employees"
  }
  ```

**测试步骤：**
1. 创建新请求，方法选择 `POST`
2. 输入 URL: `http://localhost:8000/api/exercises/1/execute/`
3. 在 "Headers" 标签页添加：
   - Key: `Content-Type`, Value: `application/json`
4. 在 "Body" 标签页：
   - 选择 "raw"
   - 选择 "JSON" 格式
   - 输入 JSON body：
     ```json
     {
       "query": "SELECT id, name, dept FROM employees"
     }
     ```
5. 点击 "Send"

**预期响应（成功）：**
```json
{
  "success": true,
  "columns": ["id", "name", "dept"],
  "rows": [
    [1, "Alice", "Engineering"],
    [2, "Bob", "Engineering"],
    [3, "Carol", "HR"]
  ],
  "row_count": 3,
  "execution_time": 0.012,
  "error": null
}
```

**预期响应（SQL 错误）：**
```json
{
  "success": false,
  "error": "no such table: employees",
  "columns": [],
  "rows": [],
  "row_count": 0,
  "execution_time": 0.001
}
```

**错误响应（缺少 query 参数）：**
```json
{
  "error": "Query is required"
}
```
状态码：`400 Bad Request`

---

### 5. POST /api/exercises/<id>/submit/

**提交并验证 SQL 查询答案**

**请求配置：**
- **方法**: `POST`
- **URL**: `http://localhost:8000/api/exercises/1/submit/` (将 `1` 替换为实际的练习 ID)
- **Headers**:
  - `Content-Type`: `application/json`
- **Body** (raw JSON):
  ```json
  {
    "query": "SELECT id, name, dept FROM employees"
  }
  ```

**测试步骤：**
1. 创建新请求，方法选择 `POST`
2. 输入 URL: `http://localhost:8000/api/exercises/1/submit/`
3. 在 "Headers" 标签页添加：
   - Key: `Content-Type`, Value: `application/json`
4. 在 "Body" 标签页：
   - 选择 "raw"
   - 选择 "JSON" 格式
   - 输入 JSON body：
     ```json
     {
       "query": "SELECT id, name, dept FROM employees"
     }
     ```
5. 点击 "Send"

**预期响应（答案正确）：**
```json
{
  "correct": true,
  "message": "All tests passed.",
  "user_result": {
    "success": true,
    "columns": ["id", "name", "dept"],
    "rows": [
      [1, "Alice", "Engineering"],
      [2, "Bob", "Engineering"]
    ],
    "row_count": 2,
    "execution_time": 0.015,
    "error": null
  },
  "diff": null
}
```

**预期响应（答案错误）：**
```json
{
  "correct": false,
  "message": "Results do not match. Expected 3 rows, got 2.",
  "user_result": {
    "success": true,
    "columns": ["id", "name", "dept"],
    "rows": [
      [1, "Alice", "Engineering"],
      [2, "Bob", "Engineering"]
    ],
    "row_count": 2,
    "execution_time": 0.012,
    "error": null
  },
  "diff": {
    "row_count_diff": 1,
    "column_diff": [],
    "row_diff": [...]
  }
}
```

**错误响应（缺少 query 参数）：**
```json
{
  "error": "Query is required"
}
```
状态码：`400 Bad Request`

---

## 测试流程建议

### 完整测试流程

1. **获取模式列表**
   - 测试 `GET /api/schemas/`
   - 记录返回的模式 ID

2. **获取练习题列表**
   - 测试 `GET /api/exercises/`
   - 记录返回的练习 ID

3. **获取练习详情**
   - 使用步骤 2 中的练习 ID
   - 测试 `GET /api/exercises/<id>/`
   - 查看 `initial_query` 和 `description`

4. **执行查询测试**
   - 使用步骤 3 中的 `initial_query` 或编写自己的查询
   - 测试 `POST /api/exercises/<id>/execute/`
   - 验证查询是否能正常执行

5. **提交答案验证**
   - 使用正确的 SQL 查询
   - 测试 `POST /api/exercises/<id>/submit/`
   - 验证答案是否正确

---

## 常见问题排查

### 1. 连接错误
- **问题**: `Could not get any response`
- **解决**: 确保 Django 服务器正在运行 (`python manage.py runserver`)

### 2. 404 Not Found
- **问题**: `404 Not Found`
- **解决**: 
  - 检查 URL 是否正确（注意末尾的 `/`）
  - 确认练习 ID 是否存在

### 3. 400 Bad Request
- **问题**: `{"error": "Query is required"}`
- **解决**: 确保 POST 请求的 Body 中包含 `query` 字段

### 4. 500 Internal Server Error
- **问题**: 服务器内部错误
- **解决**: 
  - 检查 Django 服务器日志
  - 确认数据库连接正常
  - 验证 SQL 查询语法是否正确

### 5. CORS 错误（如果从浏览器测试）
- **问题**: CORS policy error
- **解决**: 项目已配置 `CORS_ALLOW_ALL_ORIGINS = True`，应该不会有此问题

---

## Postman Collection 导入（可选）

您可以创建一个 Postman Collection 文件来保存所有请求。以下是 JSON 格式的示例：

```json
{
  "info": {
    "name": "ChatSQL API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Get Schemas",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/api/schemas/",
          "host": ["{{base_url}}"],
          "path": ["api", "schemas", ""]
        }
      }
    },
    {
      "name": "Get Exercises",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/api/exercises/",
          "host": ["{{base_url}}"],
          "path": ["api", "exercises", ""]
        }
      }
    },
    {
      "name": "Get Exercise Detail",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/api/exercises/{{exercise_id}}/",
          "host": ["{{base_url}}"],
          "path": ["api", "exercises", "{{exercise_id}}", ""]
        }
      }
    },
    {
      "name": "Execute Query",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"query\": \"SELECT id, name, dept FROM employees\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/api/exercises/{{exercise_id}}/execute/",
          "host": ["{{base_url}}"],
          "path": ["api", "exercises", "{{exercise_id}}", "execute", ""]
        }
      }
    },
    {
      "name": "Submit Query",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"query\": \"SELECT id, name, dept FROM employees\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/api/exercises/{{exercise_id}}/submit/",
          "host": ["{{base_url}}"],
          "path": ["api", "exercises", "{{exercise_id}}", "submit", ""]
        }
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    },
    {
      "key": "exercise_id",
      "value": "1"
    }
  ]
}
```

将此 JSON 保存为 `.json` 文件，然后在 Postman 中：
1. 点击 "Import"
2. 选择该 JSON 文件
3. 所有请求将自动导入

---

## 注意事项

1. **URL 末尾的斜杠**: Django 默认要求 URL 末尾有 `/`，请确保在 URL 末尾添加 `/`

2. **Content-Type**: POST 请求必须设置 `Content-Type: application/json`

3. **Session 支持**: `execute` 和 `submit` 端点会使用 Django session 来跟踪用户进度。Postman 会自动处理 cookies

4. **练习 ID**: 确保使用的练习 ID 在数据库中存在。可以先调用 `GET /api/exercises/` 获取可用的 ID

5. **SQL 查询**: 根据实际的数据库结构编写 SQL 查询。如果使用 SQLite，某些 MySQL 特定的语法可能不工作

---

## 快速测试命令（使用 curl）

如果您想使用命令行测试，可以使用以下 curl 命令：

```bash
# 获取模式列表
curl http://localhost:8000/api/schemas/

# 获取练习题列表
curl http://localhost:8000/api/exercises/

# 获取练习详情
curl http://localhost:8000/api/exercises/1/

# 执行查询
curl -X POST http://localhost:8000/api/exercises/1/execute/ \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT id, name, dept FROM employees"}'

# 提交查询
curl -X POST http://localhost:8000/api/exercises/1/submit/ \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT id, name, dept FROM employees"}'
```

---

祝测试顺利！如有问题，请检查 Django 服务器日志获取详细错误信息。



