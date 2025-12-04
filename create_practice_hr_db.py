#!/usr/bin/env python
"""
在 GCP 上创建 practice_hr 数据库和表

使用方法:
    python create_practice_hr_db.py
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('WS_DB_HOST')
port = int(os.getenv('WS_DB_PORT', '3306'))
user = os.getenv('WS_DB_USER')
password = os.getenv('WS_DB_PASSWORD')

if not all([host, user, password]):
    print("❌ 错误: 请确保 .env 文件中设置了 WS_DB_HOST, WS_DB_USER, WS_DB_PASSWORD")
    exit(1)

print("=" * 60)
print("创建 practice_hr 数据库")
print("=" * 60)
print(f"主机: {host}:{port}")
print(f"用户: {user}")
print()

try:
    # 连接到 MySQL 服务器（不指定数据库）
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        connect_timeout=10
    )
    
    with connection.cursor() as cursor:
        # 创建数据库
        print("1. 创建数据库 practice_hr...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS practice_hr CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("   ✅ 数据库创建成功")
        
        # 切换到 practice_hr 数据库
        cursor.execute("USE practice_hr")
        
        # 创建表
        print("\n2. 创建表...")
        
        tables_sql = [
            """CREATE TABLE IF NOT EXISTS products (
                product_id INT PRIMARY KEY,
                low_fats CHAR(1),
                recyclable CHAR(1)
            )""",
            """CREATE TABLE IF NOT EXISTS customer (
                id INT PRIMARY KEY,
                name VARCHAR(100),
                referee_id INT
            )""",
            """CREATE TABLE IF NOT EXISTS students (
                student_id INT PRIMARY KEY,
                student_name VARCHAR(100),
                major VARCHAR(50)
            )""",
            """CREATE TABLE IF NOT EXISTS activity (
                player_id INT,
                device_id INT,
                event_date DATE,
                games_played INT
            )""",
            """CREATE TABLE IF NOT EXISTS orders (
                order_number INT PRIMARY KEY,
                customer_number INT
            )""",
            """CREATE TABLE IF NOT EXISTS sales (
                employee_id INT,
                product_id INT,
                sales INT
            )"""
        ]
        
        for sql in tables_sql:
            cursor.execute(sql)
        
        print("   ✅ 所有表创建成功")
        
        # 插入示例数据
        print("\n3. 插入示例数据...")
        
        # 清空现有数据（如果存在）
        cursor.execute("DELETE FROM products")
        cursor.execute("DELETE FROM customer")
        cursor.execute("DELETE FROM students")
        cursor.execute("DELETE FROM activity")
        cursor.execute("DELETE FROM orders")
        cursor.execute("DELETE FROM sales")
        
        # 插入数据
        cursor.execute("""
            INSERT INTO products (product_id, low_fats, recyclable) VALUES
            (0, 'Y', 'N'),
            (1, 'Y', 'Y'),
            (2, 'N', 'Y'),
            (3, 'Y', 'Y'),
            (4, 'N', 'N')
        """)
        
        cursor.execute("""
            INSERT INTO customer (id, name, referee_id) VALUES
            (1, 'Will', NULL),
            (2, 'Jane', NULL),
            (3, 'Alex', 2),
            (4, 'Bill', NULL),
            (5, 'Zack', 1),
            (6, 'Mark', 2)
        """)
        
        cursor.execute("""
            INSERT INTO students (student_id, student_name, major) VALUES
            (1, 'Daniel', 'MSCS'),
            (2, 'Alice', NULL),
            (3, 'Bob', 'BSCS'),
            (4, 'George', 'MSEE-CE'),
            (5, 'Alain', 'MSCS')
        """)
        
        cursor.execute("""
            INSERT INTO activity (player_id, device_id, event_date, games_played) VALUES
            (1, 2, '2016-03-01', 5),
            (1, 2, '2016-05-02', 6),
            (2, 3, '2017-06-25', 1),
            (3, 1, '2016-03-02', 0),
            (3, 4, '2018-07-03', 5)
        """)
        
        cursor.execute("""
            INSERT INTO orders (order_number, customer_number) VALUES
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 3)
        """)
        
        cursor.execute("""
            INSERT INTO sales (employee_id, product_id, sales) VALUES
            (2, 2, 95),
            (2, 3, 95),
            (1, 1, 90),
            (1, 2, 99),
            (3, 1, 80),
            (3, 2, 82),
            (3, 3, 82)
        """)
        
        connection.commit()
        print("   ✅ 示例数据插入成功")
        
        # 验证
        print("\n4. 验证数据...")
        cursor.execute("SELECT COUNT(*) FROM products")
        products_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM customer")
        customer_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM students")
        students_count = cursor.fetchone()[0]
        
        print(f"   products 表: {products_count} 条记录")
        print(f"   customer 表: {customer_count} 条记录")
        print(f"   students 表: {students_count} 条记录")
    
    connection.close()
    
    print("\n" + "=" * 60)
    print("✅ practice_hr 数据库创建成功！")
    print("=" * 60)
    
except pymysql.Error as e:
    print(f"\n❌ 错误: {e}")
    print("\n可能的原因:")
    print("1. 数据库连接失败（检查 IP 是否在授权网络中）")
    print("2. 用户没有创建数据库的权限")
    print("3. 数据库已存在但表结构不同")
    exit(1)

