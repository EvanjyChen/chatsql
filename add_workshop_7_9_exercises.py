"""
批量添加 SQL Workshop 7-9 练习题

推荐使用方式：
    python manage.py shell < add_workshop_7_9_exercises.py
"""

from exercises.models import DatabaseSchema, Exercise


def add_exercises():
    # 获取或创建数据库模式
    schema, created = DatabaseSchema.objects.get_or_create(
        name="demo_sql_workshop",
        defaults={
            "display_name": "SQL Workshop Database",
            "description": "Database schema for SQL workshop exercises",
            "db_name": "practice_workshop",
            "schema_sql": """
                CREATE TABLE Products (
                    product_id INT PRIMARY KEY,
                    new_price DECIMAL(10,2),
                    change_date DATE
                );
                CREATE TABLE Sales (
                    seller_id INT,
                    product_id INT,
                    buyer_id INT,
                    sale_date DATE,
                    quantity INT,
                    price DECIMAL(10,2)
                );
                CREATE TABLE Product (
                    product_id INT PRIMARY KEY,
                    product_name VARCHAR(100),
                    unit_price DECIMAL(10,2)
                );
                CREATE TABLE Class (
                    class_id INT,
                    student_id INT
                );
                CREATE TABLE Student (
                    student_id INT PRIMARY KEY,
                    name VARCHAR(100),
                    experience_years INT
                );
                CREATE TABLE Players (
                    player_id INT PRIMARY KEY,
                    group_id INT
                );
                CREATE TABLE Matches (
                    match_id INT PRIMARY KEY,
                    first_player INT,
                    second_player INT,
                    first_score INT,
                    second_score INT
                );
                CREATE TABLE Events (
                    business_id INT,
                    event_type VARCHAR(50),
                    occurences INT
                );
                CREATE TABLE Interns (
                    id INT PRIMARY KEY,
                    name VARCHAR(100),
                    department VARCHAR(50),
                    mentorId INT
                );
                CREATE TABLE Employee (
                    employee_id INT PRIMARY KEY,
                    team_id INT
                );
                CREATE TABLE Scores (
                    player_name VARCHAR(100),
                    gender CHAR(1),
                    day DATE,
                    score_points INT
                );
            """,
            "seed_sql": """
                INSERT INTO Products VALUES 
                    (1, 20, '2019-08-14'),
                    (2, 50, '2019-08-14'),
                    (1, 30, '2019-08-15'),
                    (1, 35, '2019-08-16'),
                    (2, 65, '2019-08-17'),
                    (3, 20, '2019-08-18');
            """,
        },
    )

    print(f"{'Created' if created else 'Using existing'} schema: {schema.name}")

    # Workshop 7-9 练习题
    exercises_data = [
        # WS7-1: Product Price at a Given Date
        {
            "title": "WS7-1: Product Price at a Given Date",
            "description": """Write an SQL query to find the prices of all products on 2019-08-16.

Assume the price of all products before any change is 10.

Return the result table in any order.

Products table:

+------------+-----------+-------------+
| product_id | new_price | change_date |
+------------+-----------+-------------+
| 1          | 20        | 2019-08-14  |
| 2          | 50        | 2019-08-14  |
| 1          | 30        | 2019-08-15  |
| 1          | 35        | 2019-08-16  |
| 2          | 65        | 2019-08-17  |
| 3          | 20        | 2019-08-18  |
+------------+-----------+-------------+

Expected output:

+------------+-------+
| product_id | price |
+------------+-------+
| 2          | 50    |
| 1          | 35    |
| 3          | 10    |
+------------+-------+""",
            "difficulty": "medium",
            "order": 71,
            "expected_sql": """WITH cte AS (
    SELECT *,
        RANK() OVER (PARTITION BY product_id ORDER BY change_date DESC) AS rnk
    FROM Products
    WHERE change_date <= "2019-08-16"
)
SELECT DISTINCT p.product_id,
    IFNULL(t.new_price, 10) AS price
FROM Products p 
LEFT JOIN (SELECT * FROM cte WHERE rnk=1) t 
    USING (product_id)""",
            "initial_query": """WITH cte AS (
    SELECT *,
        -- Add ranking function here
    FROM Products
    WHERE change_date <= "2019-08-16"
)
-- Complete the query
SELECT 
FROM Products p""",
            "hints": [
                {
                    "level": 1,
                    "text": "Use WITH clause to create a CTE (Common Table Expression) for temporary results",
                },
                {
                    "level": 2,
                    "text": "Use RANK() window function to get the latest price change on or before 2019-08-16",
                },
                {
                    "level": 3,
                    "text": "PARTITION BY product_id and ORDER BY change_date DESC to get the most recent change",
                },
                {
                    "level": 4,
                    "text": "Use LEFT JOIN to get all products, and IFNULL() to set default price of 10",
                },
            ],
            "tags": ["WITH", "CTE", "Window Functions", "RANK", "LEFT JOIN", "IFNULL"],
        },
        # WS7-2: Sales Analysis I
        {
            "title": "WS7-2: Sales Analysis I",
            "description": """Write an SQL query that reports the best seller by total sales price. If there is a tie, report them all.

Return the result table in any order.

Product table:

+------------+--------------+------------+
| product_id | product_name | unit_price |
+------------+--------------+------------+
| 1          | S8           | 1000       |
| 2          | G4           | 800        |
| 3          | iPhone       | 1400       |
+------------+--------------+------------+

Sales table:

+-----------+------------+----------+------------+----------+-------+
| seller_id | product_id | buyer_id | sale_date  | quantity | price |
+-----------+------------+----------+------------+----------+-------+
| 1         | 1          | 1        | 2019-01-21 | 2        | 2000  |
| 1         | 2          | 2        | 2019-02-17 | 1        | 800   |
| 2         | 2          | 3        | 2019-06-02 | 1        | 800   |
| 3         | 3          | 4        | 2019-05-13 | 2        | 2800  |
+-----------+------------+----------+------------+----------+-------+

Expected output:

+-----------+
| seller_id |
+-----------+
| 1         |
| 3         |
+-----------+""",
            "difficulty": "medium",
            "order": 72,
            "expected_sql": """WITH cte AS (
    SELECT seller_id,
        DENSE_RANK() OVER (ORDER BY SUM(price) DESC) AS rk
    FROM sales
    GROUP BY seller_id
)
SELECT seller_id 
FROM cte 
WHERE rk = 1""",
            "initial_query": """WITH cte AS (
    SELECT seller_id,
        -- Add window function here
    FROM sales
    GROUP BY seller_id
)
SELECT seller_id FROM cte""",
            "hints": [
                {
                    "level": 1,
                    "text": "Use WITH clause to create a temporary table with rankings",
                },
                {
                    "level": 2,
                    "text": "Use DENSE_RANK() to rank sellers by total sales (no gaps in ranking for ties)",
                },
                {
                    "level": 3,
                    "text": "Use SUM(price) with GROUP BY seller_id to calculate total sales per seller",
                },
                {
                    "level": 4,
                    "text": "Filter WHERE rk = 1 to get all top sellers in case of ties",
                },
            ],
            "tags": ["WITH", "CTE", "Window Functions", "DENSE_RANK", "GROUP BY", "Aggregate"],
        },
        # WS7-3: Most Experienced Students
        {
            "title": "WS7-3: Most Experienced Students",
            "description": """Write an SQL query that reports the most experienced student in each class. In case of a tie, report all students with the maximum number of experience years.

Return the result table in any order.

Class table:

+----------+------------+
| class_id | student_id |
+----------+------------+
| 1        | 1          |
| 1        | 2          |
| 1        | 3          |
| 2        | 1          |
| 2        | 4          |
+----------+------------+

Student table:

+------------+--------+------------------+
| student_id | name   | experience_years |
+------------+--------+------------------+
| 1          | Khaled | 3                |
| 2          | Ali    | 2                |
| 3          | John   | 1                |
| 4          | Doe    | 2                |
+------------+--------+------------------+

Expected output:

+----------+------------+
| class_id | student_id |
+----------+------------+
| 1        | 1          |
| 2        | 1          |
+----------+------------+""",
            "difficulty": "medium",
            "order": 73,
            "expected_sql": """WITH cte AS (
    SELECT c.class_id, c.student_id, s.experience_years,
        DENSE_RANK() OVER (PARTITION BY c.class_id ORDER BY s.experience_years DESC) AS rk
    FROM Class c
    JOIN Student s ON c.student_id = s.student_id
)
SELECT class_id, student_id
FROM cte
WHERE rk = 1""",
            "initial_query": """WITH cte AS (
    SELECT c.class_id, c.student_id, s.experience_years,
        -- Add window function here
    FROM Class c
    JOIN Student s ON c.student_id = s.student_id
)
SELECT class_id, student_id FROM cte""",
            "hints": [
                {
                    "level": 1,
                    "text": "Use WITH clause to create a CTE with rankings by class",
                },
                {
                    "level": 2,
                    "text": "Join Class and Student tables to get experience_years",
                },
                {
                    "level": 3,
                    "text": "Use DENSE_RANK() with PARTITION BY class_id ORDER BY experience_years DESC",
                },
                {
                    "level": 4,
                    "text": "Filter WHERE rk = 1 to get the most experienced students in each class",
                },
            ],
            "tags": ["WITH", "CTE", "Window Functions", "DENSE_RANK", "PARTITION BY", "JOIN"],
        },
        # WS8-1: Tournament Winners
        {
            "title": "WS8-1: Tournament Winners",
            "description": """The winner in each group is the player who scored the maximum total points within the group. In case of a tie, the lowest player_id wins.

Write an SQL query to find the winner in each group.

Players table:

+-----------+----------+
| player_id | group_id |
+-----------+----------+
| 15        | 1        |
| 25        | 1        |
| 30        | 1        |
| 45        | 1        |
| 10        | 2        |
| 35        | 2        |
| 50        | 2        |
| 20        | 3        |
| 40        | 3        |
+-----------+----------+

Matches table:

+----------+--------------+---------------+-------------+--------------+
| match_id | first_player | second_player | first_score | second_score |
+----------+--------------+---------------+-------------+--------------+
| 1        | 15           | 45            | 3           | 0            |
| 2        | 30           | 25            | 1           | 2            |
| 3        | 30           | 15            | 2           | 0            |
| 4        | 40           | 20            | 5           | 2            |
| 5        | 35           | 50            | 1           | 1            |
+----------+--------------+---------------+-------------+--------------+

Expected output:

+----------+-----------+
| group_id | player_id |
+----------+-----------+
| 1        | 15        |
| 2        | 35        |
| 3        | 40        |
+----------+-----------+""",
            "difficulty": "hard",
            "order": 81,
            "expected_sql": """SELECT group_id, MIN(player_id) AS player_id
FROM Players, (
    SELECT player, SUM(score) AS score
    FROM (
        SELECT first_player AS player, first_score AS score
        FROM Matches
        UNION ALL
        SELECT second_player, second_score
        FROM Matches
    ) s
    GROUP BY player
) PlayerScores
WHERE Players.player_id = PlayerScores.player
    AND (group_id, score) IN (
        SELECT group_id, MAX(score)
        FROM Players, (
            SELECT player, SUM(score) AS score
            FROM (
                SELECT first_player AS player, first_score AS score
                FROM Matches
                UNION ALL
                SELECT second_player, second_score
                FROM Matches
            ) s
            GROUP BY player
        ) PlayerScores
        WHERE Players.player_id = PlayerScores.player
        GROUP BY group_id
    )
GROUP BY group_id""",
            "initial_query": """SELECT group_id, player_id
FROM Players, (
    -- Create inline view to calculate total scores
    SELECT player, SUM(score) AS score
    FROM (
        -- Union all scores from both player columns
    ) s
    GROUP BY player
) PlayerScores
WHERE -- Add join condition and filtering""",
            "hints": [
                {
                    "level": 1,
                    "text": "Use inline view (derived table) to calculate total scores for each player",
                },
                {
                    "level": 2,
                    "text": "Use UNION ALL to combine first_player scores and second_player scores",
                },
                {
                    "level": 3,
                    "text": "Calculate MAX(score) for each group_id to find the winning score",
                },
                {
                    "level": 4,
                    "text": "Use MIN(player_id) when (group_id, score) matches the max score to handle ties",
                },
            ],
            "tags": ["Inline View", "Derived Table", "UNION ALL", "Aggregate", "GROUP BY", "Subquery"],
        },
        # WS8-2: Active Businesses
        {
            "title": "WS8-2: Active Businesses",
            "description": """The average activity for a particular event_type is the average occurrences across all companies that have this event.

An active business is a business that has more than one event_type such that their occurrences is strictly greater than the average activity for that event.

Write an SQL query to find all active businesses.

Events table:

+-------------+------------+------------+
| business_id | event_type | occurences |
+-------------+------------+------------+
| 1           | reviews    | 7          |
| 3           | reviews    | 3          |
| 1           | ads        | 11         |
| 2           | ads        | 7          |
| 3           | ads        | 6          |
| 1           | page views | 3          |
| 2           | page views | 12         |
+-------------+------------+------------+

Expected output:

+-------------+
| business_id |
+-------------+
| 1           |
+-------------+""",
            "difficulty": "medium",
            "order": 82,
            "expected_sql": """SELECT business_id
FROM (
    SELECT event_type, AVG(occurences) AS ave_occurences
    FROM events AS e1
    GROUP BY event_type
) AS temp1
JOIN events AS e2 ON temp1.event_type = e2.event_type
WHERE e2.occurences > temp1.ave_occurences
GROUP BY business_id
HAVING COUNT(DISTINCT temp1.event_type) > 1""",
            "initial_query": """SELECT business_id
FROM (
    -- Calculate average occurrences for each event_type
    SELECT event_type, AVG(occurences) AS ave_occurences
    FROM events
    GROUP BY event_type
) AS temp1
JOIN events AS e2 ON -- Add join condition
WHERE -- Add filtering condition
GROUP BY business_id
HAVING -- Add having condition""",
            "hints": [
                {
                    "level": 1,
                    "text": "Create an inline view to calculate average occurrences for each event_type",
                },
                {
                    "level": 2,
                    "text": "Join this inline view with the Events table on event_type",
                },
                {
                    "level": 3,
                    "text": "Filter WHERE occurences > ave_occurences to find above-average events",
                },
                {
                    "level": 4,
                    "text": "Use HAVING COUNT(DISTINCT event_type) > 1 to find businesses with multiple above-average events",
                },
            ],
            "tags": ["Inline View", "Derived Table", "JOIN", "AVG", "GROUP BY", "HAVING", "Aggregate"],
        },
        # WS8-3: Mentors with Five Direct Reports
        {
            "title": "WS8-3: Mentors with Five Direct Reports",
            "description": """If mentorId is null, then the intern does not have a mentor.

Write an SQL query to report the mentors with at least five direct reports.

Return the result table in any order.

Interns table:

+-----+-------+------------+-----------+
| id  | name  | department | mentorId  |
+-----+-------+------------+-----------+
| 101 | John  | A          | None      |
| 102 | Dan   | A          | 101       |
| 103 | James | A          | 101       |
| 104 | Amy   | A          | 101       |
| 105 | Anne  | A          | 101       |
| 106 | Ron   | B          | 101       |
+-----+-------+------------+-----------+

Expected output:

+------+
| name |
+------+
| John |
+------+""",
            "difficulty": "easy",
            "order": 83,
            "expected_sql": """SELECT i1.name
FROM Interns i1
JOIN (
    SELECT mentorId, COUNT(*) AS report_count
    FROM Interns
    WHERE mentorId IS NOT NULL
    GROUP BY mentorId
    HAVING COUNT(*) >= 5
) i2 ON i1.id = i2.mentorId""",
            "initial_query": """SELECT i1.name
FROM Interns i1
JOIN (
    -- Create inline view to count direct reports
    SELECT mentorId, COUNT(*) AS report_count
    FROM Interns
    WHERE -- Filter condition
    GROUP BY mentorId
    HAVING -- Having condition
) i2 ON -- Join condition""",
            "hints": [
                {
                    "level": 1,
                    "text": "Create an inline view that counts direct reports for each mentor",
                },
                {
                    "level": 2,
                    "text": "Filter WHERE mentorId IS NOT NULL to exclude interns without mentors",
                },
                {
                    "level": 3,
                    "text": "Use HAVING COUNT(*) >= 5 to find mentors with at least 5 direct reports",
                },
                {
                    "level": 4,
                    "text": "Join with the original table on id = mentorId to get mentor names",
                },
            ],
            "tags": ["Inline View", "Derived Table", "JOIN", "COUNT", "GROUP BY", "HAVING", "Aggregate"],
        },
        # WS9-1: Team Size for Each Employee
        {
            "title": "WS9-1: Team Size for Each Employee",
            "description": """Write an SQL query to find the team size of each of the employees.

Return result table in any order.

Employee Table:

+-------------+---------+
| employee_id | team_id |
+-------------+---------+
| 1           | 8       |
| 2           | 8       |
| 3           | 8       |
| 4           | 7       |
| 5           | 9       |
| 6           | 9       |
+-------------+---------+

Expected output:

+-------------+-----------+
| employee_id | team_size |
+-------------+-----------+
| 1           | 3         |
| 2           | 3         |
| 3           | 3         |
| 4           | 1         |
| 5           | 2         |
| 6           | 2         |
+-------------+-----------+""",
            "difficulty": "easy",
            "order": 91,
            "expected_sql": """SELECT employee_id, 
    COUNT(*) OVER(PARTITION BY team_id) AS team_size
FROM employee""",
            "initial_query": """SELECT employee_id, 
    -- Add window function here
FROM employee""",
            "hints": [
                {
                    "level": 1,
                    "text": "Use a window function to count employees per team without reducing rows",
                },
                {
                    "level": 2,
                    "text": "Use COUNT(*) OVER() with PARTITION BY team_id",
                },
                {
                    "level": 3,
                    "text": "Window function preserves all rows while adding aggregate information",
                },
            ],
            "tags": ["Window Functions", "COUNT", "PARTITION BY", "OVER"],
        },
        # WS9-2: Running Total for Different Genders
        {
            "title": "WS9-2: Running Total for Different Genders",
            "description": """Write an SQL query to find the total score for each gender on each day.

Return the result table ordered by gender and day in ascending order.

Scores table:

+-------------+--------+------------+--------------+
| player_name | gender | day        | score_points |
+-------------+--------+------------+--------------+
| Aron        | F      | 2020-01-01 | 17           |
| Alice       | F      | 2020-01-07 | 23           |
| Bajrang     | M      | 2020-01-07 | 7            |
| Khali       | M      | 2019-12-25 | 11           |
| Slaman      | M      | 2019-12-30 | 13           |
| Joe         | M      | 2019-12-31 | 3            |
| Jose        | M      | 2019-12-18 | 2            |
| Priya       | F      | 2019-12-31 | 23           |
| Priyanka    | F      | 2019-12-30 | 17           |
+-------------+--------+------------+--------------+

Expected output:

+--------+------------+-------+
| gender | day        | total |
+--------+------------+-------+
| F      | 2019-12-30 | 17    |
| F      | 2019-12-31 | 40    |
| F      | 2020-01-01 | 57    |
| F      | 2020-01-07 | 80    |
| M      | 2019-12-18 | 2     |
| M      | 2019-12-25 | 13    |
| M      | 2019-12-30 | 26    |
| M      | 2019-12-31 | 29    |
| M      | 2020-01-07 | 36    |
+--------+------------+-------+""",
            "difficulty": "medium",
            "order": 92,
            "expected_sql": """SELECT gender, day,
    SUM(score_points) OVER(PARTITION BY gender ORDER BY day 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total
FROM Scores""",
            "initial_query": """SELECT gender, day,
    SUM(score_points) OVER(
        PARTITION BY -- Partition column
        ORDER BY -- Order column
        -- Add window frame clause
    ) AS total
FROM Scores""",
            "hints": [
                {
                    "level": 1,
                    "text": "Use window function with PARTITION BY gender to calculate running total per gender",
                },
                {
                    "level": 2,
                    "text": "Use ORDER BY day to ensure cumulative sum is calculated chronologically",
                },
                {
                    "level": 3,
                    "text": "With ORDER BY, default frame is ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW",
                },
                {
                    "level": 4,
                    "text": "This creates a running total that accumulates scores from all previous days and current day",
                },
            ],
            "tags": ["Window Functions", "SUM", "PARTITION BY", "ORDER BY", "ROWS BETWEEN", "Running Total"],
        },
        # WS9-3: Highest Sales per Employee (Window Function)
        {
            "title": "WS9-3: Highest Sales per Employee (Window Function)",
            "description": """Write a SQL query to find the highest sales with its corresponding product for each employee. In case of a tie, you should find the product with the smallest product_id.

Return the result table ordered by employee_id in ascending order.

You must use Window Function for this problem.

Sales:

+-------------+------------+-------+
| employee_id | product_id | sales |
+-------------+------------+-------+
| 2           | 2          | 95    |
| 2           | 3          | 95    |
| 1           | 1          | 90    |
| 1           | 2          | 99    |
| 3           | 1          | 80    |
| 3           | 2          | 82    |
| 3           | 3          | 82    |
+-------------+------------+-------+

Expected output:

+-------------+------------+-------+
| employee_id | product_id | sales |
+-------------+------------+-------+
| 1           | 2          | 99    |
| 2           | 2          | 95    |
| 3           | 2          | 82    |
+-------------+------------+-------+""",
            "difficulty": "medium",
            "order": 93,
            "expected_sql": """WITH cte AS (
    SELECT employee_id, product_id, sales,
        RANK() OVER(PARTITION BY employee_id ORDER BY sales DESC, product_id ASC) AS rk
    FROM Sales
)
SELECT employee_id, product_id, sales
FROM cte
WHERE rk = 1
ORDER BY employee_id""",
            "initial_query": """WITH cte AS (
    SELECT employee_id, product_id, sales,
        -- Add window function with proper ordering
    FROM Sales
)
SELECT employee_id, product_id, sales
FROM cte
WHERE -- Filter condition
ORDER BY employee_id""",
            "hints": [
                {
                    "level": 1,
                    "text": "Use RANK() window function with PARTITION BY employee_id",
                },
                {
                    "level": 2,
                    "text": "ORDER BY sales DESC to get highest sales first",
                },
                {
                    "level": 3,
                    "text": "Add product_id ASC as secondary ordering to handle ties",
                },
                {
                    "level": 4,
                    "text": "Filter WHERE rk = 1 to get the top sale for each employee",
                },
            ],
            "tags": ["Window Functions", "RANK", "PARTITION BY", "ORDER BY", "WITH", "CTE"],
        },
    ]

    # 批量创建 / 更新练习题
    created_count = 0
    updated_count = 0

    for data in exercises_data:
        exercise, created = Exercise.objects.update_or_create(
            schema=schema,
            title=data["title"],
            defaults={
                "description": data["description"],
                "difficulty": data["difficulty"],
                "order": data["order"],
                "expected_sql": data["expected_sql"],
                "initial_query": data["initial_query"],
                "hints": data["hints"],
                "tags": data["tags"],
            },
        )

        if created:
            created_count += 1
            print(f"✓ Created: {data['title']}")
        else:
            updated_count += 1
            print(f"↻ Updated: {data['title']}")

    print(f"\n{'=' * 60}")
    print("Summary:")
    print(f"  Created: {created_count} exercises")
    print(f"  Updated: {updated_count} exercises")
    print(f"  Total:   {created_count + updated_count} exercises")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    add_exercises()



