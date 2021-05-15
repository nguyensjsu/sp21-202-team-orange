import pygame
import math
from Bullet import Bullet
WIDTH, HEIGHT = 900, 500
RED = (255, 0, 0)
class Player(pygame.sprite.Sprite):

    
    def __init__(self, x, y, image, subimg = None, player2 = False):
        pygame.sprite.Sprite.__init__(self)
        self.player2 = player2
        self.x = x
        self.y = y
        self.hp = 100
        self.width = 53#55
        self.height = 74#40
        self.image = pygame.transform.scale(image, (self.width, self.height))
        if subimg != None: self.subimage = pygame.transform.scale(subimg, (self.width, self.height))
        else: self.subimage = None
        self.alpha = 255
        self.speed = 5
        self.fuel = 100
        self.shield = 100
        self.angle = 0
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
    


    def get_image(self, window):
        #accounts for player 2 orientation difference
        if self.player2: temp_img = pygame.transform.rotate(pygame.transform.flip(self.image, True, False), 180)
        else: temp_img = self.image

        pivot = (self.x + self.width // 2, self.y + self.height // 2)
        rotated_image = pygame.transform.rotozoom(temp_img, self.angle, 1)  # Rotate the image.
        rotated_offset = pygame.math.Vector2(0,0) # Rotate the offset vector.
        rect = rotated_image.get_rect(center = pivot+rotated_offset) #rotate the new rectangle around the pivot
        window.blit(rotated_image, rect) #draw main rotated image to window
        if self.subimage != None: #if exists, draw subimage to window
            if self.player2: subimage = pygame.transform.flip(self.subimage, True, False)
            else: subimage = self.subimage
            window.blit(subimage, self.rect)
    


    def calc_angle(self, pos):
        try:
            angle = math.atan((self.y - pos[1])/(self.x-pos[0]))
        except:
            angle = math.pi/2
        if pos[0] < self.x:
            angle = math.pi - angle
        elif pos[1] < self.y:
            angle = abs(angle)
        elif pos[1] > self.y:
            angle = 2 * math.pi - angle
        self.angle = angle * 57.29 #this is just converting radian output to degrees