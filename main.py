import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
FPS = 100

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run Barry Run")

block_x, block_y = 0, 0
target_x, target_y = 19, 19
block_speed = 2

path = []

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if block_x < target_x * GRID_SIZE:
        block_x += block_speed
    elif block_y < target_y * GRID_SIZE:
        block_y += block_speed

    path.append((block_x, block_y))

    screen.fill(WHITE)

    for point in path:
        pygame.draw.rect(screen, GREEN, (point[0], point[1], GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, RED, (0, 0, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, GREEN, (target_x * GRID_SIZE, target_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, RED, (block_x, block_y, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()
    clock.tick(FPS)
