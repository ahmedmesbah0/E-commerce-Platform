"""
Database Connection Manager
Handles MySQL database connections with connection pooling
"""

import mysql.connector
from mysql.connector import pooling, Error
from contextlib import contextmanager
from typing import Optional, Dict, List, Tuple, Any
import logging
from backend.config import Config

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Singleton database connection manager with connection pooling"""
    
    _instance = None
    _pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._pool is None:
            self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize connection pool"""
        try:
            self._pool = pooling.MySQLConnectionPool(
                pool_name="ecommerce_pool",
                pool_size=10,
                pool_reset_session=True,
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                autocommit=False
            )
            logger.info("Database connection pool initialized successfully")
        except Error as e:
            logger.error(f"Error initializing database pool: {e}")
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        try:
            return self._pool.get_connection()
        except Error as e:
            logger.error(f"Error getting connection from pool: {e}")
            raise
    
    @contextmanager
    def get_db_connection(self):
        """Context manager for database connections"""
        connection = None
        try:
            connection = self.get_connection()
            yield connection
        except Error as e:
            if connection:
                connection.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    @contextmanager
    def get_db_cursor(self, dictionary=True):
        """Context manager for database cursor with automatic commit/rollback"""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=dictionary)
            yield cursor
            connection.commit()
        except Error as e:
            if connection:
                connection.rollback()
            logger.error(f"Database cursor error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
    
    def execute_query(self, query: str, params: Optional[Tuple] = None, 
                     fetch_one: bool = False, fetch_all: bool = True) -> Optional[Any]:
        """
        Execute a SELECT query and return results
        
        Args:
            query: SQL query string
            params: Query parameters tuple
            fetch_one: Return single result
            fetch_all: Return all results (default)
            
        Returns:
            Query results or None
        """
        try:
            with self.get_db_cursor() as cursor:
                cursor.execute(query, params or ())
                
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                return None
        except Error as e:
            logger.error(f"Error executing query: {e}")
            logger.error(f"Query: {query}")
            raise
    
    def execute_update(self, query: str, params: Optional[Tuple] = None) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query
        
        Args:
            query: SQL query string
            params: Query parameters tuple
            
        Returns:
            Number of affected rows or last insert ID for INSERT
        """
        try:
            with self.get_db_cursor() as cursor:
                cursor.execute(query, params or ())
                
                # For INSERT queries, return last insert ID
                if query.strip().upper().startswith('INSERT'):
                    return cursor.lastrowid
                # For UPDATE/DELETE, return affected rows
                return cursor.rowcount
        except Error as e:
            logger.error(f"Error executing update: {e}")
            logger.error(f"Query: {query}")
            raise
    
    def execute_many(self, query: str, params_list: List[Tuple]) -> int:
        """
        Execute multiple queries with different parameters
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
            
        Returns:
            Number of affected rows
        """
        try:
            with self.get_db_cursor() as cursor:
                cursor.executemany(query, params_list)
                return cursor.rowcount
        except Error as e:
            logger.error(f"Error executing batch update: {e}")
            raise
    
    def call_procedure(self, proc_name: str, args: Optional[Tuple] = None) -> List[Dict]:
        """
        Call a stored procedure
        
        Args:
            proc_name: Stored procedure name
            args: Procedure arguments tuple
            
        Returns:
            Procedure results
        """
        try:
            with self.get_db_cursor() as cursor:
                cursor.callproc(proc_name, args or ())
                
                # Fetch all result sets
                results = []
                for result in cursor.stored_results():
                    results.extend(result.fetchall())
                
                return results
        except Error as e:
            logger.error(f"Error calling procedure {proc_name}: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.get_db_cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result is not None
        except Error as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def close_pool(self):
        """Close all connections in the pool"""
        if self._pool:
            logger.info("Closing database connection pool")
            # Connection pools in mysql-connector-python don't have explicit close
            self._pool = None


# Global database instance
db = DatabaseManager()
