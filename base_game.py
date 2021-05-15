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
audio_compat = False
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
hero_images = {
    0 : ("spaceship_yellow.png", None),
    1 : ("tank.png", None),
    2 : ("jet-plane.png", None),
    3 : ("submarine.png", None),
    4 : ("arm.png", "body.png"),
    5 : ("spaceship_red.png", None),
    6 : ("tank2.png", None),
    7 : ("jet-plane2.png", None),
    8 : ("submarine2.png", None),
    9 : ("arm.png", "body.png")
}


pygame.font.init()
if not audio_compat:
    pygame.mixer.init()
# General game attributes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 100, 10)

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
    BUTTON_PRESS = pygame.mixer.Sound(path.join(snd_dir, "button.mp3"))
    pygame.mixer.music.set_volume(0.1)

# Backgrounds
GAME_IMAGE = pygame.transform.scale(pygame.image.load(
    path.join(img_dir, "BG.png")), (WIDTH, HEIGHT))
MAIN_IMAGE = pygame.transform.scale(pygame.image.load(
    path.join(img_dir, "background.jpg")), (WIDTH, HEIGHT))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# create players getting hit event
PLAYER1_HIT = pygame.USEREVENT + 1
PLAYER2_HIT = pygame.USEREVENT + 2

pygame.display.set_caption("Worms")
use_snow = True
snow_list = []
# control fps
clock = pygame.time.Clock()



def handle_bullets(active_player: Player, dormant_player: Player, isPlayer1: bool):
    if (active_player.bullet.y - active_player.bullet.radius < dormant_player.rect[1] + dormant_player.rect[3] and
            active_player.bullet.y + active_player.bullet.radius > dormant_player.rect[1]):
        if (active_player.bullet.x + active_player.bullet.radius > dormant_player.rect[0] and
                active_player.bullet.x - active_player.bullet.radius < dormant_player.rect[0] + dormant_player.rect[2]):
            if isPlayer1:
                pygame.event.post(pygame.event.Event(PLAYER2_HIT))
            else:
                pygame.event.post(pygame.event.Event(PLAYER1_HIT))
            active_player.reset_bullet()



def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2-draw_text.get_width() /
             2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.time.delay(1500)
    pygame.display.update()
    


def draw_window(p1, p2, turn):
    # draw background
    WIN.blit(GAME_IMAGE, (0, 0))

    if turn == 2:
        turn_text = HEALTH_FONT.render("PLAYER 1's Turn", 1, WHITE)
    else:
        turn_text = HEALTH_FONT.render("PLAYER 2's Turn", 1, WHITE)

    WIN.blit(turn_text, ((300, 100)))
    # draw projectile
    p1.bullet.draw(WIN)
    p2.bullet.draw(WIN)
    draw_text("P1",HEALTH_FONT,WHITE,WIN,p1.x+5,p1.y-30)
    draw_text("P2",HEALTH_FONT,WHITE,WIN,p2.x+5,p2.y-30)
    # draw players
    p1.image.set_alpha(p1.alpha)
    p2.image.set_alpha(p2.alpha)
    p1img = p1.get_image(WIN)
    p2img = p2.get_image(WIN)
    #drawing is now handled by player objects

    # update each frame
    



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
    draw_text('A and D to move left and right || Mouse to aim and fire',HEALTH_FONT,WHITE, WIN, 120, 270)
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

