import pygame
from random import randint
class Booster:
    def __init__(self, name, screen, image_path=None, radius = 20):
        self.name = name # ускорение мяча к противнику, замедление ракетки противника, ускорение своей ракетки
                         # Уменьшение мяча, раздвоение мяча на 5 сек, увеличение своей ракетки
        self.radius = radius
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))

        self.rect = self.image.get_rect()
        self.rect.x = randint(400, 600)
        self.rect.y = randint(120, 480)
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def check_collision(self, ball_rect):
        return self.rect.colliderect(ball_rect)

    def update_position(self):
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def get_radius(self):
        return self.radius