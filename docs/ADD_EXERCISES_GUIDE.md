# 添加练习题（Exercise）指南

本文档说明如何向 ChatSQL 项目添加练习题。

## 📍 添加方式

有两种方式可以添加练习题：

### 方式 1: 通过 Django Admin（推荐，最简单）

### 方式 2: 通过 Python 代码/管理命令

---

## 🎯 方式 1: Django Admin 界面（推荐）

### 步骤

1. **启动 Django 服务器**
   ```bash
   source venv/bin/activate
   python manage.py runserver
   ```

2. **访问 Admin 界面**
   - 打开浏览器访问: `http://localhost:8000/admin/`
   - 使用超级用户登录:
     - 用户名: `demo_admin`
     - 密码: `DemoPass123!`
     - （或查看 `docs/superuser.txt` 获取最新凭证）

3. **添加练习题**
   - 在 Admin 界面找到 **Exercises** 部分
   - 点击 **"Add Exercise"** 按钮
   - 填写所有字段（见下方格式要求）
   - 点击 **"Save"**

### 优点
- ✅ 图形界面，操作简单
- ✅ 实时验证数据格式
- ✅ 可以立即看到效果

---

## 💻 方式 2: Python 代码/管理命令

### 选项 A: 创建管理命令

创建一个新的管理命令文件，例如 `exercises/management/commands/add_exercises.py`:

```python
from django.core.management.base import BaseCommand
from exercises.models import DatabaseSchema, Exercise

class Command(BaseCommand):
    help = 'Add sample exercises'

    def handle(self, *args, **options):
        # 获取或创建 DatabaseSchema
        schema = DatabaseSchema.objects.get(name='demo_hr')
        
        # 创建练习题
        Exercise.objects.create(
            schema=schema,
            title='Find employees by department',
            description='Write a query to find all employees in the Engineering department.',
            difficulty='easy',
            order=2,
            expected_sql='SELECT id, name, dept FROM employees WHERE dept = "Engineering"',
            initial_query='SELECT id, name, dept FROM employees',
            hints=[
                {'level': 1, 'text': 'Use WHERE clause to filter rows'},
                {'level': 2, 'text': 'The department name is "Engineering"'}
            ],
            tags=['SELECT', 'WHERE']
        )
        
        self.stdout.write(self.style.SUCCESS('Exercise created successfully!'))
```

然后运行:
```bash
python manage.py add_exercises
```

### 选项 B: 在 Django Shell 中创建

```bash
source venv/bin/activate
python manage.py shell
```

然后在 shell 中:

```python
from exercises.models import DatabaseSchema, Exercise

# 获取数据库模式
schema = DatabaseSchema.objects.get(name='demo_hr')

# 创建练习题
exercise = Exercise.objects.create(
    schema=schema,
    title='Count employees by department',
    description='Count the number of employees in each department.',
    difficulty='medium',
    order=3,
    expected_sql='SELECT dept, COUNT(*) as count FROM employees GROUP BY dept',
    initial_query='SELECT * FROM employees',
    hints=[
        {'level': 1, 'text': 'You need to use GROUP BY'},
        {'level': 2, 'text': 'Use COUNT(*) to count rows'}
    ],
    tags=['SELECT', 'GROUP BY', 'COUNT', 'Aggregate']
)

print(f"Created exercise: {exercise.title}")
```

---

## 📋 Exercise 字段格式要求

### 必需字段

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `schema` | ForeignKey | 关联的数据库模式（必须已存在） | `DatabaseSchema.objects.get(name='demo_hr')` |
| `title` | CharField(200) | 练习题标题 | `"Find employees by department"` |
| `description` | TextField | 题目描述 | `"Write a query to find all employees in Engineering."` |
| `difficulty` | CharField(10) | 难度级别 | `'easy'`, `'medium'`, 或 `'hard'` |
| `expected_sql` | TextField | 标准答案 SQL | `'SELECT id, name FROM employees WHERE dept = "Engineering"'` |

### 可选字段

| 字段名 | 类型 | 默认值 | 说明 | 示例 |
|--------|------|--------|------|------|
| `order` | Integer | `0` | 显示顺序（数字越小越靠前） | `1`, `2`, `3` |
| `initial_query` | TextField | `''` | 初始代码（给学生作为起点） | `'SELECT * FROM employees'` |
| `hints` | JSONField | `[]` | 提示列表（JSON 格式） | 见下方格式 |
| `tags` | JSONField | `[]` | 标签列表（JSON 格式） | 见下方格式 |

---

## 📝 字段格式详解

### 1. `schema` (必需)

必须先有一个 `DatabaseSchema` 对象。可以通过以下方式获取：

