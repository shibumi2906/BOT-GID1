import psycopg2
from psycopg2.extras import RealDictCursor
import config

def get_db_connection():
    """
    Создает подключение к базе данных.
    """
    conn = psycopg2.connect(config.DATABASE_URL)
    return conn

def get_user_preferences(user_id):
    """
    Получает предпочтения пользователя по его ID.
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT preferences FROM Users WHERE user_id = %s", (user_id,))
            return cur.fetchone()

def get_events_by_category(category_id):
    """
    Возвращает события по ID категории.
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM Events WHERE category_id = %s", (category_id,))
            return cur.fetchall()

def add_user(username, preferences):
    """
    Добавляет нового пользователя в таблицу Users.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO Users (username, preferences) VALUES (%s, %s) RETURNING user_id",
                        (username, Json(preferences)))
            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id

def update_event(event_id, title, description):
    """
    Обновляет информацию о событии.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE Events SET title = %s, description = %s WHERE event_id = %s",
                        (title, description, event_id))
            conn.commit()

def delete_notification(notification_id):
    """
    Удаляет уведомление по его ID.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Notifications WHERE notification_id = %s", (notification_id,))
            conn.commit()

# Дополнительные функции могут быть добавлены для работы с таблицами CategoryPreferences и другими.
