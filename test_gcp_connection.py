#!/usr/bin/env python
"""
测试 GCP Cloud SQL 连接脚本
用于验证 WS1-WS11 数据库配置是否正确

使用方法:
    python test_gcp_connection.py
"""

import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatsql.settings')
django.setup()

from django.conf import settings
import pymysql

def test_database_connection(db_name: str):
    """测试单个数据库连接"""
    print(f"\n{'='*60}")
    print(f"测试数据库: {db_name}")
    print(f"{'='*60}")
    
    if db_name not in settings.DATABASES:
        print(f"❌ 错误: 数据库 '{db_name}' 未在 settings.DATABASES 中配置")
        return False
    
    db_config = settings.DATABASES[db_name]
    
    # 检查配置是否完整
    required_keys = ['HOST', 'USER', 'PASSWORD', 'NAME', 'PORT']
    missing_keys = [key for key in required_keys if not db_config.get(key)]
    
    if missing_keys:
        print(f"❌ 错误: 缺少必需的配置项: {', '.join(missing_keys)}")
        print(f"   当前配置: {db_config}")
        return False
    
    print(f"   主机: {db_config['HOST']}")
    print(f"   端口: {db_config['PORT']}")
    print(f"   用户: {db_config['USER']}")
    print(f"   数据库名: {db_config['NAME']}")
    
    # 尝试连接
    connection = None
    try:
        print(f"\n   正在连接...")
        connection = pymysql.connect(
            host=db_config['HOST'],
            port=int(db_config['PORT']),
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            database=db_config['NAME'],
            connect_timeout=10,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print(f"   ✅ 连接成功！")
        
        # 测试查询：显示表
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            
            if tables:
                print(f"   📊 数据库中有 {len(tables)} 个表:")
                for table in tables[:10]:  # 只显示前10个
                    table_name = list(table.values())[0]
                    print(f"      - {table_name}")
                if len(tables) > 10:
                    print(f"      ... 还有 {len(tables) - 10} 个表")
            else:
                print(f"   ⚠️  数据库中没有表")
        
        return True
        
    except pymysql.Error as e:
        print(f"   ❌ 连接失败: {e}")
        return False
    except Exception as e:
        print(f"   ❌ 发生错误: {type(e).__name__}: {e}")
        return False
    finally:
        if connection:
            try:
                connection.close()
            except:
                pass  # 连接可能已经关闭

def main():
    """主函数"""
    print("\n" + "="*60)
    print("GCP Cloud SQL 连接测试")
    print("="*60)
    
    # 检查环境变量
    print("\n检查环境变量配置...")
    env_vars = {
        'WS_DB_HOST': os.getenv('WS_DB_HOST'),
        'WS_DB_PORT': os.getenv('WS_DB_PORT', '3306'),
        'WS_DB_USER': os.getenv('WS_DB_USER'),
        'WS_DB_PASSWORD': os.getenv('WS_DB_PASSWORD'),
    }
    
    missing_env = [k for k, v in env_vars.items() if not v]
    if missing_env:
        print(f"⚠️  警告: 以下环境变量未设置: {', '.join(missing_env)}")
        print("   请检查 .env 文件是否正确配置")
    else:
        print("✅ 所有必需的环境变量都已设置")
        for key, value in env_vars.items():
            if key == 'WS_DB_PASSWORD':
                print(f"   {key}: {'*' * len(value) if value else '未设置'}")
            else:
                print(f"   {key}: {value}")
    
    # 检查是否需要 DB_NAME（用于启用 MySQL 配置）
    if not os.getenv('DB_NAME'):
        print("\n⚠️  警告: DB_NAME 未设置")
        print("   如果未设置 DB_NAME，Django 会使用 SQLite，WS1-WS11 配置不会生效")
        print("   建议在 .env 中设置 DB_NAME（可以是任意值，只要启用 MySQL 配置即可）")
    
    # 测试 WS1-WS11 数据库
    print("\n" + "="*60)
    print("开始测试 WS1-WS11 数据库连接...")
    print("="*60)
    
    results = {}
    for i in range(1, 12):
        db_name = f'WS{i}'
        results[db_name] = test_database_connection(db_name)
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    print(f"\n成功: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 所有数据库连接测试通过！")
    elif success_count > 0:
        print(f"⚠️  部分数据库连接失败，请检查失败的数据库配置")
        print("\n失败的数据库:")
        for db_name, success in results.items():
            if not success:
                print(f"   - {db_name}")
    else:
        print("❌ 所有数据库连接都失败")
        print("\n可能的原因:")
        print("   1. .env 文件中的配置不正确")
        print("   2. GCP 授权网络未添加你的 IP")
        print("   3. 数据库用户名/密码错误")
        print("   4. 数据库名称不正确（WS1-WS11）")
        print("   5. 网络连接问题")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    main()

