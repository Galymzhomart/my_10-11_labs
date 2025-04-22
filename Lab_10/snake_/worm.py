import pygame
import random

class Snake:
    def __init__(self, pos, walls):
        self.pos = pos
        self.possible_possition = [(i, j) for i in range(34) for j in range(24)]
        self.possible_possition.append((-1, -1))
        self.time = 0
        
        for i in pos:
            self.possible_possition.remove(i)
        for i in walls:
            self.possible_possition.remove(i)

        # Загружаем изображения
        self.head_img = pygame.image.load('Lab_10/snake_/img/head.png')
        self.body_img = pygame.image.load('Lab_10/snake_/img/body.png')
        self.tail_img = pygame.image.load('Lab_10/snake_/img/tail.png')
        self.turn_img = pygame.image.load('Lab_10/snake_/img/turn.png')  # Новый изгиб тела

    def move(self, direct):
        if direct == 0:
            self.pos.insert(0, (self.pos[0][0]+1, self.pos[0][1]))  # Вправо
        elif direct == 1:
            self.pos.insert(0, (self.pos[0][0], self.pos[0][1]+1))  # Вниз
        elif direct == 2:
            self.pos.insert(0, (self.pos[0][0]-1, self.pos[0][1]))  # Влево
        else:
            self.pos.insert(0, (self.pos[0][0], self.pos[0][1]-1))  # Вверх

        try:
            self.possible_possition.remove(self.pos[0])
        except:
            return True
        self.possible_possition.append(self.pos[-1])
        self.pos.pop()

    def eat(self, a, s, t):
        # Function to handle eating an apple
        self.time += 1  # Increment time counter
        if self.pos[0][0] == a[0] and self.pos[0][1] == a[1] or self.time > 30:  # If the snake eats the apple or time exceeds 30 moves
            self.possible_possition.remove((-1, -1))  # Remove the special position from possible positions
            a = random.choice(self.possible_possition)  # Choose a new random position for the apple
            if self.time > 30:  # If time exceeds 30 moves
                self.possible_possition.append((-1, -1))  # Add the special position back to possible positions
            else:
                self.pos.append((-1, -1))  # Add a new segment to the snake
                s += t  # Increase score
            self.time = 0  # Reset time counter
            t = random.randint(1, 3)  # Generate a new random fruit type
        return a, s, t  # Return the new apple position, score, and fruit type

    def draw(self, window):
        for i in range(len(self.pos)):
            x, y = self.pos[i][0] * 25, self.pos[i][1] * 25

            if i == 0:  
                # Определяем направление головы
                if self.pos[0][0] > self.pos[1][0]:  
                    head = pygame.transform.rotate(self.head_img, 270)  # Вправо
                elif self.pos[0][0] < self.pos[1][0]:  
                    head = pygame.transform.rotate(self.head_img, 90)  # Влево
                elif self.pos[0][1] > self.pos[1][1]:  
                    head = pygame.transform.rotate(self.head_img, 180)  # Вниз
                else:
                    head = self.head_img  # Вверх

                window.blit(head, (x, y))

            elif i == len(self.pos) - 1:
                # Определяем направление хвоста
                if self.pos[-1][0] > self.pos[-2][0]:  
                    tail = pygame.transform.rotate(self.tail_img, 270)  # Вправо
                elif self.pos[-1][0] < self.pos[-2][0]:  
                    tail = pygame.transform.rotate(self.tail_img, 90)  # Влево
                elif self.pos[-1][1] > self.pos[-2][1]:  
                    tail = pygame.transform.rotate(self.tail_img, 180)  # Вниз
                else:
                    tail = self.tail_img  # Вверх

                window.blit(tail, (x, y))

            else:
                prev_x, prev_y = self.pos[i - 1]
                next_x, next_y = self.pos[i + 1]

                # Проверяем, если тело идет прямо (горизонтально или вертикально)
                if prev_x == next_x:  # Вертикальное тело
                    body = self.body_img
                elif prev_y == next_y:  # Горизонтальное тело
                    body = pygame.transform.rotate(self.body_img, 90)
                else:
                    # Для поворота тела
                    if (prev_x < self.pos[i][0] and next_y < self.pos[i][1]) or (next_x < self.pos[i][0] and prev_y < self.pos[i][1]):
                        body = pygame.transform.rotate(self.turn_img, 0)  
                    elif (prev_x < self.pos[i][0] and next_y > self.pos[i][1]) or (next_x < self.pos[i][0] and prev_y > self.pos[i][1]):
                        body = pygame.transform.rotate(self.turn_img, 270)  
                    elif (prev_x > self.pos[i][0] and next_y < self.pos[i][1]) or (next_x > self.pos[i][0] and prev_y < self.pos[i][1]):
                        body = pygame.transform.rotate(self.turn_img, 90)  
                    elif (prev_x > self.pos[i][0] and next_y > self.pos[i][1]) or (next_x > self.pos[i][0] and prev_y > self.pos[i][1]):
                        body = pygame.transform.rotate(self.turn_img, 180)  
                    else:
                        body = self.body_img  # ← запасной вариант, если ничего не подошло

                window.blit(body, (x, y))
