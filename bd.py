import psycopg2
from psycopg2.extras import RealDictCursor
import config

def get_db_connection():
    """
    Создает и возвращает подключение к базе данных.
    Использует параметры из файла конфигурации.
    """
    conn = psycopg2.connect(config.DATABASE_URL)
    return conn

def check_and_create_tables():
    """
    Проверяет наличие необходимых таблиц и создает их, если они отсутствуют.
    Структура таблиц включает пользователей, события, категории, уведомления и предпочтения по категориям.
    """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS Users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            preferences JSONB
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Events (
            event_id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            date_time TIMESTAMP,
            location VARCHAR(255),
            price DECIMAL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Categories (
            category_id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Notifications (
            notification_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            time TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (event_id) REFERENCES Events(event_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS CategoryPreferences (
            user_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            preference_level INTEGER,
            PRIMARY KEY (user_id, category_id),
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        );
        """
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    for command in commands:
        cursor.execute(command)
    conn.commit()
    cursor.close()
    conn.close()

def init_db():
    """
    Инициализирует базу данных, вызывая функцию проверки и создания таблиц.
    Эта функция вызывается при старте приложения для гарантии наличия всех необходимых таблиц.
    """
    check_and_create_tables()

# Примеры функций для взаимодействия с базой данных

def add_user(username, preferences):
    """
    Добавляет нового пользователя в базу данных.
    Принимает имя пользователя и его предпочтения в формате JSON.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO Users (username, preferences) VALUES (%s, %s) RETURNING user_id",
                        (username, preferences))
            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id

def get_user_preferences(user_id):
    """
    Возвращает предпочтения пользователя по его ID.
    Используется для персонализации ответов и предложений бота.
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT preferences FROM Users WHERE user_id = %s", (user_id,))
            return cur.fetchone()

