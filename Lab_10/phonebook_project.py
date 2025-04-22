import psycopg2

# Подключение к базе данных PhoneBook
def get_connection():
    return psycopg2.connect(
        dbname="PhoneBook",
        user="postgres",
        password="12345&bgm",
        host="localhost",
        port="5432"
    )

# Создание таблицы (если её нет)
def create_table(conn, cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()

# Вставка данных вручную через консоль
def insert_from_console(conn, cur):
    name = input("Введите имя: ")
    phone = input("Введите номер телефона: ")
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("Запись добавлена.")

# Главная функция
def main():
    conn = get_connection()
    cur = conn.cursor()

    create_table(conn, cur)
    insert_from_console(conn, cur)

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
