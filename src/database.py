import sqlite3
from datetime import datetime

class ProxyDatabase:
    def __init__(self, db_path='proxies.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS proxies (
                    id INTEGER PRIMARY KEY,
                    ip TEXT NOT NULL,
                    port INTEGER NOT NULL,
                    protocol TEXT DEFAULT 'http',
                    country TEXT,
                    speed REAL,
                    last_checked TEXT,
                    is_valid BOOLEAN DEFAULT 1,
                    UNIQUE(ip, port)
                )
            ''')

    def insert_proxy(self, ip, port, protocol='http', country=None, speed=None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO proxies (ip, port, protocol, country, speed, last_checked, is_valid)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            ''', (ip, port, protocol, country, speed, datetime.now().isoformat()))

    def get_valid_proxies(self, limit=100):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT ip, port, protocol FROM proxies
                WHERE is_valid = 1
                ORDER BY last_checked DESC
                LIMIT ?
            ''', (limit,))
            return [{'ip': row[0], 'port': row[1], 'protocol': row[2]} for row in cursor.fetchall()]

    def update_proxy_status(self, ip, port, is_valid, speed=None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE proxies SET is_valid = ?, speed = ?, last_checked = ?
                WHERE ip = ? AND port = ?
            ''', (is_valid, speed, datetime.now().isoformat(), ip, port))