import pygame
import time
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

FPS = 5

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

snake_pos = [300, 200]
snake_body = [[300, 200], [280, 200], [260, 200]]
direction = 'RIGHT'

food_pos = [random.randrange(1, (WIDTH // CELL_SIZE)) * CELL_SIZE,
            random.randrange(1, (HEIGHT // CELL_SIZE)) * CELL_SIZE]

game_over = False


def draw_snake(snake_body):
    for pos in snake_body:
        pygame.draw.rect(win, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

def draw_food(food_pos):
    pygame.draw.rect(win, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

def move_snake(direction, snake_body):
    if direction == 'UP':
        snake_pos[1] -= CELL_SIZE
    if direction == 'DOWN':
        snake_pos[1] += CELL_SIZE
    if direction == 'LEFT':
        snake_pos[0] -= CELL_SIZE
    if direction == 'RIGHT':
        snake_pos[0] += CELL_SIZE

    snake_body.insert(0, list(snake_pos))

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    move_snake(direction, snake_body)

    if snake_pos[0] < 0:
        snake_pos[0] = WIDTH - CELL_SIZE
    elif snake_pos[0] >= WIDTH:
        snake_pos[0] = 0
    elif snake_pos[1] < 0:
        snake_pos[1] = HEIGHT - CELL_SIZE
    elif snake_pos[1] >= HEIGHT:
        snake_pos[1] = 0

    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        food_pos = [random.randrange(1, (WIDTH // CELL_SIZE)) * CELL_SIZE,
                    random.randrange(1, (HEIGHT // CELL_SIZE)) * CELL_SIZE]
    else:
        snake_body.pop()

    if snake_pos in snake_body[1:]:
        game_over = True

    win.fill(BLACK)

    draw_snake(snake_body)
    draw_food(food_pos)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