def draw_shield_bar(surf, pct, pct2):
    if pct & pct2 < 0:
        pct = 0
        pct2 = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    x, y = 5, 5
    X, Y = (WIDTH - BAR_LENGTH), 5
    fill = (pct / 100) * BAR_LENGTH
    fill2 = (pct2 / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(X, Y, BAR_LENGTH, BAR_HEIGHT)
    outline_rect2 = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(X, Y, fill, BAR_HEIGHT)
    fill_rect2 = pygame.Rect(x, y, fill2, BAR_HEIGHT)
    if pct >= 60:
       pygame.draw.rect(surf, GREEN, fill_rect)
       pygame.draw.rect(surf, WHITE, outline_rect, 2)
    if pct2 >= 60:
       pygame.draw.rect(surf, GREEN, fill_rect2)
       pygame.draw.rect(surf, WHITE, outline_rect2, 2)
    if pct < 60:
       pygame.draw.rect(surf, ORANGE, fill_rect)
       pygame.draw.rect(surf, WHITE, outline_rect, 2)
    if pct2 < 60:
       pygame.draw.rect(surf, ORANGE, fill_rect2)
       pygame.draw.rect(surf, WHITE, outline_rect2, 2)

    #pygame.display.update()



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
        pygame.draw.rect(WIN, BLACK, game_start_button)
        pygame.draw.rect(WIN, BLACK, controls_button)
        pygame.draw.rect(WIN, BLACK, credits_button)

        draw_text('Start Game', HEALTH_FONT, WHITE, WIN, 80, 110)
        draw_text('Controls', HEALTH_FONT, WHITE, WIN, 100, 210)
        draw_text('Credits', HEALTH_FONT, WHITE, WIN, 110, 310)

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
                BUTTON_PRESS.play()
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

            p1img = hero_images.get(random.randint(0,4))
            p2img = hero_images.get(random.randint(5,9))
            if p1img[1] != None: # if there is a secondary image for the chosen model
                player1 = Player(100, 285, image = pygame.image.load(path.join(img_dir, p1img[0])), subimg = pygame.image.load(path.join(img_dir, p1img[1])))
            else:
                player1 = Player(100, 285, image = pygame.image.load(path.join(img_dir, p1img[0])))
            
            if p2img[1] != None:
                player2 = Player(700, 285, image = pygame.image.load(path.join(img_dir, p2img[0])), subimg = pygame.image.load(path.join(img_dir, p2img[1])), player2 = True)
            else:
                player2 = Player(700, 285, image = pygame.image.load(path.join(img_dir, p2img[0])), player2 = True)

          
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
            if active_player.bullet.y < 362 and not hit_registered:  # bullet is still within frame and hasn't hit anything yet
                active_player.bullet.advance_physics()
                #bullets now shoot from proper locations
                active_player.bullet.x, active_player.bullet.y = active_player.bullet.projectilePath(
                    active_player.x + active_player.width // 2, active_player.y + active_player.height // 2)
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
        # active_player.angle = findAngle(pos, active_player) * 57.29 #this is just converting radian output to
        active_player.calc_angle(pos)

        # invisible line determining the angle of the projectile
        line1 = [(active_player.x + 10, active_player.y + active_player.height // 2 - 2), pos]

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

                    x, y = active_player.new_bullet() #I'm assuming the return is for the camera follow?
                    active_player.bullet.fire(line1, pos)

            # not sure how these hit events are meant to happen; collision doesn't seem to work yet
            elif event.type == PLAYER1_HIT or event.type == PLAYER2_HIT:
                if not hit_registered:

                    dormant_player.hp -= 20

                    if not audio_compat:
                        random.choice(BULLET_HIT_SOUND).play()
                    expl = Explosion( dormant_player.rect.center, 'lg')
                    all_sprites.add(expl)
                    hit_registered = True

            #pygame.sprite.spritecollide(dormant_player, active_player.bullet, True)
    
            if active_player.hp <= 0:  # if active player's HP is 0, that means the other player killed them last turn 
               #simple formula to generate winning text instead of layers of conditionals
                if active_player == player1:
                    draw_winner("PLAYER 2 WINS!")
                   
                if active_player == player2:
                    draw_winner("PLAYER 1 WINS!")
                pygame.time.delay(2000)
                game_over=True


        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            active_player.move_left()
        elif pressed[pygame.K_d]:
            active_player.move_right()

        handle_bullets(active_player, dormant_player, player_1_turn)
        draw_window(player1, player2, int(player_1_turn) + 1)
        draw_shield_bar(WIN, player2.hp, player1.hp)
        draw_text('PLAYER 1', HEALTH_FONT, WHITE, WIN, 10, 30)
        draw_text('PLAYER 2', HEALTH_FONT, WHITE, WIN, 765, 30)

       
        pygame.draw.rect(WIN, (255, 0, 0), player1.rect, -1)
        pygame.draw.rect(WIN, (255, 0, 0), player2.rect, -1)

        all_sprites.draw(WIN)
        pygame.display.update()

    pygame.quit()



def controls():
    running = True
    
    while running:
        WIN.blit(MAIN_IMAGE, (0,0))
        draw_text('GAME NAME', HEALTH_FONT, WHITE, WIN, 320, 100)
        draw_text('A and D to move left and right || Mouse to aim and fire', HEALTH_FONT, WHITE, WIN, 120, 400)
        #draw_text("Mouse to aim and fire",HEALTH_FONT,WHITE, WIN, 520, 400)
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
        draw_text('Premchand Jayachandran, 015326428', HEALTH_FONT, WHITE, WIN, 50, 300)
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
