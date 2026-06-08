import sqlite3
from datetime import date

def get_db_connection():
    """Устанавливает соединение с базой данных."""
    conn = sqlite3.connect('guestbook.db')
    conn.row_factory = sqlite3.Row  # Доступ к колонкам по имени
    return conn

def init_db():
    """Инициализирует базу данных: создаёт таблицу, если её нет."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all_messages():
    """Возвращает все сообщения, отсортированные от новых к старым."""
    conn = get_db_connection()
    messages = conn.execute(
        'SELECT * FROM messages ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    return messages

def add_message(name, message):
    """
    Добавляет новое сообщение в базу данных.
    Дата создания проставляется автоматически (текущая дата).
    """
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)',
        (name, message, date.today().strftime('%Y-%m-%d'))
    )
    conn.commit()
    conn.close()