"""
批量添加 SQL Workshop 练习题

包含 Workshop 1 (Select) 和 Workshop 2 (Group By) 的所有练习题

"""
from exercises.models import DatabaseSchema, Exercise

def add_workshop_exercises():
    """添加 Workshop 1 和 Workshop 2 的所有练习题"""
    
    # 获取或创建数据库模式
    schema, created = DatabaseSchema.objects.get_or_create(
        name='demo_hr',
        defaults={
            'display_name': 'Demo HR Schema',
            'description': 'A small HR schema for demo and practice',
            'db_name': 'practice_hr',
            'schema_sql': '''
                CREATE TABLE IF NOT EXISTS products (
                    product_id INT PRIMARY KEY,
                    low_fats CHAR(1),
                    recyclable CHAR(1)
                );
                
                CREATE TABLE IF NOT EXISTS customer (
                    id INT PRIMARY KEY,
                    name VARCHAR(100),
                    referee_id INT
                );
                
                CREATE TABLE IF NOT EXISTS students (
                    student_id INT PRIMARY KEY,
                    student_name VARCHAR(100),
                    major VARCHAR(50)
                );
                
                CREATE TABLE IF NOT EXISTS activity (
                    player_id INT,
                    device_id INT,
                    event_date DATE,
                    games_played INT
                );
                
                CREATE TABLE IF NOT EXISTS orders (
                    order_number INT PRIMARY KEY,
                    customer_number INT
                );
                
                CREATE TABLE IF NOT EXISTS sales (
                    employee_id INT,
                    product_id INT,
                    sales INT
                );
            ''',
            'seed_sql': '''
                INSERT INTO products (product_id, low_fats, recyclable) VALUES
                (0, 'Y', 'N'),
                (1, 'Y', 'Y'),
                (2, 'N', 'Y'),
                (3, 'Y', 'Y'),
                (4, 'N', 'N');
                
                INSERT INTO customer (id, name, referee_id) VALUES
                (1, 'Will', NULL),
                (2, 'Jane', NULL),
                (3, 'Alex', 2),
                (4, 'Bill', NULL),
                (5, 'Zack', 1),
                (6, 'Mark', 2);
                
                INSERT INTO students (student_id, student_name, major) VALUES
                (1, 'Daniel', 'MSCS'),
                (2, 'Alice', NULL),
                (3, 'Bob', 'BSCS'),
                (4, 'George', 'MSEE-CE'),
                (5, 'Alain', 'MSCS');
                
                INSERT INTO activity (player_id, device_id, event_date, games_played) VALUES
                (1, 2, '2016-03-01', 5),
                (1, 2, '2016-05-02', 6),
                (2, 3, '2017-06-25', 1),
                (3, 1, '2016-03-02', 0),
                (3, 4, '2018-07-03', 5);
                
                INSERT INTO orders (order_number, customer_number) VALUES
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 3);
                
                INSERT INTO sales (employee_id, product_id, sales) VALUES
                (2, 2, 95),
                (2, 3, 95),
                (1, 1, 90),
                (1, 2, 99),
                (3, 1, 80),
                (3, 2, 82),
                (3, 3, 82);
            '''
        }
    )
    
    if created:
        print(f"✓ 创建了新的数据库模式: {schema.name}")
    else:
        print(f"✓ 使用已存在的数据库模式: {schema.name}")
    
    # Workshop 1 练习题数据
    workshop1_exercises = [
        {
            'title': 'WS1-1: Recyclable and Low Fat Products',
            'description': '''Write an SQL query to find the ids of products that are both low fat and recyclable.
            
Return the result table in any order.
Products table:
+-------------+----------+------------+
| product_id | low_fats | recyclable |
+-------------+----------+------------+
| 0 | Y | N |
| 1 | Y | Y |
| 2 | N | Y |
| 3 | Y | Y |
| 4 | N | N |
+-------------+----------+------------+''',
            'difficulty': 'easy',
            'order': 1,
            'expected_sql': "SELECT product_id FROM products WHERE low_fats = 'Y' AND recyclable = 'Y' ORDER BY product_id",
            'initial_query': 'SELECT product_id FROM products',
            'hints': [
                {'level': 1, 'text': 'Use WHERE clause to filter rows'},
                {'level': 2, 'text': 'You need to check TWO conditions: low_fats AND recyclable'},
                {'level': 3, 'text': 'Both conditions should equal to "Y"'}
            ],
            'tags': ['SELECT', 'WHERE', 'AND', 'Filtering', 'Easy']
        },
        {
            'title': 'WS1-2: Find Customer Referee',
            'description': '''Write an SQL query to report the names of the customer that are not referred by the customer with id = 2.
Return the result table in any order.
Customer table:
+----+------+------------+
| id | name | referee_id |
+----+------+------------+
| 1 | Will | null |
| 2 | Jane | null |
| 3 | Alex | 2 |
| 4 | Bill | null |
| 5 | Zack | 1 |
| 6 | Mark | 2 |
+----+------+------------+''',
            'difficulty': 'easy',
            'order': 2,
            'expected_sql': "SELECT name FROM customer WHERE referee_id != 2 OR referee_id IS NULL ORDER BY name",
            'initial_query': 'SELECT name FROM customer',
            'hints': [
                {'level': 1, 'text': 'Use WHERE clause with NOT EQUAL operator (!=)'},
                {'level': 2, 'text': 'Be careful with NULL values! NULL comparisons need special handling'},
                {'level': 3, 'text': 'Use "IS NULL" to check for NULL values, and combine with OR operator'}
            ],
            'tags': ['SELECT', 'WHERE', 'NULL', 'IS NULL', 'OR', 'Easy']
        },
        {
            'title': 'WS1-3: Find Master Degree Students',
            'description': '''Write an SQL query to report the student_id and student_name of students whose degree is master. Master degree always starts with MS prefix.
Return the result table in any order.
Students table:
+------------+--------------+---------+
| student_id | student_name | major |
+------------+--------------+---------+
| 1 | Daniel | MSCS |
| 2 | Alice | NULL |
| 3 | Bob | BSCS |
| 4 | George | MSEE-CE |
| 5 | Alain | MSCS |
+------------+--------------+---------+''',
            'difficulty': 'easy',
            'order': 3,
            'expected_sql': "SELECT student_id, student_name FROM students WHERE major LIKE 'MS%' ORDER BY student_id",
            'initial_query': 'SELECT student_id, student_name FROM students',
            'hints': [
                {'level': 1, 'text': 'Use LIKE operator for pattern matching'},
                {'level': 2, 'text': 'Master degrees start with "MS" prefix'},
                {'level': 3, 'text': 'Use % wildcard to match any characters after "MS": LIKE "MS%"'}
            ],
            'tags': ['SELECT', 'WHERE', 'LIKE', 'String Functions', 'Pattern Matching', 'Easy']
        }
    ]
    
    # Workshop 2 练习题数据
    workshop2_exercises = [
        {
            'title': 'WS2-1: Game Play Analysis I',
            'description': '''Write an SQL query to report the first login date for each player.
Return the result table in any order.
Activity table:
+-----------+-----------+------------+--------------+
| player_id | device_id | event_date | games_played |
+-----------+-----------+------------+--------------+
| 1 | 2 | 2016-03-01 | 5 |
| 1 | 2 | 2016-05-02 | 6 |
| 2 | 3 | 2017-06-25 | 1 |
| 3 | 1 | 2016-03-02 | 0 |
| 3 | 4 | 2018-07-03 | 5 |
+-----------+-----------+------------+--------------+''',
            'difficulty': 'easy',
            'order': 4,
            'expected_sql': 'SELECT player_id, MIN(event_date) as first_login FROM activity GROUP BY player_id ORDER BY player_id',
            'initial_query': 'SELECT player_id, event_date FROM activity',
            'hints': [
                {'level': 1, 'text': 'Think about "for each player" - this means GROUP BY player_id'},
                {'level': 2, 'text': 'First login means earliest date - use MIN() aggregate function'},
                {'level': 3, 'text': 'Use alias "as first_login" to rename the output column'}
            ],
            'tags': ['SELECT', 'GROUP BY', 'MIN', 'Aggregate Functions', 'Easy']
        },
        {
            'title': 'WS2-2: Customer Placing the Largest Number of Orders',
            'description': '''Write an SQL query to find the customer_number for the customer who has placed the largest number of orders.
The test cases are generated so that exactly one customer will have placed more orders than any other customer.
Orders table:
+--------------+-----------------+
| order_number | customer_number |
+--------------+-----------------+
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 3 |
+--------------+-----------------+''',
            'difficulty': 'easy',
            'order': 5,
            'expected_sql': 'SELECT customer_number FROM orders GROUP BY customer_number ORDER BY COUNT(*) DESC LIMIT 1',
            'initial_query': 'SELECT customer_number FROM orders',
            'hints': [
                {'level': 1, 'text': 'First, count the number of orders for each customer using GROUP BY'},
                {'level': 2, 'text': 'Use COUNT(*) to count orders, then ORDER BY COUNT(*) DESC'},
                {'level': 3, 'text': 'Use LIMIT 1 to get only the customer with the most orders'}
            ],
            'tags': ['SELECT', 'GROUP BY', 'COUNT', 'ORDER BY', 'LIMIT', 'Aggregate Functions', 'Easy']
        },
        {
            'title': 'WS2-3: Highest Sales Product for Each Employee',
            'description': '''Write a SQL query to find the highest sales with its corresponding product for each employee. In case of a tie, you should find the product with the smallest product_id.
Return the result table ordered by employee_id in ascending order.
Sales table:
+-------------+------------+-------+
| employee_id | product_id | sales |
+-------------+------------+-------+
| 2 | 2 | 95 |
| 2 | 3 | 95 |
| 1 | 1 | 90 |
| 1 | 2 | 99 |
| 3 | 1 | 80 |
| 3 | 2 | 82 |
| 3 | 3 | 82 |
+-------------+------------+-------+''',
            'difficulty': 'medium',
            'order': 6,
            'expected_sql': '''SELECT employee_id, product_id, sales
FROM sales
WHERE (employee_id, sales) IN (
    SELECT employee_id, MAX(sales)
    FROM sales
    GROUP BY employee_id
)
GROUP BY employee_id, sales
HAVING product_id = MIN(product_id)
ORDER BY employee_id''',
            'initial_query': 'SELECT employee_id, product_id, sales FROM sales',
            'hints': [
                {'level': 1, 'text': 'First find the maximum sales for each employee using GROUP BY and MAX()'},
                {'level': 2, 'text': 'Use a subquery to filter only the rows with maximum sales per employee'},
                {'level': 3, 'text': 'For ties, use MIN(product_id) with HAVING clause to get the smallest product_id'}
            ],
            'tags': ['SELECT', 'GROUP BY', 'MAX', 'MIN', 'HAVING', 'Subquery', 'Aggregate Functions', 'Medium']
        }
    ]
    
    # 合并所有练习题
    all_exercises = workshop1_exercises + workshop2_exercises
    
    # 添加练习题
    created_count = 0
    updated_count = 0
    
    for data in all_exercises:
        exercise, created = Exercise.objects.get_or_create(
            schema=schema,
            title=data['title'],
            defaults=data
        )
        
        if created:
            created_count += 1
            print(f"✓ 创建练习题: {data['title']}")
        else:
            # 更新已存在的练习题
            for key, value in data.items():
                setattr(exercise, key, value)
            exercise.save()
            updated_count += 1
            print(f"✓ 更新练习题: {data['title']}")
    
    print("\n" + "="*60)
    print(f"完成! 共创建 {created_count} 个新练习题, 更新 {updated_count} 个已存在的练习题")
    print("="*60)

if __name__ == '__main__':
    add_workshop_exercises()



