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
insert_or_update_user_p = """
    CREATE OR REPLACE PROCEDURE insert_or_update_user(fname VARCHAR, fphone VARCHAR)
    LANGUAGE plpgsql
    AS $$
    BEGIN
      IF EXISTS (
        SELECT 1 FROM phonebook WHERE name = fname
      ) THEN
        UPDATE phonebook SET phone = fphone WHERE name = fname;
      ELSE
        INSERT INTO phonebook (name, phone) VALUES (fname, fphone);
      END IF;
    END;
    $$;
    """
    
def insert_or_update_user(fname, fphone):
  cur.execute("CALL insert_or_update_user(%s, %s)", (fname, fphone))
  conn.commit()
  print(f"Пользователь '{fname}' добавлен или обновлён.")
  
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
    print("2 - Вставка/обновление пользователя")
    print("0 - Выход")
    choice = input("Выберите действие: ")

    if choice == "1":
      path = input("Введите путь к CSV файлу: ")
      insert_from_csv(path)
    elif choice == "2":
        cur.execute("DROP PROCEDURE IF EXISTS insert_or_update_user(VARCHAR, VARCHAR);")
        cur.execute(insert_or_update_user_p)
        conn.commit()
        fname = input("Введите имя: ")
        phone = input("Введите номер телефона: ")
        insert_or_update_user(fname, phone)
    elif choice == "0":
      break
    else:
      print("Неверный выбор!")

  cur.close()
  conn.close()

if __name__ == "__main__":
  menu()