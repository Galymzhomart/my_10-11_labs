import pygame, sys
from worm import Snake  # Импортируем класс змеи

from database import save_progress

pygame.init()

def level1(score, user_id, level):
    window = pygame.display.set_mode((850, 600))  # Окно игры

    clock = pygame.time.Clock()  
    fps = 5  # Более плавная игра

    font = pygame.font.Font(None, 36)  
    text = font.render("level1", True, (255, 255, 255))  

    apple = (4, 18)  # Стартовая позиция яблока

    walls = [(10, 10), (10, 11)]  # Стены

    snake = Snake([(6, 4), (5, 4)], walls)  # Создаём змею

    fruit = 1  # Тип фрукта
    direct = 0  # Направление
    fail = False  # Флаг поражения
    score = 0


    # Главный игровой цикл
    while len(snake.pos) < 6 and not fail:  
        for e in pygame.event.get():
            if e.type == pygame.QUIT:  
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:  
                if e.key == pygame.K_UP and direct != 1:
                    direct = 3
                elif e.key == pygame.K_DOWN and direct != 3:
                    direct = 1
                elif e.key == pygame.K_LEFT and direct != 0:
                    direct = 2
                elif e.key == pygame.K_RIGHT and direct != 2:
                    direct = 0
                elif e.key == pygame.K_p:  # Нажатие на "P" - пауза и сохранение
                    print("Игра на паузе. Сохраняем прогресс...")
                    save_progress(user_id, level, score)
                    pygame.time.delay(500)  # Небольшая задержка

        # Проверяем, съела ли змея яблоко
        apple, score, fruit = snake.eat(apple, score, fruit)

        # Цвет яблока
        color = (255, 0, 0) if fruit == 1 else (255, 255, 0) if fruit == 2 else (0, 0, 255)

        score_text = font.render("score: " + str(score), True, (255, 255, 255))  

        # Двигаем змею, проверяем столкновения
        fail = snake.move(direct)

        if fail:  
            game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
            window.blit(game_over_text, (300, 250))
            pygame.display.flip()
            pygame.time.delay(2000)  # Показываем сообщение 2 секунды
            # Сохраняем данные при поражении
            save_progress(user_id, level, score)


            return score  # Возвращаем очки

        # Отрисовка
        window.fill((0, 0, 0))
        pygame.draw.rect(window, color, (25 * apple[0], 25 * apple[1], 25, 25))  
        for i in walls:  
            pygame.draw.rect(window, (122, 122, 122), (25 * i[0], 25 * i[1], 25, 25))
        snake.draw(window)  
        window.blit(text, (750, 15))  
        window.blit(score_text, (15, 15))  
        pygame.display.flip()  
        clock.tick(fps)  

    return score  
