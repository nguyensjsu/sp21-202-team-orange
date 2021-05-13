audio_compat = True #Set False if audio works for you; pygame has audio problems on my desktop.

import os
import pygame
import math
import sys
import random
import os

pygame.font.init()
if not audio_compat: pygame.mixer.init()
# MAX_BULLETS = 10
# General constants
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
FPS=60
WIDTH,HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
#MENUSCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
#object speeds
# BULLET_SPEED = 10
SPEED = 5
#players getting hit event
PLAYER1_HIT = pygame.USEREVENT + 1
PLAYER2_HIT = pygame.USEREVENT + 2
#player turn
PLAYER_TURN = 2
#fonts
HEALTH_FONT = pygame.font.SysFont("Times New Roman",40)
WINNER_FONT = pygame.font.SysFont("Times New Roman",100)
#sound
if not audio_compat:
    BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("images","Assets_Grenade+1.mp3"))
    BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("images","Assets_Gun+Silencer.mp3"))
    MAIN_BG_SOUND = pygame.mixer.Sound(os.path.join("images", "Main_BG.ogg" ))
    GAME_BG_SOUND = pygame.mixer.Sound(os.path.join("images","Game_BG.ogg"))
#Backgrounds
GAME_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images","BG.png")),(WIDTH,HEIGHT))
MAIN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images","background.jpg")),(WIDTH,HEIGHT))

pygame.display.set_caption("Worms")
use_snow = True
snow_list = []

class Bullet(object):
    def __init__(self, x,y , radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    
    def draw(self,win):
        pygame.draw.circle(win,(0,0,0),(self.x,self.y),self.radius)
        pygame.draw.circle(win,self.color, (self.x,self.y), self.radius-1)

    @staticmethod
    #bullet projectile function
    def projectilePath(x,y,power ,angle, time):
        velX = math.cos(angle) * power
        velY = math.sin(angle) * power

        distX = velX * time
        distY = (velY * time) + ((-4.9 * (time)**2)/2)

        newX = round(distX + x)
        newY = round(y - distY)

        return (newX,newY)


class Player:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.hp = 100
        self.width = 55
        self.height = 40
        self.image = pygame.transform.scale(image,(self.width,self.height))
        self.bullets = []
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, 5, RED)

    def move_left(self):
        if self.x - SPEED > 0:
            self.x -= self.speed
            self.bullet.x -= self.speed
    def move_right(self):
        if self.x + SPEED + self.width < WIDTH :
            self.x += self.speed
            self.bullet.x += self.speed


# def player1_move(keys_pressed,player1,bullet):
#     if keys_pressed[pygame.K_LEFT] and player1.x - SPEED > 0:
#         player1.x -= SPEED
#         bullet.x -=SPEED
#     if keys_pressed[pygame.K_RIGHT] and player1.x + SPEED + player1.width < WIDTH :
#         player1.x += SPEED
#         bullet.x +=SPEED

# def player2_move(keys_pressed,player2,bullet):
#     if keys_pressed[pygame.K_a] and player2.x - SPEED > 0:                #a is pressed
#         player2.x -= SPEED
#         bullet.x -=SPEED
#     if keys_pressed[pygame.K_d] and player2.x + SPEED + player2.width < WIDTH:                #d is pressed
#         player2.x += SPEED
#         bullet.x +=SPEED

def handle_bullets(p1_b,p2_b,p1,p2,bullet):
    #for bullet in p2_b:
    #    bullet.x += BULLET_SPEED
    #    if p1.colliderect(bullet):
    #        pygame.event.post(pygame.event.Event(PLAYER1_HIT))
    #        p2_b.remove(bullet)
    #    elif bullet.x > WIDTH:
    #        p2_b.remove(bullet)

    #for bullet in p1_b:
    #    bullet.x -= BULLET_SPEED
    #    if p2.colliderect(bullet):
    #        pygame.event.post(pygame.event.Event(PLAYER2_HIT))
    #        p1_b.remove(bullet)
    #    elif bullet.x <0:
    #        p1_b.remove(bullet)
    #if p1.colliderect(bullet):
        #pygame.event.post(pygame.event.Event(PLAYER2_HIT))
    pass
    

def findAngle(pos,p1,p2):
    #player 1
    s1X = p1.x
    s1Y = p1.y
    #player 2
    s2X = p2.x
    s2Y = p2.y
    try:
        angle = math.atan((s2Y - pos[1])/(s2X-pos[0]))
    except:
        angle = math.pi/2

    if pos[1] < s2Y and pos[0] > s2X:
        angle = abs(angle)
    elif pos[1] < s2Y and pos[0] < s2X:
        angle = math.pi - angle
    elif pos[1] > s2Y and pos[0] < s2X:
        angle = math.pi - abs(angle)
    elif pos[1] > s2Y and pos[0] > s2X:
        angle = (math.pi*2) - angle
    return angle

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()/2,HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)


