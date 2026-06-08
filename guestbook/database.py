import sqlite3
from datetime import date

DATABASE = 'guestbook.db'

def get_db_connection():
    """
    Устанавливает соединение с базой данных SQLite
    Возвращает объект соединения с row_factory = sqlite3.Row
    Это позволяет обращаться к полям по имени (row['name'] или row.name)
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Доступ к колонкам по имени
    return conn

def init_db():
    """
    Инициализирует базу данных:
    1. Создаёт таблицу messages, если она не существует
    2. Добавляет тестовые сообщения (только для разработки)
    """
    conn = get_db_connection()
    
    # SQL запрос для создания таблицы
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at DATE NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # Добавляем тестовые данные (временно, для проверки работы)
    add_test_messages()

def add_test_messages():
    """
    Добавляет тестовые сообщения в базу данных
    Функция временная, используется только для отладки
    """
    conn = get_db_connection()
    
    # Проверяем, есть ли уже сообщения в таблице
    cursor = conn.execute('SELECT COUNT(*) FROM messages')
    count = cursor.fetchone()[0]
    
    # Добавляем тестовые данные только если таблица пуста
    if count == 0:
        today = date.today().isoformat()  # Получаем текущую дату в формате ГГГГ-ММ-ДД
        
        # Список тестовых сообщений
        test_messages = [
            ('Анна Петрова', 'Отличный сайт! Всё очень удобно и понятно.', today),
            ('Иван Сидоров', 'Спасибо за возможность оставить отзыв!', today),
            ('Мария Иванова', 'Жду с нетерпением новых функций.', today),
            ('Дмитрий Козлов', 'Классный проект! Так держать!', today)
        ]
        
        # Добавляем каждое сообщение
        for name, message, created_at in test_messages:
            conn.execute(
                'INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)',
                (name, message, created_at)
            )
        
        conn.commit()
        print(f"[✓] Добавлено {len(test_messages)} тестовых сообщений")
    
    conn.close()

def get_all_messages():
    """
    Получает все сообщения из базы данных
    Возвращает список сообщений, отсортированных по дате (от новых к старым)
    """
    conn = get_db_connection()
    
    # SELECT * - выбираем все поля
    # ORDER BY created_at DESC - сортируем по дате (сначала новые)
    messages = conn.execute('''
        SELECT * FROM messages 
        ORDER BY created_at DESC, id DESC
    ''').fetchall()
    
    conn.close()
    return messages

def get_message_by_id(message_id):
    """
    Получает одно сообщение по его ID
    Используется для просмотра деталей сообщения
    """
    conn = get_db_connection()
    message = conn.execute(
        'SELECT * FROM messages WHERE id = ?',
        (message_id,)
    ).fetchone()
    conn.close()
    return message

def delete_message(message_id):
    """
    Удаляет сообщение по ID
    (будет использоваться в следующей части работы)
    """
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()