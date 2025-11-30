# auth_db.py
import os
import hashlib
import sqlite3


class AuthDatabase:
    DB_PATH = "auth.sqlite"

    def __init__(self):
        self.init_database()

    def init_database(self):
        if not os.path.exists(self.DB_PATH):
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            # Таблица пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('teacher', 'admin'))
                )
            """)
            # Таблица настроек
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    theme TEXT NOT NULL DEFAULT 'light'
                )
            """)
            # Вставляем настройки по умолчанию
            cursor.execute("INSERT OR IGNORE INTO settings (id, theme) VALUES (1, 'light')")
            # Учётные записи по умолчанию
            default_users = [
                ("teacher", "123456", "teacher"),
                ("admin", "admin123", "admin")
            ]
            for user, pwd, role in default_users:
                pwd_hash = self._hash_password(pwd)
                try:
                    cursor.execute(
                        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (user, pwd_hash, role)
                    )
                except sqlite3.IntegrityError:
                    pass
            conn.commit()
            conn.close()

    def _hash_password(self, password: str, salt: bytes = b'static_salt_2025') -> str:
        pwd_bytes = password.encode('utf-8')
        hash_bytes = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt, 100000)
        return hash_bytes.hex()

    def verify_password(self, username: str, password: str) -> tuple[bool, str | None]:
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return False, None
        stored_hash, role = row
        input_hash = self._hash_password(password)
        if input_hash == stored_hash:
            return True, role
        return False, None

    def get_theme(self) -> str:
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT theme FROM settings WHERE id = 1")
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else "light"

    def set_theme(self, theme: str):
        if theme not in ["light", "dark", "glass"]:
            theme = "light"
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET theme = ? WHERE id = 1", (theme,))
        conn.commit()
        conn.close()