def draw_window(p1, p2, line, line2, turn):
    #draw background
    WIN.blit(GAME_IMAGE,(0,0))
    #draw player health bars
    p1_health_text = HEALTH_FONT.render("P1 Health: "+ str(p1.hp),1,WHITE)
    p2_health_text = HEALTH_FONT.render("P2 Health: "+ str(p2.hp),1,WHITE)
    WIN.blit(p1_health_text,(WIDTH - p1_health_text.get_width()-10,10))
    WIN.blit(p2_health_text,((10,10)))

    if turn == 1:
        p1_turn = HEALTH_FONT.render("PLAYER 1's Turn",1,WHITE)
        WIN.blit(p1_turn,((300,100)))
    
    if turn == 2:
        p2_turn = HEALTH_FONT.render("PLAYER 2's Turn",1,WHITE)
        WIN.blit(p2_turn,((300,100)))
    #draw projectile
    p1.bullet.draw(WIN)
    p2.bullet.draw(WIN)
    #draw players
    WIN.blit(p1.image,(p1.x,p1.y))                        
    WIN.blit(p2.image,(p2.x,p2.y))  

    #pygame.draw.line(WIN,WHITE,line[0],line[1])
    #pygame.draw.line(WIN,WHITE,line2[0],line2[1])

    #update each frame
    pygame.display.update()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_snow():
    for i in range (len(snow_list)):
        pygame.draw.circle(WIN, WHITE, snow_list[i], 2)
        snow_list[i][1] += 1

        if (snow_list[i][1] > HEIGHT):
            y = random.randrange(-20, 0)
            x = random.randrange(0, WIDTH)
            snow_list[i][0] = x
            snow_list[i][1] = y

    pygame.display.update()    

