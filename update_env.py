#!/usr/bin/env python
"""
更新 .env 文件，添加 WS_DB_* 配置
"""

import os
from pathlib import Path

def update_env_file():
    """更新 .env 文件，添加 WS_DB_* 配置"""
    env_path = Path(__file__).parent / '.env'
    
    # 读取现有内容
    existing_lines = []
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            existing_lines = f.readlines()
    
    # 检查是否已有 WS_DB_* 配置
    has_ws_config = any('WS_DB_' in line for line in existing_lines)
    
    if has_ws_config:
        print("✅ .env 文件中已存在 WS_DB_* 配置")
        return
    
    # 从现有配置中提取 DB_* 的值（用于 WS_DB_*）
    db_host = None
    db_user = None
    db_password = None
    db_port = '3306'
    
    for line in existing_lines:
        line = line.strip()
        if line.startswith('DB_HOST=') and '=' in line:
            db_host = line.split('=', 1)[1].strip()
        elif line.startswith('DB_USER=') and '=' in line:
            db_user = line.split('=', 1)[1].strip()
        elif line.startswith('DB_PASSWORD=') and '=' in line:
            db_password = line.split('=', 1)[1].strip()
        elif line.startswith('DB_PORT=') and '=' in line:
            db_port = line.split('=', 1)[1].strip()
    
    # 添加 WS_DB_* 配置
    ws_config = [
        '\n',
        '# ============================================\n',
        '# GCP Cloud SQL Workshop 数据库配置 (WS1-WS11)\n',
        '# ============================================\n',
        f'WS_DB_HOST={db_host or "34.169.52.137"}\n',
        f'WS_DB_PORT={db_port}\n',
        f'WS_DB_USER={db_user or "jinyuchen"}\n',
        f'WS_DB_PASSWORD={db_password or "CJY.101.com"}\n',
    ]
    
    # 写入文件
    with open(env_path, 'a', encoding='utf-8') as f:
        f.writelines(ws_config)
    
    print("✅ 已成功添加 WS_DB_* 配置到 .env 文件")
    print("\n添加的配置：")
    for line in ws_config:
        if line.strip() and not line.strip().startswith('#'):
            print(f"   {line.strip()}")

if __name__ == '__main__':
    update_env_file()

