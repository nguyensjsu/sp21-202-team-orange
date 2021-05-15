import pygame
from Bullet import Bullet
WIDTH, HEIGHT = 900, 500
RED = (255, 0, 0)
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.hp = 100
        self.width = 55
        self.height = 40
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.alpha = 255
        self.speed = 5
        self.fuel = 100
        self.shield = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bullet = Bullet(self.x + self.width // 2,
                             self.y + self.height // 2, 5, RED)

    def move_left(self):
        if self.x - self.speed > 0 and self.fuel > 0:
            self.x -= self.speed
            self.fuel -= self.speed
            self.bullet.x -= self.speed
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_right(self):
        if self.x + self.speed + self.width < WIDTH and self.fuel > 0:
            self.x += self.speed
            self.fuel -= self.speed
            self.bullet.x += self.speed
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def reset_bullet(self):
        # self.bullet = None
        self.bullet.x = self.x + self.width // 2
        self.bullet.y = self.y + self.height // 2
        self.bullet.time = 0

    def new_bullet(self):
        self.bullet = Bullet(self.x + self.width // 2,
                             self.y + self.height // 2, 5, RED)
        return self.x, self.y