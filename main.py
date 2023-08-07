import pygame
from pygame import mixer
from fighter import Fighter

# initialize mixer
mixer.init()

# initialize pygame
pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set display name of window
pygame.display.set_caption("Mortal Kombat")

# set frame rate
clock = pygame.time.Clock()
FPS = 60

# define colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] # [P1, P2]
round_over = False
round_over_time = 0
ROUND_OVER_COOLDOWN = 2000

# define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 65]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 116]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# load bg image
bg_image = pygame.image.load("Images/bg_image.jpg").convert_alpha()

# load spritesheets
warrior_sheet = pygame.image.load("Images/warrior/warrior_spritesheet.png").convert_alpha()
wizard_sheet = pygame.image.load("Images/wizard/wizard_spritesheet.png").convert_alpha()

# define number of steps in each animation
WARRIOR_ANIMATION_STEP = [7, 7, 7, 3, 10, 3, 8, 3]
WIZARD_ANIMATION_STEP = [8, 8, 7, 2, 8, 2, 8, 3]

# define font
count_font = pygame.font.Font("fonts/turok/Turok.ttf", 80)
score_font = pygame.font.Font("fonts/turok/Turok.ttf", 30)
victory_font = pygame.font.Font("fonts/turok/Turok.ttf", 90)

# function for drawing text
def draw_text(text, font, text_color, x, y):
    # take text and turn into image
    img = font.render(text, True, text_color)
    # blit the image onto the screen 
    screen.blit(img, (x, y))

# function for drawing bg
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# function for drawing health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 1, y - 1, 402, 32))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# instance of Fighter class
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEP)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEP)

# game loop
running = True
while running:

    clock.tick(FPS)

    # draw bg
    draw_bg()

    # draw player stats
    draw_health_bar(fighter_1._health, 20, 20)
    draw_health_bar(fighter_2._health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    # update countdown
    if intro_count <= 0:
        # move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        # display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        # update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # update fighters 
    fighter_1.update()
    fighter_2.update()

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # check for player defeat
    if round_over == False:
        if fighter_1._alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2._alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # display victory 
        draw_text("Victory", victory_font, RED, 370, 150)
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEP)
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEP)

    # check to see if the user clicked the window close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update display (take all of the changes and update display with them)
    pygame.display.update()

# exit game
pygame.quit()