```python
# 方式 1: 通过 name 获取
schema = DatabaseSchema.objects.get(name='demo_hr')

# 方式 2: 通过 id 获取
schema = DatabaseSchema.objects.get(id=1)

# 方式 3: 如果不存在，先创建
schema, created = DatabaseSchema.objects.get_or_create(
    name='demo_hr',
    defaults={
        'display_name': 'Demo HR Schema',
        'description': 'A small HR schema for demo',
        'db_name': 'practice_hr',
        'schema_sql': 'CREATE TABLE employees (id INT PRIMARY KEY, name VARCHAR(100), dept VARCHAR(50));',
        'seed_sql': "INSERT INTO employees (id, name, dept) VALUES (1, 'Alice', 'Sales'), (2, 'Bob', 'Engineering');"
    }
)
```

### 2. `difficulty` (必需)

必须是以下三个值之一：
- `'easy'` - 简单
- `'medium'` - 中等
- `'hard'` - 困难

### 3. `hints` (可选，JSON 格式)

**格式**: 列表，每个元素是一个包含 `level` 和 `text` 的字典

```python
hints = [
    {'level': 1, 'text': 'Use WHERE clause to filter rows'},
    {'level': 2, 'text': 'The department name is "Engineering"'},
    {'level': 3, 'text': 'Remember to use quotes around string values'}
]
```

**在 Django Admin 中**: 直接输入 JSON 字符串:
```json
[{"level": 1, "text": "Use WHERE clause to filter rows"}, {"level": 2, "text": "The department name is Engineering"}]
```

### 4. `tags` (可选，JSON 格式)

**格式**: 字符串列表

```python
tags = ['SELECT', 'WHERE', 'Filtering']
tags = ['JOIN', 'INNER JOIN', 'Multiple Tables']
tags = ['GROUP BY', 'COUNT', 'Aggregate Functions']
```

**在 Django Admin 中**: 直接输入 JSON 字符串:
```json
["SELECT", "WHERE", "Filtering"]
```

---

## 📚 完整示例

### 示例 1: 简单查询（Easy）

```python
Exercise.objects.create(
    schema=schema,
    title='List all employees',
    description='Write a SELECT query to retrieve all employees from the employees table.',
    difficulty='easy',
    order=1,
    expected_sql='SELECT id, name, dept FROM employees ORDER BY id',
    initial_query='SELECT * FROM employees',
    hints=[
        {'level': 1, 'text': 'Start with SELECT statement'},
        {'level': 2, 'text': 'Specify the columns you want to retrieve'}
    ],
    tags=['SELECT', 'Basic Query']
)
```

### 示例 2: 条件查询（Easy）

```python
Exercise.objects.create(
    schema=schema,
    title='Find employees in Engineering',
    description='Find all employees who work in the Engineering department.',
    difficulty='easy',
    order=2,
    expected_sql='SELECT id, name, dept FROM employees WHERE dept = "Engineering"',
    initial_query='SELECT id, name, dept FROM employees',
    hints=[
        {'level': 1, 'text': 'Use WHERE clause to filter rows'},
        {'level': 2, 'text': 'Use = operator to match department name'},
        {'level': 3, 'text': 'Remember to use quotes around string values: "Engineering"'}
    ],
    tags=['SELECT', 'WHERE', 'Filtering']
)
```

### 示例 3: 聚合查询（Medium）

```python
Exercise.objects.create(
    schema=schema,
    title='Count employees by department',
    description='Count the number of employees in each department. Show department name and count.',
    difficulty='medium',
    order=3,
    expected_sql='SELECT dept, COUNT(*) as employee_count FROM employees GROUP BY dept',
    initial_query='SELECT * FROM employees',
    hints=[
        {'level': 1, 'text': 'You need to group rows by department'},
        {'level': 2, 'text': 'Use GROUP BY dept'},
        {'level': 3, 'text': 'Use COUNT(*) to count the number of rows in each group'}
    ],
    tags=['SELECT', 'GROUP BY', 'COUNT', 'Aggregate Functions']
)
```

### 示例 4: 复杂查询（Hard）

```python
Exercise.objects.create(
    schema=schema,
    title='Find department with most employees',
    description='Find the department that has the most employees. Show department name and employee count.',
    difficulty='hard',
    order=4,
    expected_sql='''
        SELECT dept, COUNT(*) as count 
        FROM employees 
        GROUP BY dept 
        ORDER BY count DESC 
        LIMIT 1
    ''',
    initial_query='SELECT dept, COUNT(*) FROM employees GROUP BY dept',
    hints=[
        {'level': 1, 'text': 'First, count employees by department'},
        {'level': 2, 'text': 'Then order by count in descending order'},
        {'level': 3, 'text': 'Use LIMIT 1 to get only the top result'}
    ],
    tags=['SELECT', 'GROUP BY', 'COUNT', 'ORDER BY', 'LIMIT', 'Aggregate Functions']
)
```

