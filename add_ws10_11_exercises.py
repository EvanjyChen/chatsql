"""
批量添加 SQL Workshop 10-11 练习题
使用方法：python manage.py shell < add_ws10_11_exercises.py
"""

from exercises.models import DatabaseSchema, Exercise

def add_exercises():
    # 获取或创建数据库模式
    schema, created = DatabaseSchema.objects.get_or_create(
        name='demo_sql_workshop_10_11',
        defaults={
            'display_name': 'SQL Workshop 10-11 Database',
            'description': 'Database schema for SQL workshop IF/CASE and UNION exercises',
            'db_name': 'practice_workshop_10_11',
            'schema_sql': '''
                CREATE TABLE Employees (
                    employee_id INT PRIMARY KEY,
                    name VARCHAR(100),
                    salary DECIMAL(10,2)
                );
                CREATE TABLE Teams (
                    team_id INT PRIMARY KEY,
                    team_name VARCHAR(100)
                );
                CREATE TABLE Matches (
                    match_id INT PRIMARY KEY,
                    host_team INT,
                    guest_team INT,
                    host_goals INT,
                    guest_goals INT
                );
                CREATE TABLE Payment (
                    id INT PRIMARY KEY,
                    intern_id INT,
                    amount DECIMAL(10,2),
                    pay_date DATE
                );
                CREATE TABLE Intern (
                    intern_id INT PRIMARY KEY,
                    department_id INT
                );
                CREATE TABLE Transactions (
                    id INT PRIMARY KEY,
                    country VARCHAR(50),
                    state VARCHAR(50),
                    amount DECIMAL(10,2),
                    trans_date DATE
                );
                CREATE TABLE Chargebacks (
                    trans_id INT,
                    trans_date DATE
                );
                CREATE TABLE Tree (
                    id INT PRIMARY KEY,
                    p_id INT
                );
                CREATE TABLE Cloudy (
                    fail_date DATE
                );
                CREATE TABLE Clear (
                    success_date DATE
                );
            ''',
            'seed_sql': '''
                INSERT INTO Employees VALUES 
                    (2, 'Meir', 3000),
                    (3, 'Michael', 3800),
                    (7, 'Addilyn', 7400),
                    (8, 'Juan', 6100),
                    (9, 'Kannon', 7700);
                
                INSERT INTO Tree VALUES 
                    (1, NULL),
                    (2, 1),
                    (3, 1),
                    (4, 2),
                    (5, 2);
            '''
        }
    )
    
    print(f"{'Created' if created else 'Using existing'} schema: {schema.name}")
    
    # Workshop 10-11 练习题
    exercises_data = [
        # WS10-1: Calculate Special Bonus
        {
            'title': 'WS10-1: Calculate Special Bonus',
            'description': '''Write an SQL query to calculate the bonus of each employee. The bonus of an employee is 100% of their salary if the ID of the employee is an odd number and the employee name does not start with the character 'M'. The bonus of an employee is 0 otherwise.
Return the result table ordered by employee_id.

Employees table:
+-------------+---------+--------+
| employee_id | name    | salary |
+-------------+---------+--------+
| 2           | Meir    | 3000   |
| 3           | Michael | 3800   |
| 7           | Addilyn | 7400   |
| 8           | Juan    | 6100   |
| 9           | Kannon  | 7700   |
+-------------+---------+--------+

Expected output:
+-------------+-------+
| employee_id | bonus |
+-------------+-------+
| 2           | 0     |
| 3           | 0     |
| 7           | 7400  |
| 8           | 0     |
| 9           | 7700  |
+-------------+-------+''',
            'difficulty': 'easy',
            'order': 101,
            'expected_sql': '''SELECT employee_id,
    CASE
        WHEN employee_id % 2 != 0 AND name NOT LIKE 'M%'
        THEN salary
        ELSE 0
    END AS bonus
FROM employees
ORDER BY employee_id''',
            'initial_query': '''SELECT employee_id,
    CASE
        WHEN -- Add condition for odd employee_id and name not starting with 'M'
        THEN -- Bonus is salary
        ELSE -- Bonus is 0
    END AS bonus
FROM employees
ORDER BY employee_id''',
            'hints': [
                {'level': 1, 'text': 'Use CASE statement to implement conditional logic in SQL'},
                {'level': 2, 'text': 'Check if employee_id is odd using MOD operator: employee_id % 2 != 0'},
                {'level': 3, 'text': 'Check if name does not start with M using: name NOT LIKE "M%"'},
                {'level': 4, 'text': 'Combine both conditions with AND, return salary if true, else return 0'}
            ],
            'tags': ['CASE', 'Conditional Logic', 'MOD', 'LIKE', 'String Pattern']
        },
        
        # WS10-2: Team Scores in Football Tournament
        {
            'title': 'WS10-2: Team Scores in Football Tournament',
            'description': '''Write an SQL query that selects the team_id, team_name and num_points of each team in the tournament after all described matches.
Return the result table ordered by num_points in decreasing order. In case of a tie, order the records by team_id in increasing order.

Points are awarded as follows:
• A team receives three points if they win a match (scored more goals than opponent)
• A team receives one point if they draw a match (scored same number of goals)
• A team receives no points if they lose a match (scored fewer goals than opponent)

Teams table:
+---------+-------------+
| team_id | team_name   |
+---------+-------------+
| 10      | Leetcode FC |
| 20      | NewYork FC  |
| 30      | Atlanta FC  |
| 40      | Chicago FC  |
| 50      | Toronto FC  |
+---------+-------------+

Matches table:
+----------+-----------+------------+------------+-------------+
| match_id | host_team | guest_team | host_goals | guest_goals |
+----------+-----------+------------+------------+-------------+
| 1        | 10        | 20         | 3          | 0           |
| 2        | 30        | 10         | 2          | 2           |
| 3        | 10        | 50         | 5          | 1           |
| 4        | 20        | 30         | 1          | 0           |
| 5        | 50        | 30         | 1          | 0           |
+----------+-----------+------------+------------+-------------+

Expected output:
+---------+-------------+------------+
| team_id | team_name   | num_points |
+---------+-------------+------------+
| 10      | Leetcode FC | 7          |
| 20      | NewYork FC  | 3          |
| 50      | Toronto FC  | 3          |
| 30      | Atlanta FC  | 1          |
| 40      | Chicago FC  | 0          |
+---------+-------------+------------+''',
            'difficulty': 'medium',
            'order': 102,
            'expected_sql': '''SELECT team_id, team_name,
    SUM(CASE 
        WHEN team_id = host_team AND host_goals > guest_goals THEN 3
        WHEN team_id = guest_team AND guest_goals > host_goals THEN 3
        WHEN team_id = host_team AND host_goals = guest_goals THEN 1
        WHEN team_id = guest_team AND guest_goals = host_goals THEN 1
        ELSE 0 
    END) AS num_points
FROM Teams
LEFT JOIN Matches ON team_id = host_team OR team_id = guest_team
GROUP BY team_id, team_name
ORDER BY num_points DESC, team_id ASC''',
            'initial_query': '''SELECT team_id, team_name,
    SUM(CASE 
        WHEN -- Team is host and wins
        WHEN -- Team is guest and wins
        WHEN -- Team is host and draws
        WHEN -- Team is guest and draws
        ELSE 0 
    END) AS num_points
FROM Teams
LEFT JOIN Matches ON -- Join condition
GROUP BY team_id, team_name
ORDER BY num_points DESC, team_id ASC''',
            'hints': [
                {'level': 1, 'text': 'Use LEFT JOIN to include all teams (even those with no matches)'},
                {'level': 2, 'text': 'Join condition: team_id = host_team OR team_id = guest_team'},
                {'level': 3, 'text': 'Use CASE to calculate points: 3 for win, 1 for draw, 0 for loss'},
                {'level': 4, 'text': 'Handle both scenarios: when team is host and when team is guest'},
                {'level': 5, 'text': 'Use SUM() to aggregate points and GROUP BY team_id, team_name'}
            ],
            'tags': ['CASE', 'LEFT JOIN', 'SUM', 'GROUP BY', 'Conditional Aggregation']
        },
        
        # WS10-3: Department Salary Comparison (Homework)
        {
            'title': 'WS10-3: Department Salary Comparison',
            'description': '''Write an SQL query to report the comparison result (higher/lower/same) of the average salary of employees in a department to the company's average salary.
Return the result table in any order.

Payment table:
+----+-----------+--------+------------+
| id | intern_id | amount | pay_date   |
+----+-----------+--------+------------+
| 1  | 1         | 9000   | 2017-03-31 |
| 2  | 2         | 6000   | 2017-03-31 |
| 3  | 3         | 10000  | 2017-03-31 |
| 4  | 1         | 7000   | 2017-02-28 |
| 5  | 2         | 6000   | 2017-02-28 |
| 6  | 3         | 8000   | 2017-02-28 |
+----+-----------+--------+------------+

Intern table:
+-----------+---------------+
| intern_id | department_id |
+-----------+---------------+
| 1         | 1             |
| 2         | 2             |
| 3         | 2             |
+-----------+---------------+

Expected output:
+-----------+---------------+------------+
| pay_month | department_id | comparison |
+-----------+---------------+------------+
| 2017-02   | 1             | same       |
| 2017-03   | 1             | higher     |
| 2017-02   | 2             | same       |
| 2017-03   | 2             | lower      |
+-----------+---------------+------------+''',
            'difficulty': 'hard',
            'order': 103,
            'expected_sql': '''WITH MonthlyAvg AS (
    SELECT 
        DATE_FORMAT(pay_date, '%Y-%m') AS pay_month,
        AVG(amount) AS company_avg
    FROM Payment
    GROUP BY pay_month
),
DeptAvg AS (
    SELECT 
        DATE_FORMAT(p.pay_date, '%Y-%m') AS pay_month,
        i.department_id,
        AVG(p.amount) AS dept_avg
    FROM Payment p
    JOIN Intern i ON p.intern_id = i.intern_id
    GROUP BY pay_month, i.department_id
)
SELECT 
    d.pay_month,
    d.department_id,
    CASE
        WHEN d.dept_avg > m.company_avg THEN 'higher'
        WHEN d.dept_avg < m.company_avg THEN 'lower'
        ELSE 'same'
    END AS comparison
FROM DeptAvg d
JOIN MonthlyAvg m ON d.pay_month = m.pay_month
ORDER BY d.pay_month, d.department_id''',
            'initial_query': '''WITH MonthlyAvg AS (
    SELECT 
        DATE_FORMAT(pay_date, '%Y-%m') AS pay_month,
        -- Calculate company average
    FROM Payment
    GROUP BY pay_month
),
DeptAvg AS (
    SELECT 
        DATE_FORMAT(p.pay_date, '%Y-%m') AS pay_month,
        i.department_id,
        -- Calculate department average
    FROM Payment p
    JOIN Intern i ON p.intern_id = i.intern_id
    GROUP BY pay_month, i.department_id
)
SELECT 
    d.pay_month,
    d.department_id,
    CASE
        WHEN -- Department avg > company avg
        WHEN -- Department avg < company avg
        ELSE -- Same
    END AS comparison
FROM DeptAvg d
JOIN MonthlyAvg m ON d.pay_month = m.pay_month''',
            'hints': [
                {'level': 1, 'text': 'Use WITH clause to create two CTEs: one for company average, one for department average'},
                {'level': 2, 'text': 'Use DATE_FORMAT(pay_date, "%Y-%m") to group by month'},
                {'level': 3, 'text': 'Calculate company average across all payments for each month'},
                {'level': 4, 'text': 'Calculate department average by joining Payment and Intern tables'},
                {'level': 5, 'text': 'Use CASE to compare dept_avg with company_avg and return higher/lower/same'}
            ],
            'tags': ['WITH', 'CTE', 'CASE', 'AVG', 'DATE_FORMAT', 'JOIN', 'Multiple CTEs']
        },
        
        # WS11-1: Monthly Transactions II
        {
            'title': 'WS11-1: Monthly Transactions II',
            'description': '''Write an SQL query to find for each month and country: the number of approved transactions and their total amount, the number of chargebacks, and their total amount.
Note: In your query, given the month and country, ignore rows with all zeros.

Transactions table:
+-----+---------+----------+--------+------------+
| id  | country | state    | amount | trans_date |
+-----+---------+----------+--------+------------+
| 101 | US      | approved | 1000   | 2019-05-18 |
| 102 | US      | declined | 2000   | 2019-05-19 |
| 103 | US      | approved | 3000   | 2019-06-10 |
| 104 | US      | declined | 4000   | 2019-06-13 |
| 105 | US      | approved | 5000   | 2019-06-15 |
+-----+---------+----------+--------+------------+

Chargebacks table:
+----------+------------+
| trans_id | trans_date |
+----------+------------+
| 102      | 2019-05-29 |
| 101      | 2019-06-30 |
| 105      | 2019-09-18 |
+----------+------------+

Expected output:
+---------+---------+----------------+-----------------+------------------+-------------------+
| month   | country | approved_count | approved_amount | chargeback_count | chargeback_amount |
+---------+---------+----------------+-----------------+------------------+-------------------+
| 2019-05 | US      | 1              | 1000            | 1                | 2000              |
| 2019-06 | US      | 2              | 8000            | 1                | 1000              |
| 2019-09 | US      | 0              | 0               | 1                | 5000              |
+---------+---------+----------------+-----------------+------------------+-------------------+''',
            'difficulty': 'medium',
            'order': 111,
            'expected_sql': '''WITH CTE AS (
    SELECT
        id, country, state, amount,
        DATE_FORMAT(trans_date, '%Y-%m') AS month
    FROM Transactions
    WHERE state = 'approved'
    UNION
    SELECT
        c.trans_id, t.country, 'chargeback' AS state, t.amount,
        DATE_FORMAT(c.trans_date, '%Y-%m') AS month
    FROM Chargebacks c
    LEFT JOIN Transactions t ON c.trans_id = t.id
)
SELECT
    month,
    country,
    SUM(IF(state='approved', 1, 0)) AS approved_count,
    SUM(IF(state='approved', amount, 0)) AS approved_amount,
    SUM(IF(state='chargeback', 1, 0)) AS chargeback_count,
    SUM(IF(state='chargeback', amount, 0)) AS chargeback_amount
FROM CTE
GROUP BY month, country''',
            'initial_query': '''WITH CTE AS (
    SELECT
        id, country, state, amount,
        DATE_FORMAT(trans_date, '%Y-%m') AS month
    FROM Transactions
    WHERE state = 'approved'
    UNION
    SELECT
        -- Get chargeback transactions
    FROM Chargebacks c
    LEFT JOIN Transactions t ON c.trans_id = t.id
)
SELECT
    month,
    country,
    SUM(IF(state='approved', 1, 0)) AS approved_count,
    -- Add other aggregate calculations
FROM CTE
GROUP BY month, country''',
            'hints': [
                {'level': 1, 'text': 'Use UNION to combine approved transactions and chargebacks into one result set'},
                {'level': 2, 'text': 'First SELECT: get approved transactions with their original trans_date'},
                {'level': 3, 'text': 'Second SELECT: get chargebacks with chargeback trans_date, join to get country and amount'},
                {'level': 4, 'text': 'Use DATE_FORMAT(trans_date, "%Y-%m") to format dates as month'},
                {'level': 5, 'text': 'Use IF() or CASE with SUM() to count and sum separately for approved vs chargeback'}
            ],
            'tags': ['UNION', 'WITH', 'CTE', 'IF', 'SUM', 'DATE_FORMAT', 'LEFT JOIN', 'Conditional Aggregation']
        },
        
        # WS11-2: Tree Node
        {
            'title': 'WS11-2: Tree Node Classification',
            'description': '''Each node in the tree can be one of three types:
• "Leaf": if the node is a leaf node
• "Root": if the node is the root of the tree
• "Inner": if the node is neither a leaf node nor a root node

Write an SQL query to report the type of each node in the tree.
Return the result table ordered by id in ascending order.

Tree table:
+----+------+
| id | p_id |
+----+------+
| 1  | null |
| 2  | 1    |
| 3  | 1    |
| 4  | 2    |
| 5  | 2    |
+----+------+

Expected output:
+----+-------+
| id | type  |
+----+-------+
| 1  | Root  |
| 2  | Inner |
| 3  | Leaf  |
| 4  | Leaf  |
| 5  | Leaf  |
+----+-------+''',
            'difficulty': 'medium',
            'order': 112,
            'expected_sql': '''SELECT id, 'Root' AS Type
FROM tree
WHERE p_id IS NULL
UNION
SELECT id, 'Leaf' AS Type
FROM tree
WHERE id NOT IN (
    SELECT DISTINCT p_id
    FROM tree
    WHERE p_id IS NOT NULL
)
AND p_id IS NOT NULL
UNION
SELECT id, 'Inner' AS Type
FROM tree
WHERE id IN (
    SELECT DISTINCT p_id
    FROM tree
    WHERE p_id IS NOT NULL
)
AND p_id IS NOT NULL
ORDER BY id''',
            'initial_query': '''SELECT id, 'Root' AS Type
FROM tree
WHERE -- Condition for root node
UNION
SELECT id, 'Leaf' AS Type
FROM tree
WHERE -- Condition for leaf node
UNION
SELECT id, 'Inner' AS Type
FROM tree
WHERE -- Condition for inner node
ORDER BY id''',
            'hints': [
                {'level': 1, 'text': 'Use UNION to combine three separate queries for Root, Leaf, and Inner nodes'},
                {'level': 2, 'text': 'Root node: p_id IS NULL (has no parent)'},
                {'level': 3, 'text': 'Leaf node: id NOT IN (subquery of all p_id values) AND p_id IS NOT NULL'},
                {'level': 4, 'text': 'Inner node: id IN (subquery of all p_id values) AND p_id IS NOT NULL'},
                {'level': 5, 'text': 'Use subquery: SELECT DISTINCT p_id FROM tree WHERE p_id IS NOT NULL to find parent nodes'}
            ],
            'tags': ['UNION', 'Subquery', 'NOT IN', 'IN', 'Tree Structure', 'DISTINCT']
        },
        
        # WS11-3: Weather Report (Homework)
        {
            'title': 'WS11-3: Continuous Weather Periods',
            'description': '''The weather can be ONLY either 'Cloudy' or 'Clear'.
Write an SQL query to generate a report of period_state for each continuous interval of days in the period from 2019-01-01 to 2019-12-31.

period_state is 'cloudy' if weather in this interval cloudy or 'clear' if weather in this interval clear. 
Interval of days are retrieved as start_date and end_date.
Return the result table ordered by start_date.

Cloudy table:
+------------+
| fail_date  |
+------------+
| 2018-12-28 |
| 2018-12-29 |
| 2019-01-04 |
| 2019-01-05 |
+------------+

Clear table:
+--------------+
| success_date |
+--------------+
| 2018-12-30   |
| 2018-12-31   |
| 2019-01-01   |
| 2019-01-02   |
| 2019-01-03   |
| 2019-01-06   |
+--------------+

Expected output:
+--------------+------------+------------+
| period_state | start_date | end_date   |
+--------------+------------+------------+
| clear        | 2019-01-01 | 2019-01-03 |
| cloudy       | 2019-01-04 | 2019-01-05 |
| clear        | 2019-01-06 | 2019-01-06 |
+--------------+------------+------------+''',
            'difficulty': 'hard',
            'order': 113,
            'expected_sql': '''WITH AllDates AS (
    SELECT fail_date AS date, 'cloudy' AS state
    FROM Cloudy
    WHERE fail_date BETWEEN '2019-01-01' AND '2019-12-31'
    UNION
    SELECT success_date AS date, 'clear' AS state
    FROM Clear
    WHERE success_date BETWEEN '2019-01-01' AND '2019-12-31'
),
Ranked AS (
    SELECT 
        date,
        state,
        ROW_NUMBER() OVER (ORDER BY date) AS rn,
        ROW_NUMBER() OVER (PARTITION BY state ORDER BY date) AS state_rn
    FROM AllDates
)
SELECT 
    state AS period_state,
    MIN(date) AS start_date,
    MAX(date) AS end_date
FROM Ranked
GROUP BY state, (rn - state_rn)
ORDER BY start_date''',
            'initial_query': '''WITH AllDates AS (
    SELECT fail_date AS date, 'cloudy' AS state
    FROM Cloudy
    WHERE fail_date BETWEEN '2019-01-01' AND '2019-12-31'
    UNION
    SELECT success_date AS date, 'clear' AS state
    FROM Clear
    WHERE success_date BETWEEN '2019-01-01' AND '2019-12-31'
),
Ranked AS (
    SELECT 
        date,
        state,
        -- Add ROW_NUMBER() window functions
    FROM AllDates
)
SELECT 
    state AS period_state,
    MIN(date) AS start_date,
    MAX(date) AS end_date
FROM Ranked
GROUP BY -- Group by condition
ORDER BY start_date''',
            'hints': [
                {'level': 1, 'text': 'Use UNION to combine cloudy and clear dates into one table with state column'},
                {'level': 2, 'text': 'Filter dates to be between 2019-01-01 and 2019-12-31'},
                {'level': 3, 'text': 'Use ROW_NUMBER() OVER (ORDER BY date) to assign sequential numbers to all dates'},
                {'level': 4, 'text': 'Use ROW_NUMBER() OVER (PARTITION BY state ORDER BY date) to assign numbers within each state'},
                {'level': 5, 'text': 'The difference (rn - state_rn) is constant for consecutive dates with same state'},
                {'level': 6, 'text': 'GROUP BY state and (rn - state_rn) to find continuous periods, use MIN/MAX for start/end dates'}
            ],
            'tags': ['UNION', 'WITH', 'CTE', 'ROW_NUMBER', 'Window Functions', 'GROUP BY', 'Date Ranges', 'Islands and Gaps']
        }
    ]
    
    # 批量创建练习题
    created_count = 0
    updated_count = 0
    
    for data in exercises_data:
        exercise, created = Exercise.objects.update_or_create(
            schema=schema,
            title=data['title'],
            defaults={
                'description': data['description'],
                'difficulty': data['difficulty'],
                'order': data['order'],
                'expected_sql': data['expected_sql'],
                'initial_query': data['initial_query'],
                'hints': data['hints'],
                'tags': data['tags']
            }
        )
        
        if created:
            created_count += 1
            print(f"✓ Created: {data['title']}")
        else:
            updated_count += 1
            print(f"↻ Updated: {data['title']}")
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Created: {created_count} exercises")
    print(f"  Updated: {updated_count} exercises")
    print(f"  Total:   {created_count + updated_count} exercises")
    print(f"{'='*60}")

if __name__ == '__main__':
    add_exercises()
