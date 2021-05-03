import os
import pygame
import math
pygame.font.init()
pygame.mixer.init()
MAX_BULLETS = 10
WHITE = (255,255,255)
FPS=60
WIDTH,HEIGHT = 900,500

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
#global player constants
PLAYER_WIDTH, PLAYER_HEIGHT = 55,40
#player1 constants
PLAYER1_IMAGE = pygame.image.load(os.path.join("images","spaceship_red.png"))
PLAYER1 = pygame.transform.rotate(pygame.transform.scale(PLAYER1_IMAGE,(PLAYER_WIDTH,PLAYER_HEIGHT)),90)
#player2 constants
PLAYER2_IMAGE = pygame.transform.rotate(pygame.image.load(os.path.join("images","spaceship_yellow.png")),270)
PLAYER2 = pygame.transform.scale(PLAYER2_IMAGE,(PLAYER_WIDTH,PLAYER_HEIGHT))
#object speeds
BULLET_SPEED = 10
SPEED = 5
#players getting hit event
PLAYER1_HIT = pygame.USEREVENT + 1
PLAYER2_HIT = pygame.USEREVENT + 2
#player turn
PLAYER1_TURN = pygame.USEREVENT + 3
PLAYER2_TURN = pygame.USEREVENT + 4
#fonts
HEALTH_FONT = pygame.font.SysFont("Times New Roman",40)
WINNER_FONT = pygame.font.SysFont("Times New Roman",100)
#sound
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("images","Assets_Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("images","Assets_Gun+Silencer.mp3"))

BG_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images","background.jpg")),(WIDTH,HEIGHT))

pygame.display.set_caption("Worms")

class bullet(object):
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


def player1_move(keys_pressed,player1,bullet):
    if keys_pressed[pygame.K_LEFT] and player1.x - SPEED > 0:
        player1.x -= SPEED
    if keys_pressed[pygame.K_RIGHT] and player1.x + SPEED + player1.width < WIDTH :
        player1.x += SPEED

def player2_move(keys_pressed,player2,bullet):
    if keys_pressed[pygame.K_a] and player2.x - SPEED > 0:                #a is pressed
        player2.x -= SPEED
        bullet.x -=SPEED
    if keys_pressed[pygame.K_d] and player2.x + SPEED + player2.width < WIDTH:                #d is pressed
        player2.x += SPEED
        bullet.x +=SPEED

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

def draw_window(p1,p2,p1_b,p2_b,line,bullet1,bullet2,p1_hp,p2_hp):
    #draw background
    WIN.blit(BG_IMAGE,(0,0))
    #draw player health bars
    p1_health_text = HEALTH_FONT.render("Health: "+ str(p1_hp),1,WHITE)
    p2_health_text = HEALTH_FONT.render("Health: "+ str(p2_hp),1,WHITE)
    WIN.blit(p1_health_text,(WIDTH - p1_health_text.get_width()-10,10))
    WIN.blit(p2_health_text,((10,10)))
    #draw projectile
    bullet1.draw(WIN)
    bullet2.draw(WIN)
    #draw players
    WIN.blit(PLAYER1,(p1.x,p1.y))                        
    WIN.blit(PLAYER2,(p2.x,p2.y))  

        

    #pygame.draw.line(WIN,WHITE,line[0],line[1])

    #update each frame
    pygame.display.update()

def main():
    player1 = pygame.Rect(700,300,PLAYER_WIDTH,PLAYER_HEIGHT)
    player2 = pygame.Rect(100,300,PLAYER_WIDTH,PLAYER_HEIGHT)
    bullet1 = bullet(player1.x, player1.y+player1.height//2 -2,5,WHITE)
    bullet2 = bullet(player2.x+player2.width-8, player2.y+player2.height//2 -2,5,WHITE)
    #bullet = pygame.Rect(player2.x+player2.width, player2.y+player2.height//2 -2 , 10 , 5)
    x = 0
    y = 0
    time = 0
    power = 0
    angle = 0
    shoot= False

    #bullets for players
    p1_bullets = []
    p2_bullets = []
    #hitpoints for players
    p1_hp = 100
    p2_hp = 100

    #control fps
    clock = pygame.time.Clock()
    run = True
    while run:
        if shoot:
            if bullet2.y <500 - bullet2.radius:
                time += 0.05
                poss = bullet2.projectilePath(x,y,power,angle,time)
                bullet2.x = poss[0]
                bullet2.y = poss[1]
            else:
                shoot=False
                bullet2.x = player2.x+player2.width-8
                bullet2.y = player2.y+player2.height//2 -2
        #position of the mouse
        pos = pygame.mouse.get_pos()
        #invisible line determining the angle of the projectile
        line1 = [(player1.x, player1.y+player1.height//2 -2),pos]
        line2 = [(player2.x+player2.width-8,player2.y+player2.height//2 -2),pos]
        clock.tick(FPS)
        for event in pygame.event.get():
            #press close window event
            if event.type == pygame.QUIT:
                run = False
            #keypress event
            if event.type == pygame.KEYDOWN:
                print("hi")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shoot == False:
                    BULLET_FIRE_SOUND.play()
                    shoot = True
                    #if event.type == PLAYER1_TURN:
                        #x = player1.x
                        #y = player1.y
                        #time = 0
                        #power = math.sqrt((line[1][1]-line[0][1])**2 +(line[1][0]-line[0][0])**2)/8
                        #angle = findAngle(pos,player1,player2)
                    #elif event.type == PLAYER2_TURN:
                    #    x = player2.x
                    #    y = player2.y
                    #    time = 0
                    #    power = 0
                    #    power = math.sqrt((line[1][1]-line[0][1])**2 +(line[1][0]-line[0][0])**2)/8
                    #    angle = findAngle(pos,player1,player2)
                    
                    x = bullet2.x
                    y = bullet2.y
                    time = 0
                    power = math.sqrt((line2[1][1]-line2[0][1])**2 +(line2[1][0]-line2[0][0])**2)/8
                    angle = findAngle(pos,player1,bullet2)
            if event.type  == PLAYER1_HIT:
                p1_hp -= 10

            if event.type  == PLAYER2_HIT:
                p2_hp -= 10
            
            winner_text = ""
            if p1_hp <= 0:
                winner_text = "PLAYER 2 WINS!"
            if p2_hp <= 0:
                winner_text = "PLAYER 1 WINS!"

            if winner_text != "":
                draw_winner(winner_text)
                break

        keys_pressed = pygame.key.get_pressed()
        player1_move(keys_pressed,player1,bullet1)
        player2_move(keys_pressed,player2,bullet2)

        handle_bullets(p1_bullets,p2_bullets,player1,player2,bullet2)

        draw_window(player1,player2,p1_bullets,p2_bullets,line2,bullet1,bullet2,p1_hp,p2_hp)
    pygame.quit()

if __name__ == "__main__":
    main()