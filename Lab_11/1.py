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

# Функция: поиск по шаблону
create_func_search_by_pattern = """
    CREATE OR REPLACE FUNCTION search_by_pattern(pattern TEXT)
    RETURNS TABLE(id INT, name character varying(100), phone character varying(100)) AS $$
    BEGIN
      RETURN QUERY
      SELECT p.id, p.name, p.phone
      FROM phonebook p
      WHERE p.name ILIKE '%' || pattern || '%'
      OR p.phone ILIKE '%' || pattern || '%';
    END;
    $$ LANGUAGE plpgsql;
    """

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
  with open(file_path, newline='', encoding='utf-8') as csvfile:
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
    print("2 - Поиск по шаблону")
    print("0 - Выход")
    choice = input("Выберите действие: ")

    if choice == "1":
      path = input("Введите путь к CSV файлу: ")
      insert_from_csv(path)
    elif choice == "2":
        cur.execute("DROP FUNCTION IF EXISTS search_by_pattern(TEXT);")
        cur.execute(create_func_search_by_pattern)
        conn.commit()
        pattern = input("Введите шаблон для поиска: ")
        cur.execute("SELECT * FROM search_by_pattern(%s)", (pattern,))
        results = cur.fetchall()
        for row in results:
            print(row)
    elif choice == "0":
      break
    else:
      print("Неверный выбор!")

  cur.close()
  conn.close()

if __name__ == "__main__":
  menu()