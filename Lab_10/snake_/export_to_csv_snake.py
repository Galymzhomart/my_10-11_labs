import psycopg2
import csv

def get_connection():
    return psycopg2.connect(
        dbname="snakeusers",
        user="postgres",
        password="12345&bgm",
        host="localhost",
        port="5432"
    )

def export_phonebook_to_csv(filename="Lab_10/snake_/snake_export.csv"):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    
    # Получаем названия столбцов
    column_names = [desc[0] for desc in cursor.description]

    # Запись в CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)  # Заголовки
        writer.writerows(rows)         # Данные

    cursor.close()
    conn.close()
    print(f"Данные из phonebook сохранены в файл: {filename}")

# Автоматический запуск при запуске скрипта
if __name__ == "__main__":
    export_phonebook_to_csv()