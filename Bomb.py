import pygame
from random import randint
from Colors import *


class Bomb:
    def __init__(self, screen, image_path=None, radius=20):
        self.radius = radius
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))
            except:
                self.create_simple_image()
        else:
            self.create_simple_image()

        self.rect = self.image.get_rect()
        self.rect.x = randint(400, 600)
        self.rect.y = randint(120, 480)
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def create_simple_image(self):
        size = self.radius * 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius, 3)
        pygame.draw.rect(self.image, (0, 0, 0),
                         (self.radius - 3, 5, 6, self.radius // 2))

        self.spark_color = (255, 255, 0)  # Желтый
        self.spark_color1 = orange

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if pygame.time.get_ticks() % 300 < 200:  # Мигает каждые 300мс
            spark_size = 7
            mini_spark_size = 4
            spark_surface = pygame.Surface((spark_size * 2, spark_size * 2), pygame.SRCALPHA)
            mini_spark_surface = pygame.Surface((spark_size * 2, spark_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(spark_surface, (255, 255, 0, 180),
                               (spark_size, spark_size), spark_size)
            pygame.draw.circle(mini_spark_surface, (255, 178, 102, 200),
                               (mini_spark_size, mini_spark_size), mini_spark_size)
            screen.blit(spark_surface,
                        (self.rect.centerx - spark_size + 12,
                         self.rect.top - spark_size + 7))
            screen.blit(mini_spark_surface,
                        (self.rect.centerx - mini_spark_size + 12,
                         self.rect.top - mini_spark_size + 7))

    def check_collision(self, ball_rect):
        return self.rect.colliderect(ball_rect)

    def update_position(self):
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def get_radius(self):
        return self.radius