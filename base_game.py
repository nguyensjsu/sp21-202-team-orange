import random
import sys
import math
import pygame
from os import path
from camera import *
from Bullet import *
from Player import *
from Explosion import *
# Set False if audio works for you; pygame has audio problems on my desktop. -William
audio_compat = True
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')


pygame.font.init()
if not audio_compat:
    pygame.mixer.init()
# General game attributes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60
WIDTH, HEIGHT = 900, 500
HEALTH_FONT = pygame.font.Font("KGHolocene.ttf", 20)
WINNER_FONT = pygame.font.Font("Public.otf", 100)
# sound
if not audio_compat:
    BULLET_HIT_SOUND = []
    for snd in ['expl3.wav', 'expl6.wav']:
        BULLET_HIT_SOUND.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
    BULLET_FIRE_SOUND = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
    MAIN_BG_SOUND = pygame.mixer.Sound(path.join(snd_dir, "frozenjam.ogg"))
    GAME_BG_SOUND = pygame.mixer.Sound(path.join(snd_dir, "Game_BG.ogg"))
    pygame.mixer.music.set_volume(0.1)

# Backgrounds
GAME_IMAGE = pygame.transform.scale(pygame.image.load(
    path.join(img_dir, "BG.png")), (WIDTH, HEIGHT))
MAIN_IMAGE = pygame.transform.scale(pygame.image.load(
    path.join(img_dir, "background.jpg")), (WIDTH, HEIGHT))



WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#MENUSCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
# players getting hit event
PLAYER1_HIT = pygame.USEREVENT + 1
PLAYER2_HIT = pygame.USEREVENT + 2

pygame.display.set_caption("Worms")
use_snow = True
snow_list = []
# control fps
clock = pygame.time.Clock()



def handle_bullets(active_player: Player, dormant_player: Player, isPlayer1: bool):
    # if (active_player.bullet.hit == False):
    if (active_player.bullet.y - active_player.bullet.radius < dormant_player.rect[1] + dormant_player.rect[3] and
            active_player.bullet.y + active_player.bullet.radius > dormant_player.rect[1]):
        if (active_player.bullet.x + active_player.bullet.radius > dormant_player.rect[0] and
                active_player.bullet.x - active_player.bullet.radius < dormant_player.rect[0] + dormant_player.rect[2]):
            if isPlayer1:
                pygame.event.post(pygame.event.Event(PLAYER2_HIT))
            else:
                pygame.event.post(pygame.event.Event(PLAYER1_HIT))
            active_player.reset_bullet()


def findAngle(pos, obj):
    try:
        angle = math.atan((obj.y - pos[1])/(obj.x-pos[0]))
    except:
        angle = math.pi/2

    if pos[0] < obj.x:
        angle = math.pi - angle
    elif pos[1] < obj.y:
        angle = abs(angle)
    elif pos[1] > obj.y:
        angle = 2 * math.pi - angle
    # if pos[1] < obj.y and pos[0] > obj.x:
    #     angle = abs(angle)
    # elif pos[1] < obj.y and pos[0] < obj.x:
    #     angle = math.pi - angle
    # elif pos[1] > obj.y and pos[0] < obj.x:
    #     angle = math.pi - angle
    # elif pos[1] > obj.y and pos[0] > obj.x:
    #     angle = (math.pi*2) - angle
    return angle


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2-draw_text.get_width() /
             2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.time.delay(1500)
    pygame.display.update()
    


