import pygame
vec = pygame.math.Vector2

class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0,0)
        self.offset_float = vec(0,0)
        self.DISPLAY_W, self.DISPLAY_H = 500,300
        self.CONST = vec(-self.DISPLAY_W/2 + ((player.radius)*2) / 2, -382)
    def setmethod(self,method):
        self.method = method
    
    def scroll(self):
        self.method.scroll()

class CamScroll():
    def __init__(self,camera,player):
        self.camera=camera
        self.player=player

    def scroll(self):
        pass

class Follow(CamScroll):
    def __init__(self,camera,player):
        CamScroll.__init__(self,camera,player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.x = int(self.camera.offset_float.x), int(self.camera.offset_float.y)

class Border(CamScroll):
    def __init__(self,camera,player):
        CamScroll.__init__(self,camera,player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.x = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.player.left_border, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, self.player.right_border - self.camera.DISPLAY_W)