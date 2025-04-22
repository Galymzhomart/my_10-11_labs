import pygame
from database import create_tables, get_user, get_user_progress, save_progress
from level1 import level1
from level2 import level2
from level3 import level3

# Создаём таблицы
create_tables()

# Считываем имя пользователя
username = input("Введите имя пользователя: ")
user_id = get_user(username)
level, score = get_user_progress(user_id)
print(f"Добро пожаловать, {username}! Ваш текущий уровень: {level}, счёт: {score}")

levels = [level1, level2, level3]

# Начинаем с уровня пользователя
while level <= len(levels):
    print(f"Запуск уровня {level}...")
    score = levels[level - 1](score, user_id, level)
    save_progress(user_id, level, score)  # Сохраняем до увеличения уровня
    level += 1

print("Все уровни пройдены!")