import psycopg2
import csv

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="PhoneBook",
    user="postgres",
    password="12345&bgm",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Процедура: вставка нового пользователя или обновление существующего
drop_delete_user_by_name_or_phone_p = """
    CREATE OR REPLACE PROCEDURE delete_user_by_name_or_phone(pattern VARCHAR)
    LANGUAGE plpgsql
    AS $$
    BEGIN
      DELETE FROM phonebook WHERE name ILIKE '%' || pattern || '%'
        OR phone ILIKE '%' || pattern || '%';
    END;
    $$;
    """
    
def drop_delete_user_by_name_or_phone(pattern):
  cur.execute("CALL delete_user_by_name_or_phone(%s)", (pattern,))
  conn.commit()
  print(f"Пользователь '{pattern}' удалён.")
  
# Создание таблицы
def create_table():
  cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100),
      phone VARCHAR(20)
    )
  """)
  conn.commit()

# Загрузка из CSV
def insert_from_csv(file_path):
  with open(file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      if len(row) != 2:
        continue
      cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
  conn.commit()
  print("Данные из CSV добавлены.")

# Меню
def menu():
  create_table()
  while True:
    print("\nМеню:")
    print("1 - Загрузить из CSV")
    print("2 - Удалить по имени или номеру")
    print("0 - Выход")
    choice = input("Выберите действие: ")

    if choice == "1":
      path = input("Введите путь к CSV файлу: ")
      insert_from_csv(path)
    elif choice == "2":
        cur.execute("DROP PROCEDURE IF EXISTS delete_user_by_name_or_phone(VARCHAR);")
        cur.execute(drop_delete_user_by_name_or_phone_p)
        conn.commit()
        pattern = input("Введите имя или номер для удаления: ")
        drop_delete_user_by_name_or_phone(pattern)
    elif choice == "0":
      break
    else:
      print("Неверный выбор!")

  cur.close()
  conn.close()

if __name__ == "__main__":
  menu()