def draw_window(p1, p2, turn):
    # draw background
    WIN.blit(GAME_IMAGE, (0, 0))
    # draw player health bars
    p1_health_text = HEALTH_FONT.render("P2 Health: " + str(p1.hp), 1, WHITE)
    p2_health_text = HEALTH_FONT.render("P1 Health: " + str(p2.hp), 1, WHITE)
    WIN.blit(p1_health_text, (WIDTH - p1_health_text.get_width()-10, 10))
    WIN.blit(p2_health_text, ((10, 10)))

    if turn == 1:
        p1_turn = HEALTH_FONT.render("PLAYER 1's Turn", 1, WHITE)
        WIN.blit(p1_turn, ((300, 100)))

    if turn == 2:
        p2_turn = HEALTH_FONT.render("PLAYER 2's Turn", 1, WHITE)
        WIN.blit(p2_turn, ((300, 100)))
    # draw projectile
    p1.bullet.draw(WIN)
    p2.bullet.draw(WIN)
    # draw players
    p1.image.set_alpha(p1.alpha)
    p2.image.set_alpha(p2.alpha)
    WIN.blit(p1.get_image(), (p1.x, p1.y))
    WIN.blit(p2.get_image(), (p2.x, p2.y))

    # pygame.draw.line(WIN,WHITE,line[0],line[1])
    # pygame.draw.line(WIN,WHITE,line2[0],line2[1])

    # update each frame
    pygame.display.update()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def draw_snow():
    for i in range(len(snow_list)):
        pygame.draw.circle(WIN, WHITE, snow_list[i], 2)
        snow_list[i][1] += 1

        if (snow_list[i][1] > HEIGHT):
            y = random.randrange(-20, 0)
            x = random.randrange(0, WIDTH)
            snow_list[i][0] = x
            snow_list[i][1] = y

    pygame.display.update()

def show_go_screen():
    WIN.blit(MAIN_IMAGE, (0,0))
    draw_text('GAME NAME', HEALTH_FONT, WHITE, WIN, 320, 100)
    draw_text("A and D to move, Mouse to fire",HEALTH_FONT,WHITE, WIN, 220, 270)
    draw_text("Press a key to begin",HEALTH_FONT, WHITE, WIN, 300, 350)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()
            if event.type == pygame.KEYUP:
                waiting = False


