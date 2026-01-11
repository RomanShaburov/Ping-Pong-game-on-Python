from Colors import *
from random import *
import pygame
import math

class Bullet:
    def __init__(self, speed, start_x, start_y, way):
        """
        start_x, start_y: начальная позиция пули (позиция мяча)
        way: направление движения (-1 = влево, 1 = вправо)
        """
        self.way = way
        self.x = start_x
        self.y = start_y
        self.speed = speed

        # Случайное направление по оси Y (немного вверх или вниз)
        # Можно менять значение 0.5 для изменения угла
        random_y_direction = uniform(-0.5, 0.5)

        # Основное направление по X (влево или вправо)
        self.dx = way * speed * 0.8  # 0.8 - чтобы было немного медленнее по X
        self.dy = random_y_direction * speed  # 0.4 - чтобы меньше отклонялось по Y

        # Размер пули
        bullet_width = 40
        bullet_height = 20
        self.rect = pygame.Rect(self.x, self.y, bullet_width, bullet_height)

    def draw(self, screen):
        # Черный кружок в зависимости от направления
        if self.way < 0:  # Движется влево
            pygame.draw.circle(screen, black,
                               (self.rect.center[0] - 20, self.rect.center[1]),
                               10)
        else:  # Движется вправо
            pygame.draw.circle(screen, black,
                               (self.rect.center[0] + 20, self.rect.center[1]),
                               10)
        pygame.draw.rect(screen, yellow, self.rect)
        if self.way < 0:  # Движется влево
            pygame.draw.rect(screen, orange, (self.rect.center[0] + 5, self.rect.center[1] - 2
                                                  , 15, 5))
        else:  # Движется вправо
            pygame.draw.rect(screen, orange, (self.rect.center[0] - 20, self.rect.center[1] - 2
                                                  , 15, 5))


    def move(self):
        # Обновляем позицию
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Проверяем, вышла ли пуля за пределы экрана
        if (self.rect.right < 0 or
                self.rect.left > 1250 or
                self.rect.bottom < 0 or
                self.rect.top > 600):
            return True  # Пулю нужно удалить
        return False