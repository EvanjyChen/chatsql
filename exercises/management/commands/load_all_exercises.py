"""
管理命令：加载所有 Workshop 练习题（WS1-WS11）

使用方法:
    python manage.py load_all_exercises

这个命令会：
1. 加载 WS1-WS2（来自 add_workshop_exercises.py）
2. 加载 WS3-WS6（来自 add_multiple_exercises.py）
3. 加载 WS7-WS9（来自 add_workshop_7_9_exercises.py）
4. 加载 WS10-WS11（来自 add_ws10_11_exercises.py，如果存在）

所有题目数据会持久化到数据库中，重启后不会丢失。
"""

from django.core.management.base import BaseCommand
from django.conf import settings
import sys
import os
import importlib.util
from pathlib import Path

# 使用 Django settings 获取项目根目录
BASE_DIR = Path(settings.BASE_DIR)
sys.path.insert(0, str(BASE_DIR))


class Command(BaseCommand):
    help = '加载所有 Workshop 练习题（WS1-WS11）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制重新加载所有题目（即使已存在）',
        )

    def load_script_module(self, script_path, description):
        """动态加载并执行脚本模块"""
        if not script_path.exists():
            self.stdout.write(
                self.style.WARNING(f'⚠ 跳过: 文件 {script_path.name} 不存在')
            )
            return False

        try:
            # 使用 importlib 动态加载模块
            spec = importlib.util.spec_from_file_location(
                script_path.stem, script_path
            )
            module = importlib.util.module_from_spec(spec)
            
            # 重定向 print 到 Django 输出
            original_print = __builtins__['print']
            def custom_print(*args, **kwargs):
                msg = ' '.join(str(arg) for arg in args)
                self.stdout.write(msg)
            module.__dict__['print'] = custom_print
            
            # 执行模块
            spec.loader.exec_module(module)
            
            # 调用相应的函数
            if hasattr(module, 'add_exercises'):
                module.add_exercises()
            elif hasattr(module, 'add_workshop_exercises'):
                module.add_workshop_exercises()
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ {description}: 未找到 add_exercises 或 add_workshop_exercises 函数')
                )
                return False
            
            return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ 加载 {description} 时出错: {str(e)}')
            )
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
            return False

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('开始加载所有 Workshop 练习题...'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        scripts = [
            (BASE_DIR / 'add_workshop_exercises.py', 'WS1-WS2'),
            (BASE_DIR / 'add_multiple_exercises.py', 'WS3-WS6'),
            (BASE_DIR / 'add_workshop_7_9_exercises.py', 'WS7-WS9'),
            (BASE_DIR / 'add_ws10_11_exercises.py', 'WS10-WS11'),
        ]

        for script_path, description in scripts:
            self.stdout.write(self.style.SUCCESS(f'\n📚 正在加载 {description}...'))
            self.stdout.write(f'   脚本: {script_path.name}')
            
            success = self.load_script_module(script_path, description)
            
            if success:
                self.stdout.write(self.style.SUCCESS(f'✓ {description} 加载完成'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ {description} 跳过'))

        # 统计总数
        from exercises.models import Exercise
        total_count = Exercise.objects.count()
        ws_count = Exercise.objects.filter(title__startswith='WS').count()

        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('✅ 所有题目加载完成！'))
        self.stdout.write(self.style.SUCCESS(f'📊 统计信息:'))
        self.stdout.write(self.style.SUCCESS(f'   - 总题目数: {total_count}'))
        self.stdout.write(self.style.SUCCESS(f'   - WS 题目数: {ws_count}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # 显示各 Workshop 的题目数量
        self.stdout.write(self.style.SUCCESS('\n📋 各 Workshop 题目统计:'))
        for ws in range(1, 12):
            prefix = f'WS{ws}-'
            count = Exercise.objects.filter(title__startswith=prefix).count()
            if count > 0:
                self.stdout.write(self.style.SUCCESS(f'   {prefix}: {count} 题'))
            else:
                self.stdout.write(self.style.WARNING(f'   {prefix}: 0 题（未加载）'))

