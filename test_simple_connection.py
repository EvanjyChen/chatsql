#!/usr/bin/env python
"""简单的连接测试脚本"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('WS_DB_HOST', '34.169.52.137')
port = int(os.getenv('WS_DB_PORT', '3306'))
user = os.getenv('WS_DB_USER', 'jinyuchen')
password = os.getenv('WS_DB_PASSWORD', 'CJY.101.com')
database = 'WS1'

print(f"尝试连接到: {host}:{port}")
print(f"用户: {user}")
print(f"数据库: {database}")
print("-" * 60)

try:
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        connect_timeout=10
    )
    print("✅ 连接成功！")
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        print(f"当前数据库: {result[0]}")
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print(f"数据库中的表数量: {len(tables)}")
    connection.close()
except pymysql.Error as e:
    print(f"❌ 连接失败: {e}")
    print("\n可能的原因:")
    print("1. IP 地址未添加到授权网络")
    print("2. 用户名或密码错误")
    print("3. 用户没有访问权限")

