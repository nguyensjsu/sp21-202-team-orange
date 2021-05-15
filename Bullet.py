import pygame
import math
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = radius
        self.dia = 3.14 * self.radius * self.radius
        self.color = color
        self.hitbox = pygame.Rect(x, y, self.dia, self.dia)
        self.hit = False
        self.power = 0
        self.angle = 0
        self.time = 0

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius-1)

    #@staticmethod
    # bullet projectile function
    def projectilePath(self, x, y):#, x, y):#, power, angle, time):
        velX = math.cos(self.angle) * self.power
        velY = math.sin(self.angle) * self.power

        distX = velX * self.time
        distY = (velY * self.time) + ((-4.9 * (self.time)**2)/2)

        newX = round(distX + x)
        newY = round(y - distY)

        return newX, newY