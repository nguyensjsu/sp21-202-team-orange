import pygame
import os
BLACK = (0,0,0)
#explosion animation 
#load the images into the list
explosion_anim = {}
explosion_anim['lg'] = []
for i in range(9):
    file = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join("images", file))
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (72, 72))
    explosion_anim['lg'].append(img_lg)
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
