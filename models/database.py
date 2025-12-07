"""
Database model using PostgreSQL with psycopg2
"""
import hashlib
import secrets
import psycopg2
from typing import Optional, Tuple, List, Dict, Any
from contextlib import contextmanager
import os


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, host: str = "localhost", port: int = 5432, 
                 database: str = "pc_manager", user: str = "postgres", 
                 password: str = "postgres"):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.init_database()
    
    def test_connection(self) -> bool:
        """Test if we can connect to the database"""
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database="postgres",  # Connect to default database first
                user=self.user,
                password=self.password
            )
            conn.close()
            return True
        except psycopg2.Error:
            return False
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            yield conn
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        try:
            # Connect to PostgreSQL server (without specific database) to create database
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database="postgres",  # Connect to default database first
                user=self.user,
                password=self.password
            )
            
            conn.autocommit = True
            cur = conn.cursor()
            
            # Create database if it doesn't exist
            cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (self.database,))
            exists = cur.fetchone()
            if not exists:
                cur.execute(f"CREATE DATABASE {self.database}")
            
            cur.close()
            conn.close()
            
            # Now connect to our database and create tables
            with self.get_connection() as conn:
                cur = conn.cursor()
                
                # Create users table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password_hash VARCHAR(128) NOT NULL,
                        salt VARCHAR(64) NOT NULL,
                        role VARCHAR(20) NOT NULL CHECK (role IN ('teacher', 'admin'))
                    )
                """)
                
                # Create settings table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS settings (
                        id INTEGER PRIMARY KEY CHECK (id = 1),
                        theme VARCHAR(20) NOT NULL DEFAULT 'light'
                    )
                """)
                
                # Create computers table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS computers (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        ip_address VARCHAR(15) NOT NULL,
                        classroom VARCHAR(100) NOT NULL,
                        status VARCHAR(20) DEFAULT 'online',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Insert default settings
                cur.execute("""
                    INSERT INTO settings (id, theme) 
                    VALUES (1, 'light') 
                    ON CONFLICT (id) DO NOTHING
                """)
                
                # Insert default users if they don't exist
                default_users = [
                    ("teacher", "123456", "teacher"),
                    ("admin", "admin123", "admin")
                ]
                
                for username, password, role in default_users:
                    salt = self._generate_salt()
                    password_hash = self._hash_password(password, salt)
                    cur.execute("""
                        INSERT INTO users (username, password_hash, salt, role)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (username) DO NOTHING
                    """, (username, password_hash, salt, role))
                
                # Insert default computers if they don't exist
                cur.execute("""
                    INSERT INTO computers (name, ip_address, classroom)
                    VALUES 
                        ('ПК-01', '192.168.1.101', 'Кабинет 201'),
                        ('ПК-02', '192.168.1.102', 'Кабинет 201'),
                        ('ПК-03', '192.168.1.103', 'Кабинет 201'),
                        ('ПК-11', '192.168.1.111', 'Кабинет 202'),
                        ('ПК-12', '192.168.1.112', 'Кабинет 202')
                    ON CONFLICT DO NOTHING
                """)
                
                conn.commit()
                cur.close()
                
        except psycopg2.Error as e:
            raise Exception(f"Database initialization error: {e}")
    
    def _generate_salt(self) -> str:
        """Generate a random salt for password hashing"""
        return secrets.token_hex(32)
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Hash password with dynamic salt using PBKDF2"""
        pwd_bytes = password.encode('utf-8')
        salt_bytes = salt.encode('utf-8')
        hash_bytes = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt_bytes, 100000)
        return hash_bytes.hex()
    
    def verify_user(self, username: str, password: str) -> Tuple[bool, Optional[str]]:
        """Verify user credentials and return (success, role)"""
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT password_hash, salt, role FROM users 
                    WHERE username = %s
                """, (username,))
                row = cur.fetchone()
                
                if not row:
                    return False, None
                
                stored_hash, salt, role = row
                input_hash = self._hash_password(password, salt)
                
                if input_hash == stored_hash:
                    return True, role
                return False, None
        except psycopg2.Error:
            return False, None
    
    def get_theme(self) -> str:
        """Get current theme from database"""
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT theme FROM settings WHERE id = 1")
                row = cur.fetchone()
                return row[0] if row else "light"
        except psycopg2.Error:
            return "light"
    
    def set_theme(self, theme: str) -> bool:
        """Set theme in database"""
        if theme not in ["light", "dark", "glass"]:
            theme = "light"
        
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("UPDATE settings SET theme = %s WHERE id = 1", (theme,))
                conn.commit()
                return True
        except psycopg2.Error:
            return False
    
    def get_all_computers(self) -> Dict[str, List[Dict[str, str]]]:
        """Get all computers grouped by classroom"""
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT classroom, name, ip_address, status 
                    FROM computers 
                    ORDER BY classroom, name
                """)
                rows = cur.fetchall()
                
                computers = {}
                for classroom, name, ip, status in rows:
                    if classroom not in computers:
                        computers[classroom] = []
                    computers[classroom].append({
                        "name": name,
                        "ip": ip,
                        "status": status
                    })
                
                return computers
        except psycopg2.Error:
            return {}
    
    def add_computer(self, name: str, ip_address: str, classroom: str) -> bool:
        """Add a new computer to the database"""
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO computers (name, ip_address, classroom)
                    VALUES (%s, %s, %s)
                """, (name, ip_address, classroom))
                conn.commit()
                return True
        except psycopg2.Error:
            return False
    
    def update_computer_status(self, name: str, status: str) -> bool:
        """Update computer status"""
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE computers 
                    SET status = %s 
                    WHERE name = %s
                """, (status, name))
                conn.commit()
                return cur.rowcount > 0
        except psycopg2.Error:
            return False