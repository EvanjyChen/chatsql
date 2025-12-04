import pymysql
import time
from typing import Dict, List, Tuple
from django.conf import settings

class SQLExecutor:
    """Secure SQL query executor for practice databases"""
    
    DANGEROUS_KEYWORDS = [
        'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 
        'CREATE', 'TRUNCATE', 'GRANT', 'REVOKE', 'EXEC'
    ]
    
    MAX_EXECUTION_TIME = 5  # seconds
    MAX_ROWS = 1000
    
    def __init__(self, db_name: str):
        """
        Initialize executor for specific practice database
        Args:
            db_name: 'practice_hr', 'practice_ecommerce', or 'practice_school'
        """
        if db_name not in settings.DATABASES:
            raise ValueError(f"Invalid database: {db_name}")
        
        self.db_config = settings.DATABASES[db_name]
        self.db_name = db_name
    
    def validate_query(self, query: str) -> Tuple[bool, str]:
        """
        Validate SQL query for security
        Returns: (is_valid, error_message)
        """
        query_upper = query.strip().upper()
        
        # Must start with SELECT
        if not query_upper.startswith('SELECT'):
            return False, "Only SELECT queries are allowed"
        
        # Check for dangerous keywords
        for keyword in self.DANGEROUS_KEYWORDS:
            if keyword in query_upper:
                return False, f"Keyword '{keyword}' is not allowed"
        
        # Check for comment-based injection
        if '--' in query or '/*' in query or '*/' in query:
            return False, "Comments are not allowed in queries"
        
        # Check for semicolon (multiple statements)
        if query.count(';') > 1:
            return False, "Multiple statements are not allowed"
        
        return True, ""
    
    def execute(self, query: str) -> Dict:
        """
        Execute SQL query and return results
        Returns: {
            'success': bool,
            'columns': List[str],
            'rows': List[List],
            'row_count': int,
            'execution_time': float,
            'error': str (if failed)
        }
        """
        # Validate query
        is_valid, error = self.validate_query(query)
        if not is_valid:
            return {
                'success': False,
                'error': error,
                'columns': [],
                'rows': [],
                'row_count': 0,
                'execution_time': 0
            }
        
        connection = None
        start_time = time.time()
        
        # Validate database configuration before connecting
        host = self.db_config.get('HOST')
        user = self.db_config.get('USER')
        password = self.db_config.get('PASSWORD')
        database = self.db_config.get('NAME')
        
        if not host:
            return {
                'success': False,
                'error': f'Database configuration error: HOST is not set for database "{self.db_name}". Please check your .env file and ensure WS_DB_HOST is configured.',
                'columns': [],
                'rows': [],
                'row_count': 0,
                'execution_time': round(time.time() - start_time, 3)
            }
        
        if not user:
            return {
                'success': False,
                'error': f'Database configuration error: USER is not set for database "{self.db_name}". Please check your .env file and ensure WS_DB_USER is configured.',
                'columns': [],
                'rows': [],
                'row_count': 0,
                'execution_time': round(time.time() - start_time, 3)
            }
        
        if password is None:
            return {
                'success': False,
                'error': f'Database configuration error: PASSWORD is not set for database "{self.db_name}". Please check your .env file and ensure WS_DB_PASSWORD is configured.',
                'columns': [],
                'rows': [],
                'row_count': 0,
                'execution_time': round(time.time() - start_time, 3)
            }
        
        try:
            # Connect to database
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=int(self.db_config.get('PORT', 3306)),
                connect_timeout=5,
                read_timeout=self.MAX_EXECUTION_TIME,
                cursorclass=pymysql.cursors.DictCursor
            )
            
            with connection.cursor() as cursor:
                # Execute query with timeout
                cursor.execute(query)
                
                # Fetch results (limited)
                rows = cursor.fetchmany(self.MAX_ROWS)
                
                # Get column names
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                
                # Convert to list of lists for JSON serialization
                row_list = [list(row.values()) for row in rows]
                
                execution_time = time.time() - start_time
                
                return {
                    'success': True,
                    'columns': columns,
                    'rows': row_list,
                    'row_count': len(row_list),
                    'execution_time': round(execution_time, 3),
                    'error': None
                }
        
        except pymysql.MySQLError as e:
            error_code, error_msg = e.args[0], str(e)
            
            # Handle "Unknown database" error with helpful message
            if error_code == 1049:  # Unknown database
                # Try to suggest alternative databases
                suggestion = ""
                if 'practice_hr' in database or 'practice_ecommerce' in database or 'practice_school' in database:
                    suggestion = f"\n提示: 数据库 '{database}' 不存在。如果这是练习数据库，请检查 GCP 上是否已创建该数据库，或者联系管理员。"
                    # Check if WS1 exists as alternative
                    try:
                        test_conn = pymysql.connect(
                            host=host,
                            user=user,
                            password=password,
                            database='WS1',
                            port=int(self.db_config.get('PORT', 3306)),
                            connect_timeout=2
                        )
                        test_conn.close()
                        suggestion += "\n可用的替代数据库: WS1, WS2, WS3, WS4, WS5, WS6, WS7, WS8, WS9, WS10, WS11"
                    except:
                        pass
                
                return {
                    'success': False,
                    'error': f"数据库 '{database}' 不存在。{error_msg}{suggestion}",
                    'columns': [],
                    'rows': [],
                    'row_count': 0,
                    'execution_time': round(time.time() - start_time, 3)
                }
            
            return {
                'success': False,
                'error': str(e),
                'columns': [],
                'rows': [],
                'row_count': 0,
                'execution_time': round(time.time() - start_time, 3)
            }
        
        finally:
            if connection:
                connection.close()
    
    def compare_results(self, user_result: Dict, expected_result: Dict) -> Dict:
        """
        Compare user query result with expected result
        Returns: {
            'correct': bool,
            'message': str,
            'diff': Dict (if incorrect)
        }
        """
        if not user_result['success']:
            return {
                'correct': False,
                'message': 'Query execution failed',
                'diff': None
            }
        
        # Check if expected query executed successfully
        if not expected_result['success']:
            return {
                'correct': False,
                'message': f'Expected query execution failed: {expected_result.get("error", "Unknown error")}. Please check the expected SQL configuration.',
                'diff': None
            }
        
        # Compare column names (order doesn't matter, case-insensitive)
        user_cols = set(col.lower() for col in user_result['columns'])
        expected_cols = set(col.lower() for col in expected_result['columns'])
        
        if user_cols != expected_cols:
            # Get original column names for display
            user_cols_orig = set(user_result['columns'])
            expected_cols_orig = set(expected_result['columns'])
            return {
                'correct': False,
                'message': 'Column names do not match',
                'diff': {
                    'missing_columns': list(expected_cols_orig - user_cols_orig),
                    'extra_columns': list(user_cols_orig - expected_cols_orig),
                    'user_columns': list(user_result['columns']),
                    'expected_columns': list(expected_result['columns'])
                }
            }
        
        # Compare row count
        if user_result['row_count'] != expected_result['row_count']:
            return {
                'correct': False,
                'message': f"Row count mismatch: expected {expected_result['row_count']}, got {user_result['row_count']}",
                'diff': None
            }
        
        # Compare actual data (normalize for comparison)
        user_data_normalized = self._normalize_result(user_result)
        expected_data_normalized = self._normalize_result(expected_result)
        
        if user_data_normalized != expected_data_normalized:
            return {
                'correct': False,
                'message': 'Query results do not match expected output',
                'diff': None
            }
        
        return {
            'correct': True,
            'message': 'Correct! Well done!',
            'diff': None
        }
    
    def _normalize_result(self, result: Dict) -> set:
        """Normalize result for comparison (handle row order)"""
        rows = []
        for row in result['rows']:
            # Convert each row to tuple (hashable) and sort
            row_tuple = tuple(sorted(str(val) for val in row))
            rows.append(row_tuple)
        return set(rows)
