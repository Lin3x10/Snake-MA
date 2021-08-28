import pygame
import random
import time
pygame.font.init()

pygame.init()

# size of snake
BLOCKSIZE = 30

# display variables
HEIGHT = 600
WIDTH = 600

# frames
FPS = 8
CLOCK = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# snake position
SNAKE_POS_X = BLOCKSIZE
SNAKE_POS_Y = BLOCKSIZE
SNAKE_POS_X_CHANGE = 0
SNAKE_POS_Y_CHANGE = 0

# food position
FOOD_POS_X = round(random.randrange(
    0, WIDTH - BLOCKSIZE) / BLOCKSIZE) * BLOCKSIZE
FOOD_POS_Y = round(random.randrange(
    0, HEIGHT - BLOCKSIZE) / BLOCKSIZE) * BLOCKSIZE

# fonts
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 100)

RUN = True
SNAKE_LIST = []
LENGHT_OF_SNAKE = 1

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")


def draw_grid():
    # Die Iteration muss im Verhältnis zur Blockgrösse stehen
    for i in range(0, WIDTH // BLOCKSIZE):
        pygame.draw.line(SCREEN, (255, 255, 255),
                         (0, i * BLOCKSIZE), (WIDTH, i * BLOCKSIZE))
        pygame.draw.line(SCREEN, (255, 255, 255),
                         (i * BLOCKSIZE, 0), (i * BLOCKSIZE, HEIGHT))

# define the snake with a list


def snake(BLOCKSIZE, SNAKE_LIST):

    for x in SNAKE_LIST:
        pygame.draw.rect(SCREEN, RED, [x[0], x[1], BLOCKSIZE, BLOCKSIZE])

# def game_over():


def game_over_message(text, color):

    game_over_text = GAME_OVER_FONT.render(text, 1, color)
    SCREEN.blit(game_over_text, (WIDTH/2 - game_over_text.get_width() /
                                 2, HEIGHT/2 - game_over_text.get_height()/2))
    pygame.display.update()

# def food():


def food():
    pygame.draw.rect(
        SCREEN, GREEN, [FOOD_POS_X, FOOD_POS_Y, BLOCKSIZE, BLOCKSIZE])


def main():
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

        SCREEN.fill(BLACK)
        food()
        SNAKE_HEAD = []
        SNAKE_HEAD.append(SNAKE_POS_X)
        SNAKE_HEAD.append(SNAKE_POS_Y)
        SNAKE_LIST.append(SNAKE_HEAD)
        if len(SNAKE_LIST) > LENGHT_OF_SNAKE:
            del SNAKE_LIST[0]

        for x in SNAKE_LIST[:-1]:
            if x == SNAKE_HEAD:
                RUN = False

        snake(BLOCKSIZE, SNAKE_LIST)

        draw_grid()
        CLOCK.tick(FPS)
        pygame.display.update()

        if SNAKE_POS_X == FOOD_POS_X and SNAKE_POS_Y == FOOD_POS_Y:
            FOOD_POS_X = round(random.randrange(
                0, WIDTH - BLOCKSIZE) / BLOCKSIZE) * BLOCKSIZE
            FOOD_POS_Y = round(random.randrange(
                0, HEIGHT - BLOCKSIZE) / BLOCKSIZE) * BLOCKSIZE
            LENGHT_OF_SNAKE += 1

    game_over_message("Game Over!", WHITE)
    time.sleep(2)  # delay before closing game
    pygame.quit()


main()
