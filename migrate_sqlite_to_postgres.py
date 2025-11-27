import sqlite3
import psycopg2
import os

# Подключение к SQLite
sqlite_conn = sqlite3.connect('db.sqlite3')  # Укажите путь к вашему файлу SQLite
sqlite_cursor = sqlite_conn.cursor()

# Получение списка таблиц из SQLite
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

# Подключение к PostgreSQL
pg_conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="postgres",
    password="postgres",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Перенос данных для каждой таблицы
for table in tables:
    table_name = table[0]
    
    # Пропускаем системные таблицы SQLite
    if table_name.startswith('sqlite_'):
        continue
    
    print(f"Перенос таблицы: {table_name}")
    
    # Получение структуры таблицы
    sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
    columns = sqlite_cursor.fetchall()
    
    # Создание таблицы в PostgreSQL
    columns_sql = ", ".join([f'"{col[1]}" TEXT' for col in columns])
    pg_cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    pg_cursor.execute(f"CREATE TABLE {table_name} ({columns_sql});")
    
    # Получение данных из SQLite
    sqlite_cursor.execute(f"SELECT * FROM {table_name};")
    rows = sqlite_cursor.fetchall()
    
    # Вставка данных в PostgreSQL
    if rows:
        placeholders = ", ".join(["%s"] * len(columns))
        for row in rows:
            pg_cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders});", row)

# Фиксация изменений
pg_conn.commit()

# Закрытие соединений
sqlite_cursor.close()
sqlite_conn.close()
pg_cursor.close()
pg_conn.close()

print("Перенос данных завершен успешно!")