def main():
    click = False
    while True:
        
        WIN.blit(MAIN_IMAGE,(0,0))
        draw_text('main menu', HEALTH_FONT, WHITE, WIN, 20, 20)

        if not audio_compat: MAIN_BG_SOUND.play()
 
        mx, my = pygame.mouse.get_pos()

        game_start_button = pygame.Rect(50, 100, 200, 50)
        controls_button = pygame.Rect(50, 200, 200, 50)
        credits_button = pygame.Rect(50, 300, 200, 50)

        
        if game_start_button.collidepoint((mx, my)) and click: game()
        if controls_button.collidepoint((mx, my)) and click: controls() 
        if credits_button.collidepoint((mx, my)) and click: credit() 
        pygame.draw.rect(WIN, (255, 0, 0), game_start_button)
        pygame.draw.rect(WIN, (255, 0, 0), controls_button)
        pygame.draw.rect(WIN, (255, 0, 0), credits_button)

        draw_text('Play', HEALTH_FONT, (255, 255, 255), WIN, 50, 100)
        draw_text('Controls', HEALTH_FONT, (255, 255, 255), WIN, 50, 200)
        draw_text('Credits', HEALTH_FONT, (255, 255, 255), WIN, 50, 300)
 
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def game():
    # player1 = pygame.Rect(700,300,PLAYER_WIDTH,PLAYER_HEIGHT)
    # player2 = pygame.Rect(100,300,PLAYER_WIDTH,PLAYER_HEIGHT)
    player1 = Player(700, 300, pygame.image.load(os.path.join("images","spaceship_red.png")))
    player2 = Player(100, 300, pygame.image.load(os.path.join("images","spaceship_yellow.png")))
    # bullet1 = Bullet(player1.x+10 , player1.y+player1.height//2 +2,5, RED)
    # bullet2 = Bullet(player2.x+player2.width-8, player2.y+player2.height//2 -2,5, RED)
    
    if not audio_compat:
        MAIN_BG_SOUND.stop()
        GAME_BG_SOUND.play()
    PLAYER_TURN = 1

    #bullet = pygame.Rect(player2.x+player2.width, player2.y+player2.height//2 -2 , 10 , 5)
    
    x = 0
    y = 0
    time = 0
    power = 0
    angle = 0
    shoot= False
    click = False
    #bullets for players
    # p1_bullets = []
    # p2_bullets = []
    #hitpoints for players
    # p1_hp = 100
    # p2_hp = 100

    #Setup snow
    if (use_snow):
        for i in range(60):
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, HEIGHT)
            snow_list.append([x,y])

    #control fps
    clock = pygame.time.Clock()
    run = True
    while run:

        #Update the snow flakes
        if (use_snow):
            draw_snow()
        
        if PLAYER_TURN == 1:
            if shoot:
                if player1.bullet.y <500 - player2.bullet.radius:
                    time += 0.05
                    poss = player1.bullet.projectilePath(x,y,power,angle,time)
                    player1.bullet.x = poss[0]
                    player1.bullet.y = poss[1]
                else:
                    shoot=False
                    PLAYER_TURN = 2
                    player1.bullet.x = player1.x + 10
                    player1.bullet.y = player1.y + player1.height // 2 - 2
        if PLAYER_TURN == 2:
            if shoot:
                if player2.bullet.y < 500 - player2.bullet.radius:
                    time += 0.05
                    poss = player2.bullet.projectilePath(x, y, power, angle, time)
                    player2.bullet.x = poss[0]
                    player2.bullet.y = poss[1]
                    
                else:
                    shoot=False
                    PLAYER_TURN = 1
                    player2.bullet.x = player2.x + player2.width - 8
                    player2.bullet.y = player2.y + player2.height // 2 - 2
                
        #position of the mouse
        pos = pygame.mouse.get_pos()
        #invisible line determining the angle of the projectile
        line1 = [(player1.x + 10, player1.y + player1.height // 2 - 2), pos]
        line2 = [(player2.x + player2.width - 8, player2.y + player2.height // 2 - 2), pos]
        clock.tick(FPS)
        click=False
        for event in pygame.event.get():
            #press close window event
            if event.type == pygame.QUIT:
                run = False
            #keypress event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    GAME_BG_SOUND.stop()
                    main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                if shoot == False:
                    print(PLAYER_TURN)
                    if not audio_compat: BULLET_FIRE_SOUND.play()
                    shoot = True
                    if PLAYER_TURN == 1:
                        x = player1.bullet.x
                        y = player1.bullet.y
                        time = 0
                        power = math.sqrt((line1[1][1] - line1[0][1]) ** 2 + (line1[1][0] - line1[0][0]) ** 2) / 8
                        angle = findAngle(pos, player1, player1.bullet)
                    if PLAYER_TURN == 2:
                        x = player2.bullet.x
                        y = player2.bullet.y
                        time = 0
                        power = math.sqrt((line2[1][1] - line2[0][1]) ** 2 + (line2[1][0] - line2[0][0]) ** 2) / 8
                        angle = findAngle(pos, player2, player2.bullet)
                    
                    #x = bullet2.x
                    #y = bullet2.y
                   # time = 0
                    #power = math.sqrt((line2[1][1]-line2[0][1])**2 +(line2[1][0]-line2[0][0])**2)/8
                    #angle = findAngle(pos,player2,bullet2)

                    #x = bullet1.x
                    #y = bullet1.y
                    #time = 0
                    #power = math.sqrt((line1[1][1]-line1[0][1])**2 +(line1[1][0]-line1[0][0])**2)/8
                    #angle = findAngle(pos,player1,bullet1)

            if event.type  == PLAYER1_HIT:
                player1.hp -= 10

            if event.type  == PLAYER2_HIT:
                player2.hp -= 10
            
            winner_text = ""
            if player1.hp <= 0:
                winner_text = "PLAYER 2 WINS!"
            if player2.hp <= 0:
                winner_text = "PLAYER 1 WINS!"

            if winner_text != "":
                draw_winner(winner_text)
                break

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            if PLAYER_TURN == 1:
                player1.move_left()
            if PLAYER_TURN == 2:
                player2.move_left()
        if keys_pressed[pygame.K_d]:
            if PLAYER_TURN == 1:
                player1.move_right()
            if PLAYER_TURN == 2:
                player2.move_right()

        # handle_bullets(player1.bullets,player2.bullets,player1.rect,player2.rect,bullet2)
        draw_window(player1, player2, line1, line2, PLAYER_TURN)

        
    pygame.quit()

def controls():
    running = True
    while running:
        WIN.fill((0,0,0))
 
        draw_text('Controls', HEALTH_FONT, (255, 255, 255), WIN, 20, 20)
        draw_text('Use Mouse to Shoot', HEALTH_FONT, (255, 255, 255), WIN, 20, 100)
        draw_text('Player 1 uses a and d to move left and right', HEALTH_FONT, (255, 255, 255), WIN, 20, 200)
        draw_text('Player 2 uses left arrow key and right arrow key ', HEALTH_FONT, (255, 255, 255), WIN, 20, 300)
        draw_text('to move left and right', HEALTH_FONT, (255, 255, 255), WIN, 20, 400)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.update()

def credit():
    running = True
    while running:
        WIN.fill((0,0,0))
 
        draw_text('Credits', HEALTH_FONT, (255, 255, 255), WIN, 20, 20)
        draw_text('Ryan Choy, 014499316', HEALTH_FONT, (255, 255, 255), WIN, 50, 100)
        draw_text('Janaarthana Harri, 015246205', HEALTH_FONT, (255, 255, 255), WIN, 50, 200)
        draw_text('Premchand, ID number', HEALTH_FONT, (255, 255, 255), WIN, 50, 300)
        draw_text('William Su, 013697658', HEALTH_FONT, (255, 255, 255), WIN, 50, 400)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.update()

if __name__ == "__main__":
    main() 