def main():
    click = False
    while True:

        WIN.blit(MAIN_IMAGE, (0, 0))
        draw_text('Main Menu', HEALTH_FONT, WHITE, WIN, 20, 20)

        if not audio_compat:
            MAIN_BG_SOUND.play()

        mx, my = pygame.mouse.get_pos()

        game_start_button = pygame.Rect(50, 100, 200, 50)
        controls_button = pygame.Rect(50, 200, 200, 50)
        credits_button = pygame.Rect(50, 300, 200, 50)

        if game_start_button.collidepoint((mx, my)) and click:
            game()
        if controls_button.collidepoint((mx, my)) and click:
            controls()
        if credits_button.collidepoint((mx, my)) and click:
            credit()
        pygame.draw.rect(WIN, (255, 0, 0), game_start_button)
        pygame.draw.rect(WIN, (255, 0, 0), controls_button)
        pygame.draw.rect(WIN, (255, 0, 0), credits_button)

        draw_text('Start Game', HEALTH_FONT, (255, 255, 255), WIN, 50, 100)
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

    if not audio_compat:
        MAIN_BG_SOUND.stop()
        GAME_BG_SOUND.play()


    # Setup snow
    if (use_snow):
        for i in range(60):
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, HEIGHT)
            snow_list.append([x, y])

    
    game_over = True
    run = True
    while run:
        
        #Resets the gameloop 
        if game_over:
           show_go_screen()
           game_over = False
           player1 = Player(700, 300, pygame.image.load(
                path.join(img_dir, "spaceship_red.png")))
           player2 = Player(100, 300, pygame.image.load(
                path.join(img_dir, "spaceship_yellow.png")))
           all_sprites = pygame.sprite.Group()
           player_1_turn = True
           active_player = player1
           dormant_player = player2
           active_player.hp = 100
           dormant_player.hp = 100

           bul = active_player.bullet 
           camera = Camera(bul)
           follow = Follow(camera,bul)
           border = Border(camera,bul)

           camera.setmethod(follow)

           x = 0
           y = 0
           time = 0
           power = 0
           angle = 0
           shoot = False
           hit_registered = False


        # Update the snow flakes
        if (use_snow):
            draw_snow()
        if shoot:
            camera.scroll()
            if active_player.bullet.y < 362 and not hit_registered:  # bullet is still within frame
                active_player.bullet.time += 0.25
                active_player.bullet.x, active_player.bullet.y = active_player.bullet.projectilePath(
                    x, y)
            else:  # bullet has left frame boundary
                shoot = False
                hit_registered = False
                player_1_turn = not player_1_turn
                active_player.reset_bullet()  # retrive bullet
                active_player.fuel = 100
                # switch active and dormant roles
                temp = active_player
                active_player = dormant_player
                dormant_player = temp
        
        all_sprites.update()

        # position of the mouse
        pos = pygame.mouse.get_pos()

        #rotate active player sprite to match aim
        active_player.angle = findAngle(pos, active_player) * 57.29 #this is just converting radian output to

        # invisible line determining the angle of the projectile
        line1 = [(active_player.x + 10, active_player.y + active_player.height // 2 - 2), pos]
        #line2 = [(player2.x + player2.width - 8,
                  #player2.y + player2.height // 2 - 2), pos]

        clock.tick(FPS)
        click = False
        
        for event in pygame.event.get():

            # press close window event
            if event.type == pygame.QUIT:
                run = False
            # keypress event
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not audio_compat:
                        GAME_BG_SOUND.stop()
                    main()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                if shoot == False:
                    if player_1_turn:
                        print("1")
                    else:
                        print("2")
                    if not audio_compat:
                        BULLET_FIRE_SOUND.play()
                    shoot = True

                    x, y = active_player.new_bullet()
                    active_player.bullet.time = 0
                    active_player.bullet.power = math.sqrt(
                            (line1[1][1] - line1[0][1]) ** 2 + (line1[1][0] - line1[0][0]) ** 2) / 8
                    active_player.bullet.angle = findAngle(pos, active_player.bullet)

            # not sure how these hit events are meant to happen; collision doesn't seem to work yet
            elif event.type == PLAYER1_HIT or event.type == PLAYER2_HIT:
                if not hit_registered:
                    dormant_player.hp -= 50
                    if not audio_compat:
                        random.choice(BULLET_HIT_SOUND).play()
                    expl = Explosion( dormant_player.rect.center, 'lg')
                    all_sprites.add(expl)
                    hit_registered = True

            #pygame.sprite.spritecollide(dormant_player, active_player.bullet, True)
    
            if active_player.hp <= 0:  # if active player's HP is 0, that means the other player killed them last turn 
               #simple formula to generate winning text instead of layers of conditionals
                if active_player == player1:
                    draw_winner("PLAYER 1 WINS!")
                   
                if active_player == player2:
                    draw_winner("PLAYER 2 WINS!")
                pygame.time.delay(3000)
                game_over=True


        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            active_player.move_left()
        elif pressed[pygame.K_d]:
            active_player.move_right()

        handle_bullets(active_player, dormant_player, player_1_turn)
        draw_window(player1, player2, int(player_1_turn) + 1)
       
        pygame.draw.rect(WIN, (255, 0, 0), player1.rect, 2)
        pygame.draw.rect(WIN, (255, 0, 0), player2.rect, 2)

        all_sprites.draw(WIN)

    pygame.quit()


def controls():
    running = True
    
    while running:
        WIN.blit(MAIN_IMAGE, (0,0))
        draw_text('A and D to move', HEALTH_FONT, WHITE, WIN, 320, 100)
        draw_text("Mouse to fire",HEALTH_FONT,WHITE, WIN, 320, 100)
        pygame.display.flip()
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
        WIN.blit(MAIN_IMAGE, (0,0))
        draw_text('Credits', HEALTH_FONT, WHITE, WIN, 20, 20)
        draw_text('Ryan Choy, 014499316', HEALTH_FONT, WHITE, WIN, 50, 100)
        draw_text('Janaarthana Harri, 015246205',
                  HEALTH_FONT, WHITE, WIN, 50, 200)
        draw_text('Premchand, 015326428', HEALTH_FONT, WHITE, WIN, 50, 300)
        draw_text('William Su, 013697658', HEALTH_FONT, WHITE, WIN, 50, 400)
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
