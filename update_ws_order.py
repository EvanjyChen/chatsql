"""
更新 WS 题目的显示顺序

将 WS1 到 WS11 的题目按照顺序排列：
- WS1: order 1-3
- WS2: order 4-6
- WS3: order 7-9
- WS4: order 10-12
- WS5: order 13-15
- WS6: order 16-18
- WS7: order 19-21
- WS8: order 22-24
- WS9: order 25-27
- WS10: order 28-30
- WS11: order 31-33

使用方法：
    python manage.py shell < update_ws_order.py
    或者
    python manage.py shell
    >>> exec(open('update_ws_order.py').read())
"""

import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatsql.settings')
django.setup()

from exercises.models import Exercise

def update_ws_order():
    """更新所有 WS 题目的 order 字段"""
    
    # 定义每个 WS 的题目标题和对应的新 order 值
    ws_mapping = {
        # WS1
        'WS1-1: Recyclable and Low Fat Products': 1,
        'WS1-2: Find Customer Referee': 2,
        'WS1-3: Find Master Degree Students': 3,
        
        # WS2
        'WS2-1: Game Play Analysis I': 4,
        'WS2-2: Customer Placing the Largest Number of Orders': 5,
        'WS2-3: Highest Sales Product for Each Employee': 6,
        
        # WS3
        'WS3-1: Actors and Directors Who Cooperated At Least Three Times': 7,
        'WS3-2: Article Views II': 8,
        'WS3-3: Students Who Took All Professor Classes': 9,
        
        # WS4
        'WS4-1: Game Play Analysis II': 10,
        'WS4-2: Page Recommendations': 11,
        'WS4-3: Median from Histogram': 12,
        
        # WS5
        'WS5-1: Project Employees I': 13,
        'WS5-2: Sales Person Without RED Company Orders': 14,
        'WS5-3: Department Employee Count': 15,
        
        # WS6
        'WS6-1: Consecutive Available Seats': 16,
        'WS6-2: Game Play Analysis III': 17,
        'WS6-3: Total Grade by Gender Until Each Day': 18,
        
        # WS7
        'WS7-1: Product Price at a Given Date': 19,
        'WS7-2: Sales Analysis I': 20,
        'WS7-3: Most Experienced Students': 21,
        
        # WS8
        'WS8-1: Tournament Winners': 22,
        'WS8-2: Active Businesses': 23,
        'WS8-3: Mentors with Five Direct Reports': 24,
        
        # WS9
        'WS9-1: Team Size for Each Employee': 25,
        'WS9-2: Running Total for Different Genders': 26,
        'WS9-3: Highest Sales per Employee (Window Function)': 27,
        
        # WS10
        'WS10-1: Calculate Special Bonus': 28,
        'WS10-2: Team Scores in Football Tournament': 29,
        'WS10-3: Department Salary Comparison': 30,
        
        # WS11
        'WS11-1: Monthly Transactions II': 31,
        'WS11-2: Tree Node Classification': 32,
        'WS11-3: Continuous Weather Periods': 33,
    }
    
    updated_count = 0
    not_found = []
    
    print("开始更新 WS 题目的 order 字段...")
    print("=" * 60)
    
    for title, new_order in ws_mapping.items():
        try:
            # 查找所有匹配的题目（可能有多个 schema）
            exercises = Exercise.objects.filter(title=title)
            
            if exercises.exists():
                for exercise in exercises:
                    old_order = exercise.order
                    exercise.order = new_order
                    exercise.save()
                    updated_count += 1
                    print(f"✓ 更新: {title}")
                    print(f"  旧 order: {old_order} -> 新 order: {new_order}")
            else:
                not_found.append(title)
                print(f"⚠ 未找到: {title}")
        except Exception as e:
            print(f"✗ 更新失败: {title} - {str(e)}")
    
    print("=" * 60)
    print(f"完成! 共更新 {updated_count} 个题目")
    
    if not_found:
        print(f"\n未找到的题目 ({len(not_found)} 个):")
        for title in not_found:
            print(f"  - {title}")
    
    # 显示更新后的顺序
    print("\n" + "=" * 60)
    print("更新后的题目顺序:")
    print("=" * 60)
    
    all_ws_exercises = Exercise.objects.filter(title__startswith='WS').order_by('order', 'id')
    for ex in all_ws_exercises:
        print(f"Order {ex.order:2d}: {ex.title}")


if __name__ == '__main__':
    update_ws_order()

