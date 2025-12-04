"""
批量添加 SQL Workshop 3-6 练习题

使用方法:
    python manage.py shell < add_multiple_exercises.py
"""

from exercises.models import DatabaseSchema, Exercise


def add_exercises():
    """添加 WS3-WS6 的所有练习题"""

    # 获取或创建数据库模式 (假设使用 demo_hr 或创建新的)
    try:
        schema = DatabaseSchema.objects.get(name="demo_hr")
        print(f"✓ 使用现有数据库模式: {schema.name}")
    except DatabaseSchema.DoesNotExist:
        print("⚠ demo_hr 模式不存在，请先创建数据库模式（可先运行 add_workshop_exercises.py）")
        return

    # WS3: Having 相关练习题
    ws3_exercises = [
        {
            "title": "WS3-1: Actors and Directors Who Cooperated At Least Three Times",
            "description": """Write a SQL query for a report that provides the pairs (actor_id, director_id) where the actor has cooperated with the director at least three times.

Return the result table in any order.

ActorDirector table:

+-------------+-------------+-------------+
| actor_id    | director_id | timestamp   |
+-------------+-------------+-------------+
| 1           | 1           | 0           |
| 1           | 1           | 1           |
| 1           | 1           | 2           |
| 1           | 2           | 3           |
| 1           | 2           | 4           |
| 2           | 1           | 5           |
| 2           | 1           | 6           |
+-------------+-------------+-------------+

Expected Output:

+-------------+-------------+
| actor_id    | director_id |
+-------------+-------------+
| 1           | 1           |
+-------------+-------------+""",
            "difficulty": "easy",
            "order": 301,
            "expected_sql": """SELECT actor_id, director_id
FROM ActorDirector
GROUP BY actor_id, director_id
HAVING COUNT(*) >= 3""",
            "initial_query": """SELECT actor_id, director_id
FROM ActorDirector
-- Add your GROUP BY and HAVING clauses here""",
            "hints": [
                {
                    "level": 1,
                    "text": "Check if the condition is before OR after grouping. If after grouping, use HAVING",
                },
                {
                    "level": 2,
                    "text": "GROUP BY should include all grouping factors: actor_id and director_id",
                },
                {
                    "level": 3,
                    "text": "Use COUNT(*) >= 3 in the HAVING clause to filter groups",
                },
            ],
            "tags": ["GROUP BY", "HAVING", "COUNT", "Aggregate Functions"],
        },
        {
            "title": "WS3-2: Article Views II",
            "description": """Write an SQL query to find all the people who viewed more than one article on the same date.

Return the result table sorted by id in ascending order.

Views table:

+------------+-----------+-----------+------------+
| article_id | author_id | viewer_id | view_date  |
+------------+-----------+-----------+------------+
| 1          | 3         | 5         | 2019-08-01 |
| 3          | 4         | 5         | 2019-08-01 |
| 1          | 3         | 6         | 2019-08-02 |
| 2          | 7         | 7         | 2019-08-01 |
| 2          | 7         | 6         | 2019-08-02 |
| 4          | 7         | 1         | 2019-07-22 |
| 3          | 4         | 4         | 2019-07-21 |
| 3          | 4         | 4         | 2019-07-21 |
+------------+-----------+-----------+------------+

Expected Output:

+------+
| id   |
+------+
| 5    |
| 6    |
+------+""",
            "difficulty": "medium",
            "order": 302,
            "expected_sql": """SELECT viewer_id AS id
FROM Views
GROUP BY viewer_id, view_date
HAVING COUNT(DISTINCT article_id) > 1
ORDER BY viewer_id""",
            "initial_query": """SELECT viewer_id AS id
FROM Views
-- Add GROUP BY, HAVING, and ORDER BY clauses""",
            "hints": [
                {
                    "level": 1,
                    "text": "First, find the group by factors: viewer_id and view_date",
                },
                {
                    "level": 2,
                    "text": "What if the same article is viewed multiple times? Use DISTINCT",
                },
                {
                    "level": 3,
                    "text": "Use COUNT(DISTINCT article_id) > 1 in HAVING clause",
                },
                {
                    "level": 4,
                    "text": 'Remember to order by viewer_id and use the alias "id"',
                },
            ],
            "tags": ["GROUP BY", "HAVING", "COUNT", "DISTINCT", "ORDER BY"],
        },
        {
            "title": "WS3-3: Students Who Took All Professor Classes",
            "description": """Write an SQL query to report the student ids from the Student table who took classes offered by all the professors in the Professor table.

Return the result table in any order.

Student table:

+-------------+--------------+
| student_id  | professor_key|
+-------------+--------------+
| 1           | 5            |
| 2           | 6            |
| 3           | 5            |
| 3           | 6            |
| 1           | 6            |
+-------------+--------------+

Professor table:

+---------------+
| professor_key |
+---------------+
| 5             |
| 6             |
+---------------+

Expected Output:

+-------------+
| student_id  |
+-------------+
| 1           |
| 3           |
+-------------+""",
            "difficulty": "medium",
            "order": 303,
            "expected_sql": """SELECT student_id
FROM Student
GROUP BY student_id
HAVING COUNT(DISTINCT professor_key) = (SELECT COUNT(*) FROM Professor)""",
            "initial_query": """SELECT student_id
FROM Student
-- Add GROUP BY and HAVING clauses
-- Hint: Compare count with total professors""",
            "hints": [
                {"level": 1, "text": "Group by student_id to get each student"},
                {
                    "level": 2,
                    "text": "Count distinct professors for each student",
                },
                {
                    "level": 3,
                    "text": "Use a subquery to get the total number of professors",
                },
                {
                    "level": 4,
                    "text": "Compare the count with total using HAVING clause",
                },
            ],
            "tags": ["GROUP BY", "HAVING", "COUNT", "DISTINCT", "Subquery"],
        },
    ]

    # WS4: Subquery 相关练习题
    ws4_exercises = [
        {
            "title": "WS4-1: Game Play Analysis II",
            "description": """Write an SQL query to report the device that is first logged in for each player.

Return the result table in any order.

Activity table:

+-----------+-----------+------------+--------------+
| player_id | device_id | event_date | games_played |
+-----------+-----------+------------+--------------+
| 1         | 2         | 2016-03-01 | 5            |
| 1         | 2         | 2016-05-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-02 | 0            |
| 3         | 4         | 2018-07-03 | 5            |
+-----------+-----------+------------+--------------+

Expected Output:

+-----------+-----------+
| player_id | device_id |
+-----------+-----------+
| 1         | 2         |
| 2         | 3         |
| 3         | 1         |
+-----------+-----------+""",
            "difficulty": "easy",
            "order": 401,
            "expected_sql": """SELECT player_id, device_id
FROM Activity
WHERE (player_id, event_date) IN (
    SELECT player_id, MIN(event_date)
    FROM Activity
    GROUP BY player_id
)""",
            "initial_query": """SELECT player_id, device_id
FROM Activity
WHERE (player_id, event_date) IN (
    -- Write subquery to find first login date for each player
)""",
            "hints": [
                {
                    "level": 1,
                    "text": "Think about data flow: first get player + first date, then join with main table",
                },
                {
                    "level": 2,
                    "text": "Use a subquery with GROUP BY player_id and MIN(event_date)",
                },
                {
                    "level": 3,
                    "text": "Use IN operator to match (player_id, event_date) pairs",
                },
                {"level": 4, "text": "Alternative: You can use JOIN instead of IN"},
            ],
            "tags": ["Subquery", "IN", "GROUP BY", "MIN", "Aggregate Functions"],
        },
        {
            "title": "WS4-2: Page Recommendations",
            "description": """Write an SQL query to recommend pages to the user with user_id = 1 using the pages that your friends liked. It should not recommend pages you already liked.

Return result table in any order without duplicates.

Friendship table:

+----------+----------+
| user1_id | user2_id |
+----------+----------+
| 1        | 2        |
| 1        | 3        |
| 1        | 4        |
| 2        | 3        |
| 2        | 4        |
| 2        | 5        |
| 6        | 1        |
+----------+----------+

Likes table:

+---------+---------+
| user_id | page_id |
+---------+---------+
| 1       | 88      |
| 2       | 23      |
| 3       | 24      |
| 4       | 56      |
| 5       | 11      |
| 6       | 33      |
| 2       | 77      |
| 3       | 77      |
| 6       | 88      |
+---------+---------+

Expected Output:

+------------------+
| recommended_page |
+------------------+
| 23               |
| 24               |
| 56               |
| 33               |
| 77               |
+------------------+""",
            "difficulty": "medium",
            "order": 402,
            "expected_sql": """SELECT DISTINCT page_id AS recommended_page
FROM Likes
WHERE user_id IN (
    SELECT user2_id FROM Friendship WHERE user1_id = 1
    UNION
    SELECT user1_id FROM Friendship WHERE user2_id = 1
)
AND page_id NOT IN (
    SELECT page_id FROM Likes WHERE user_id = 1
)""",
            "initial_query": """SELECT DISTINCT page_id AS recommended_page
FROM Likes
WHERE user_id IN (
    -- Get all friends of user 1
    -- Need to check both user1_id and user2_id
)
AND page_id NOT IN (
    -- Get pages already liked by user 1
)""",
            "hints": [
                {
                    "level": 1,
                    "text": "Data Flow: First get friends from Friendship table",
                },
                {
                    "level": 2,
                    "text": "Friends can appear in either user1_id or user2_id, use UNION to combine",
                },
                {
                    "level": 3,
                    "text": "Then get pages liked by friends, but exclude pages user 1 already likes",
                },
                {
                    "level": 4,
                    "text": "Alternative: You can use WITH clause for better readability",
                },
            ],
            "tags": ["Subquery", "IN", "NOT IN", "UNION", "DISTINCT"],
        },
        {
            "title": "WS4-3: Median from Histogram",
            "description": """The median is the value separating the higher half from the lower half of a data sample.

Write an SQL query to report the median of all the numbers in the database after decompressing the Histogram table. Round the median to one decimal point.

Histogram table:

+-----+-----------+
| bin | frequency |
+-----+-----------+
| 0   | 7         |
| 1   | 1         |
| 2   | 3         |
| 3   | 1         |
+-----+-----------+

The decompressed data would be: [0,0,0,0,0,0,0,1,2,2,2,3]

Total: 12 numbers, median position: (12+1)/2 = 6.5, so average of 6th and 7th values = (0+0)/2 = 0.0

Expected Output:

+--------+
| median |
+--------+
| 0.0    |
+--------+""",
            "difficulty": "hard",
            "order": 403,
            "expected_sql": """SELECT ROUND(AVG(bin), 1) AS median
FROM (
    SELECT h1.bin
    FROM Histogram h1, Histogram h2
    WHERE h1.bin >= h2.bin
    GROUP BY h1.bin
    HAVING SUM(h2.frequency) >= (SELECT SUM(frequency) FROM Histogram) / 2
       AND SUM(h2.frequency) - h1.frequency <= (SELECT SUM(frequency) FROM Histogram) / 2
) AS temp""",
            "initial_query": """-- This is a challenging problem requiring cumulative sum approach
-- Think about: How to find the middle position(s) in decompressed data
SELECT ROUND(AVG(bin), 1) AS median
FROM (
    -- Write subquery to find median bin(s)
) AS temp""",
            "hints": [
                {
                    "level": 1,
                    "text": "For grouped data, median is estimated by interpolation or finding middle position",
                },
                {
                    "level": 2,
                    "text": "Calculate cumulative frequency to find which bin contains the median",
                },
                {"level": 3, "text": "Use self-join to calculate cumulative sums"},
                {
                    "level": 4,
                    "text": "The median position is at total_count/2",
                },
            ],
            "tags": ["Subquery", "Self Join", "Aggregate Functions", "ROUND", "Hard"],
        },
    ]

    # WS5: Join 相关练习题
    ws5_exercises = [
        {
            "title": "WS5-1: Project Employees I",
            "description": """Write an SQL query that reports the average experience years of all the employees for each project, rounded to 2 digits.

Return the result table in any order.

Project table:

+-------------+-------------+
| project_id  | employee_id |
+-------------+-------------+
| 1           | 1           |
| 1           | 2           |
| 1           | 3           |
| 2           | 1           |
| 2           | 4           |
+-------------+-------------+

Employee table:

+-------------+--------+------------------+
| employee_id | name   | experience_years |
+-------------+--------+------------------+
| 1           | Khaled | 3                |
| 2           | Ali    | 2                |
| 3           | John   | 1                |
| 4           | Doe    | 2                |
+-------------+--------+------------------+

Expected Output:

+-------------+---------------+
| project_id  | average_years |
+-------------+---------------+
| 1           | 2.00          |
| 2           | 2.50          |
+-------------+---------------+""",
            "difficulty": "easy",
            "order": 501,
            "expected_sql": """SELECT p.project_id, 
    ROUND(AVG(e.experience_years), 2) AS average_years
FROM Project p
INNER JOIN Employee e ON p.employee_id = e.employee_id
GROUP BY p.project_id""",
            "initial_query": """SELECT p.project_id, 
    ROUND(AVG(e.experience_years), 2) AS average_years
FROM Project p
-- Add JOIN clause here
GROUP BY p.project_id""",
            "hints": [
                {
                    "level": 1,
                    "text": "First, decide which tables you need to access",
                },
                {
                    "level": 2,
                    "text": "Determine JOIN type (INNER JOIN) and JOIN condition (employee_id)",
                },
                {
                    "level": 3,
                    "text": "Group by project_id to calculate average for each project",
                },
                {
                    "level": 4,
                    "text": "Use ROUND(AVG(...), 2) for 2 decimal places",
                },
            ],
            "tags": ["INNER JOIN", "GROUP BY", "AVG", "ROUND", "Aggregate Functions"],
        },
        {
            "title": "WS5-2: Sales Person Without RED Company Orders",
            "description": """Write an SQL query to report the names of all the salespersons who did not have any orders related to the company with the name "RED".

Return the result table in any order.

SalesPerson table:

+----------+------+--------+-----------------+------------+
| sales_id | name | salary | commission_rate | hire_date  |
+----------+------+--------+-----------------+------------+
| 1        | John | 100000 | 6               | 4/1/2006   |
| 2        | Amy  | 12000  | 5               | 5/1/2010   |
| 3        | Mark | 65000  | 12              | 12/25/2008 |
| 4        | Pam  | 25000  | 25              | 1/1/2005   |
| 5        | Alex | 5000   | 10              | 2/3/2007   |
+----------+------+--------+-----------------+------------+

Company table:

+--------+--------+----------+
| com_id | name   | city     |
+--------+--------+----------+
| 1      | RED    | Boston   |
| 2      | ORANGE | New York |
| 3      | YELLOW | Boston   |
| 4      | GREEN  | Austin   |
+--------+--------+----------+

Orders table:

+----------+------------+--------+----------+--------+
| order_id | order_date | com_id | sales_id | amount |
+----------+------------+--------+----------+--------+
| 1        | 1/1/2014   | 3      | 4        | 10000  |
| 2        | 2/1/2014   | 4      | 5        | 5000   |
| 3        | 3/1/2014   | 1      | 1        | 50000  |
| 4        | 4/1/2014   | 1      | 4        | 25000  |
+----------+------------+--------+----------+--------+

Expected Output:

+------+
| name |
+------+
| Amy  |
| Mark |
| Alex |
+------+""",
            "difficulty": "medium",
            "order": 502,
            "expected_sql": """SELECT s.name
FROM SalesPerson s
WHERE s.sales_id NOT IN (
    SELECT o.sales_id
    FROM Orders o
    LEFT JOIN Company c ON o.com_id = c.com_id
    WHERE c.name = 'RED'
)""",
            "initial_query": """SELECT s.name
FROM SalesPerson s
WHERE s.sales_id NOT IN (
    -- First find salespersons who sold to RED company
    SELECT o.sales_id
    FROM Orders o
    -- Add JOIN with Company table
    WHERE -- Add condition for RED company
)""",
            "hints": [
                {
                    "level": 1,
                    "text": "Decompose the query: first find salespersons who sold to RED",
                },
                {
                    "level": 2,
                    "text": "Join Orders with Company to filter by company name",
                },
                {
                    "level": 3,
                    "text": "Then use NOT IN to exclude those salespersons from all salespersons",
                },
                {
                    "level": 4,
                    "text": "Alternative approach: Use LEFT JOIN and check for NULL",
                },
            ],
            "tags": ["JOIN", "Subquery", "NOT IN", "LEFT JOIN"],
        },
        {
            "title": "WS5-3: Department Employee Count",
            "description": """Write an SQL query to report the respective department name and number of employees working in each department for all departments in the Department table (even ones with no current employees).

Return the result in any order.

Emp table:

+------------+--------------+--------+---------+
| emp_id     | emp_name     | gender | dept_id |
+------------+--------------+--------+---------+
| 1          | Jack         | M      | 1       |
| 2          | Jane         | F      | 1       |
| 3          | Mark         | M      | 2       |
+------------+--------------+--------+---------+

Dept table:

+---------+-------------+
| dept_id | dept_name   |
+---------+-------------+
| 1       | Engineering |
| 2       | Science     |
| 3       | Law         |
+---------+-------------+

Expected Output:

+-------------+----------------+
| dept_name   | emp_number     |
+-------------+----------------+
| Engineering | 2              |
| Science     | 1              |
| Law         | 0              |
+-------------+----------------+""",
            "difficulty": "easy",
            "order": 503,
            "expected_sql": """SELECT d.dept_name, COUNT(e.emp_id) AS emp_number
FROM Dept d
LEFT JOIN Emp e ON d.dept_id = e.dept_id
GROUP BY d.dept_name, d.dept_id""",
            "initial_query": """SELECT d.dept_name, COUNT(e.emp_id) AS emp_number
FROM Dept d
-- What type of JOIN should we use to include departments with 0 employees?
GROUP BY d.dept_name, d.dept_id""",
            "hints": [
                {
                    "level": 1,
                    "text": "We need ALL departments, even those with no employees - what JOIN type?",
                },
                {
                    "level": 2,
                    "text": "Use LEFT JOIN with Dept as the left table",
                },
                {
                    "level": 3,
                    "text": "COUNT(e.emp_id) will count employees, and return 0 for NULL",
                },
                {
                    "level": 4,
                    "text": "Group by department to get count for each department",
                },
            ],
            "tags": ["LEFT JOIN", "GROUP BY", "COUNT", "Aggregate Functions"],
        },
    ]

    # WS6: Self Join 相关练习题
    ws6_exercises = [
        {
            "title": "WS6-1: Consecutive Available Seats",
            "description": """Write an SQL query to report all the consecutive available seats in the cinema.

Return the result table ordered by seat_id in ascending order.

The test cases are generated so that more than two seats are consecutively available.

Cinema table:

+---------+------+
| seat_id | free |
+---------+------+
| 1       | 1    |
| 2       | 0    |
| 3       | 1    |
| 4       | 1    |
| 5       | 1    |
+---------+------+

Note: free = 1 means free, free = 0 means occupied

Expected Output:

+---------+
| seat_id |
+---------+
| 3       |
| 4       |
| 5       |
+---------+""",
            "difficulty": "easy",
            "order": 601,
            "expected_sql": """SELECT DISTINCT a.seat_id
FROM Cinema a, Cinema b
WHERE ABS(a.seat_id - b.seat_id) = 1
  AND a.free = 1 
  AND b.free = 1
ORDER BY a.seat_id""",
            "initial_query": """SELECT DISTINCT a.seat_id
FROM Cinema a, Cinema b
-- How to check two consecutive rows in the same table?
-- Hint: Use self join
WHERE -- Add condition for consecutive seats
  AND a.free = 1 
  AND b.free = 1
ORDER BY a.seat_id""",
            "hints": [
                {
                    "level": 1,
                    "text": "Cannot check consecutive rows in a single table with simple SQL",
                },
                {"level": 2, "text": "Use self join to create a copy of the table"},
                {
                    "level": 3,
                    "text": "Consecutive seats: ABS(a.seat_id - b.seat_id) = 1",
                },
                {"level": 4, "text": "Both seats must be free (free = 1)"},
                {
                    "level": 5,
                    "text": "Alternative: You can use LAG() or LEAD() window functions",
                },
            ],
            "tags": ["Self Join", "DISTINCT", "ORDER BY", "ABS"],
        },
        {
            "title": "WS6-2: Game Play Analysis III",
            "description": """Write an SQL query to report for each player and date, how many games played so far by the player. That is, the total number of games played by the player until that date.

Return the result table in any order.

Activity table:

+-----------+-----------+------------+--------------+
| player_id | device_id | event_date | games_played |
+-----------+-----------+------------+--------------+
| 1         | 2         | 2016-03-01 | 5            |
| 1         | 2         | 2016-05-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-02 | 0            |
| 3         | 4         | 2018-07-03 | 5            |
+-----------+-----------+------------+--------------+

Expected Output:

+-----------+------------+---------------------+
| player_id | event_date | games_played_so_far |
+-----------+------------+---------------------+
| 1         | 2016-03-01 | 5                   |
| 1         | 2016-05-02 | 11                  |
| 2         | 2017-06-25 | 1                   |
| 3         | 2016-03-02 | 0                   |
| 3         | 2018-07-03 | 5                   |
+-----------+------------+---------------------+""",
            "difficulty": "medium",
            "order": 602,
            "expected_sql": """SELECT a1.player_id, 
    a1.event_date,
    SUM(a2.games_played) AS games_played_so_far
FROM Activity a1, Activity a2
WHERE a1.player_id = a2.player_id
  AND a1.event_date >= a2.event_date
GROUP BY a1.player_id, a1.event_date""",
            "initial_query": """SELECT a1.player_id, 
    a1.event_date,
    SUM(a2.games_played) AS games_played_so_far
FROM Activity a1, Activity a2
WHERE a1.player_id = a2.player_id
  AND -- Add condition to accumulate games up to current date
GROUP BY a1.player_id, a1.event_date""",
            "hints": [
                {
                    "level": 1,
                    "text": "How to accumulate games_played? Need self join",
                },
                {
                    "level": 2,
                    "text": "One copy (a1) is for the base, another (a2) for history",
                },
                {
                    "level": 3,
                    "text": "Use a1.event_date >= a2.event_date to get all previous games",
                },
                {
                    "level": 4,
                    "text": "SUM(a2.games_played) gives cumulative total",
                },
                {
                    "level": 5,
                    "text": "Group by player_id and event_date to get running total per date",
                },
            ],
            "tags": ["Self Join", "GROUP BY", "SUM", "Aggregate Functions", "Cumulative"],
        },
        {
            "title": "WS6-3: Total Grade by Gender Until Each Day",
            "description": """Write an SQL query to find the total grade for each gender until each day.

Return the result table ordered by gender and day in ascending order.

Grades table:

+--------------+--------+------------+--------+
| student_name | gender | day        | grade  |
+--------------+--------+------------+--------+
| Aron         | F      | 2020-01-01 | 17     |
| Alice        | F      | 2020-01-07 | 23     |
| Bajrang      | M      | 2020-01-07 | 7      |
| Khali        | M      | 2019-12-25 | 11     |
| Slaman       | M      | 2019-12-30 | 13     |
| Joe          | M      | 2019-12-31 | 3      |
| Jose         | M      | 2019-12-18 | 2      |
| Priya        | F      | 2019-12-31 | 23     |
| Priyanka     | F      | 2019-12-30 | 17     |
+--------------+--------+------------+--------+

Expected Output:

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
            "order": 603,
            "expected_sql": """SELECT g1.gender,
    g1.day,
    SUM(g2.grade) AS total
FROM Grades g1, Grades g2
WHERE g1.gender = g2.gender
  AND g1.day >= g2.day
GROUP BY g1.gender, g1.day
ORDER BY g1.gender, g1.day""",
            "initial_query": """SELECT g1.gender,
    g1.day,
    SUM(g2.grade) AS total
FROM Grades g1, Grades g2
WHERE g1.gender = g2.gender
  AND -- Add condition for cumulative sum
GROUP BY g1.gender, g1.day
ORDER BY g1.gender, g1.day""",
            "hints": [
                {
                    "level": 1,
                    "text": "Similar to cumulative sum problem - use self join",
                },
                {
                    "level": 2,
                    "text": "Match rows with same gender: g1.gender = g2.gender",
                },
                {
                    "level": 3,
                    "text": "Include all grades up to current day: g1.day >= g2.day",
                },
                {
                    "level": 4,
                    "text": "SUM(g2.grade) gives running total",
                },
                {
                    "level": 5,
                    "text": "Group by gender and day, then order by both",
                },
            ],
            "tags": ["Self Join", "GROUP BY", "SUM", "ORDER BY", "Cumulative"],
        },
    ]

    # 合并所有练习题
    all_exercises = ws3_exercises + ws4_exercises + ws5_exercises + ws6_exercises

    # 批量创建/更新练习题
    created_count = 0
    updated_count = 0

    for data in all_exercises:
        exercise, created = Exercise.objects.get_or_create(
            schema=schema,
            title=data["title"],
            defaults=data,
        )

        if created:
            created_count += 1
            print(f"✓ 创建: {data['title']}")
        else:
            # 更新已存在的练习题（保持 title 不变）
            for key, value in data.items():
                if key != "title":
                    setattr(exercise, key, value)
            exercise.save()
            updated_count += 1
            print(f"↻ 更新: {data['title']}")

    print("\n" + "=" * 60)
    print(
        f"✓ 完成! 创建了 {created_count} 个新练习题, 更新了 {updated_count} 个现有练习题"
    )
    print(f"✓ 总计: {len(all_exercises)} 个练习题")
    print("=" * 60)


if __name__ == "__main__":
    add_exercises()