---

## ⚠️ 重要注意事项

### 1. `expected_sql` 必须是有效的 SQL

- 确保 SQL 语法正确
- 确保查询能在对应的数据库上执行
- 注意数据库类型（MySQL vs SQLite）的差异

### 2. `expected_sql` 应该返回可比较的结果

- 系统会比较用户查询结果和预期结果
- 如果结果顺序不重要，确保使用 `ORDER BY` 或系统会自动处理
- 列名应该清晰明确

### 3. `initial_query` 应该给学生一个起点

- 可以是空查询: `'SELECT * FROM employees'`
- 可以是部分完成的查询，让学生补充
- 可以是注释提示: `'SELECT \n  -- Write your query here\nFROM employees'`

### 4. `hints` 应该循序渐进

- Level 1: 最基础的提示
- Level 2: 更具体的提示
- Level 3: 更详细的提示

### 5. `tags` 应该准确描述题目

- 帮助用户搜索和筛选
- 使用常见的 SQL 关键词
- 例如: `['SELECT', 'WHERE', 'JOIN', 'GROUP BY', 'ORDER BY']`

---

## 🔍 验证练习题

添加练习题后，可以通过以下方式验证：

### 1. 通过 API 测试

```bash
# 获取所有练习题
curl http://localhost:8000/api/exercises/

# 获取特定练习题详情
curl http://localhost:8000/api/exercises/1/
```

### 2. 通过前端界面

- 访问 `http://localhost:3000`（如果前端运行）
- 查看练习题列表
- 选择练习题并测试执行

### 3. 在 Django Admin 中查看

- 访问 `http://localhost:8000/admin/exercises/exercise/`
- 查看所有练习题列表
- 点击编辑查看详细信息

---

## 🛠️ 批量添加练习题

如果需要批量添加多个练习题，可以创建一个 Python 脚本：

```python
# add_multiple_exercises.py
from exercises.models import DatabaseSchema, Exercise

def add_exercises():
    schema = DatabaseSchema.objects.get(name='demo_hr')
    
    exercises_data = [
        {
            'title': 'List all employees',
            'description': 'Retrieve all employees',
            'difficulty': 'easy',
            'order': 1,
            'expected_sql': 'SELECT id, name, dept FROM employees ORDER BY id',
            'initial_query': 'SELECT * FROM employees',
            'hints': [{'level': 1, 'text': 'Use SELECT statement'}],
            'tags': ['SELECT']
        },
        {
            'title': 'Find Engineering employees',
            'description': 'Find employees in Engineering department',
            'difficulty': 'easy',
            'order': 2,
            'expected_sql': 'SELECT id, name, dept FROM employees WHERE dept = "Engineering"',
            'initial_query': 'SELECT id, name, dept FROM employees',
            'hints': [{'level': 1, 'text': 'Use WHERE clause'}],
            'tags': ['SELECT', 'WHERE']
        },
        # ... 更多练习题
    ]
    
    for data in exercises_data:
        Exercise.objects.get_or_create(
            schema=schema,
            title=data['title'],
            defaults=data
        )
        print(f"Created/Updated: {data['title']}")

if __name__ == '__main__':
    add_exercises()
```

然后在 Django shell 中运行:
```bash
python manage.py shell < add_multiple_exercises.py
```

---

## 📖 相关文件

- **模型定义**: `exercises/models.py`
- **Admin 配置**: `exercises/admin.py`
- **示例命令**: `exercises/management/commands/setup_demo.py`

---

## ❓ 常见问题

### Q: 如何修改已存在的练习题？
A: 在 Django Admin 中找到该练习题，点击编辑，修改后保存。

### Q: 如何删除练习题？
A: 在 Django Admin 中选择练习题，点击删除。

### Q: `expected_sql` 和 `initial_query` 有什么区别？
A: 
- `expected_sql`: 标准答案，用于验证用户提交的查询是否正确
- `initial_query`: 初始代码，显示在编辑器中作为起点

### Q: 可以添加多个数据库模式吗？
A: 可以！先创建 `DatabaseSchema`，然后为该模式创建练习题。

### Q: 如何测试 `expected_sql` 是否正确？
A: 可以先通过 `execute` API 测试查询是否能正常执行：
```bash
curl -X POST http://localhost:8000/api/exercises/1/execute/ \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR_EXPECTED_SQL_HERE"}'
```

---

祝您添加练习题顺利！如有问题，请查看代码注释或联系开发团队。



