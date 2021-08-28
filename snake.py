import pygame
import random
import time
import os

pygame.font.init()
pygame.mixer.init()
pygame.init()

# size of snake
BLOCKSIZE = 30

HEIGHT = 600
WIDTH = 600

FPS = 8
CLOCK = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
VIOLET = (255, 0, 255)
CADETBLUE1 = (152, 245, 255)
CADETBLUE2 = (142, 229, 238)
LAVENDERBLUSH1 = (255, 240, 245)
LAVENDERBLUSH2 = (238, 224, 229)
BISQUE1 = (250, 220, 190)
BISQUE2 = (238, 213, 183)

# snake position
SNAKE_POS_X = BLOCKSIZE
SNAKE_POS_Y = BLOCKSIZE
SNAKE_POS_X_CHANGE = 0
SNAKE_POS_Y_CHANGE = 0

BANANA = pygame.image.load(
    os.path.join("graphics", "banana.png"))
BANANA = pygame.transform.scale(BANANA, (BLOCKSIZE, BLOCKSIZE))

CRUNCH = pygame.mixer.Sound(os.path.join(
    "sounds", "zapsplat_cartoon_bite_crunch_eat_13015.mp3"))


# food position
FOOD_POS_X = round(random.randrange(
    0, WIDTH - BLOCKSIZE) / BLOCKSIZE) * BLOCKSIZE
FOOD_POS_Y = round(random.randrange(
    0, HEIGHT - BLOCKSIZE) / BLOCKSIZE) * BLOCKSIZE

GAME_OVER_FONT = pygame.font.SysFont("comicsans", 100)
SCORE = pygame.font.SysFont("comicsans", 40)

RUN = True
SNAKE_LIST = []
LENGTH_OF_SNAKE = 1

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")


def draw_grid():
    # Die Iteration muss im Verhältnis zur Blockgrösse stehen
    for i in range(0, WIDTH // BLOCKSIZE):
        pygame.draw.line(SCREEN, (255, 255, 255),
                         (0, i * BLOCKSIZE), (WIDTH, i * BLOCKSIZE))
        pygame.draw.line(SCREEN, (255, 255, 255),
                         (i * BLOCKSIZE, 0), (i * BLOCKSIZE, HEIGHT))


def score(score):
    VALUE = SCORE.render("" + str(score), True, BLACK)
    SCREEN.blit(VALUE, (WIDTH / 2, 20))


# define the snake with a list
def snake(BLOCKSIZE, SNAKE_LIST):
    for x in SNAKE_LIST:
        pygame.draw.rect(SCREEN, RED, [x[0], x[1], BLOCKSIZE, BLOCKSIZE])


def game_over_message(text, color):
    game_over_text = GAME_OVER_FONT.render(text, 1, color)
    SCREEN.blit(game_over_text, (WIDTH/2 - game_over_text.get_width() /
                                 2, HEIGHT/2 - game_over_text.get_height()/2))
    pygame.display.update()


def food():
    FOOD_RECT = pygame.Rect(FOOD_POS_X, FOOD_POS_Y, BLOCKSIZE, BLOCKSIZE)
    SCREEN.blit(BANANA, FOOD_RECT)


def checkerboard():
    for x in range(0, WIDTH // BLOCKSIZE):
        if x % 2 == 0:
            for y in range(0, WIDTH // BLOCKSIZE):
                if y % 2 == 0:
                    pygame.draw.rect(
                        SCREEN, BISQUE1, [y * BLOCKSIZE, x * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE])
        else:
            for y in range(0, WIDTH // BLOCKSIZE):
                if y % 2 != 0:
                    pygame.draw.rect(
                        SCREEN, BISQUE1, [y * BLOCKSIZE, x * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE])


while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        # snake_movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                SNAKE_POS_X_CHANGE = 0
                SNAKE_POS_Y_CHANGE = -BLOCKSIZE
            elif event.key == pygame.K_DOWN:
                SNAKE_POS_X_CHANGE = 0
                SNAKE_POS_Y_CHANGE = BLOCKSIZE
            elif event.key == pygame.K_RIGHT:
                SNAKE_POS_X_CHANGE = BLOCKSIZE
                SNAKE_POS_Y_CHANGE = 0
            elif event.key == pygame.K_LEFT:
                SNAKE_POS_X_CHANGE = -BLOCKSIZE
                SNAKE_POS_Y_CHANGE = 0

    # Schlange darf den Bildschirm nicht verlassen -> game over!
    if SNAKE_POS_X >= WIDTH or SNAKE_POS_X < 0 or SNAKE_POS_Y >= HEIGHT or SNAKE_POS_Y < 0:
        RUN = False

    SNAKE_POS_X += SNAKE_POS_X_CHANGE
    SNAKE_POS_Y += SNAKE_POS_Y_CHANGE

    SCREEN.fill(BISQUE2)
    checkerboard()
    food()
    SNAKE_HEAD = []
    SNAKE_HEAD.append(SNAKE_POS_X)
    SNAKE_HEAD.append(SNAKE_POS_Y)
    SNAKE_LIST.append(SNAKE_HEAD)
    if len(SNAKE_LIST) > LENGTH_OF_SNAKE:
        del SNAKE_LIST[0]

    for x in SNAKE_LIST[:-1]:
        if x == SNAKE_HEAD:
            RUN = False

    snake(BLOCKSIZE, SNAKE_LIST)
    score(LENGTH_OF_SNAKE - 1)
    # draw_grid()
    CLOCK.tick(FPS)
    pygame.display.update()

    if SNAKE_POS_X == FOOD_POS_X and SNAKE_POS_Y == FOOD_POS_Y:
        FOOD_POS_X = round(random.randrange(
            0, WIDTH - BLOCKSIZE) / BLOCKSIZE) * BLOCKSIZE
        FOOD_POS_Y = round(random.randrange(
            0, HEIGHT - BLOCKSIZE) / BLOCKSIZE) * BLOCKSIZE
        LENGTH_OF_SNAKE += 1
        CRUNCH.play()

game_over_message("Game Over!", BLACK)
time.sleep(2)  # delay before closing game
pygame.quit()
