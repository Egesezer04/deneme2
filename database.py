import sqlite3
import logging
from typing import Dict
from models import BaseModel

class Database(BaseModel):
    def __init__(self, sqlite_db: str = "listings.db"):
        super().__init__()
        self.sqlite_db = sqlite_db
        self._connect_db()

    def _connect_db(self):
        try:
            self.conn = sqlite3.connect(self.sqlite_db, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self._create_table()
        except sqlite3.Error as e:
            logging.error(f"DB CONNECTION ERROR: {e}")
            self.conn = None
            self.cursor = None

    def _create_table(self):
        if not self.cursor:
            return
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price REAL,
                description TEXT,
                images TEXT,
                score REAL,
                missing TEXT
            )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"DB TABLE ERROR: {e}")

    def add(self, data: Dict):
        if not self.conn:
            logging.error("DB not connected, cannot insert data.")
            return
        try:
            self.cursor.execute("""
            INSERT INTO listings (title, price, description, images, score, missing)
            VALUES (:title, :price, :description, :images, :score, :missing)
            """, data)
            self.conn.commit()
            logging.info(f"Listing saved: {data['title']}")
        except sqlite3.Error as e:
            logging.error(f"DB INSERT ERROR: {e}, Data: {data}")
