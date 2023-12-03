import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
FPS = 100

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run Barry Run")

grid_width = WIDTH // GRID_SIZE
grid_height = HEIGHT // GRID_SIZE
grid = [[0] * grid_width for _ in range(grid_height)]

clock = pygame.time.Clock()
editing = True
running = False

while editing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            row = y // GRID_SIZE
            col = x // GRID_SIZE
            grid[row][col] = 1 - grid[row][col]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                editing = False

    screen.fill(WHITE)

    for row in range(grid_height):
        for col in range(grid_width):
            if grid[row][col] == 1:
                pygame.draw.rect(screen, GRAY, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()

running = True
block_x, block_y = 0, 0
target_x, target_y = 19, 19
block_speed = 2
path = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if block_x < target_x * GRID_SIZE:
        block_x += block_speed
    elif block_y < target_y * GRID_SIZE:
        block_y += block_speed

    row = block_y // GRID_SIZE
    col = block_x // GRID_SIZE
    if grid[row][col] == 1:
        if block_x < target_x * GRID_SIZE:
            block_y += block_speed
        elif block_y < target_y * GRID_SIZE:
            block_x += block_speed

    path.append((block_x, block_y))

    screen.fill(WHITE)

    for row in range(grid_height):
        for col in range(grid_width):
            if grid[row][col] == 1:
                pygame.draw.rect(screen, GRAY, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    for point in path:
        pygame.draw.rect(screen, GREEN, (point[0], point[1], GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, RED, (0, 0, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, GREEN, (target_x * GRID_SIZE, target_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, RED, (block_x, block_y, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()
    clock.tick(FPS)
