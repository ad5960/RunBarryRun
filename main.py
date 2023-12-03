import pygame
import sys

pygame.init()

# Get user inputs for game settings
WIDTH = int(input("Enter the width of the window: "))
HEIGHT = int(input("Enter the height of the window: "))
FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

GRID_SIZE = 30
grid_width = WIDTH // GRID_SIZE
grid_height = HEIGHT // GRID_SIZE
grid = [[0] * grid_width for _ in range(grid_height)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run Barry Run")

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
editing = True
running = False

start_pos = None
end_pos = None

while editing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            col = x // GRID_SIZE
            row = y // GRID_SIZE
            if start_pos is None:
                start_pos = (col, row)
            elif end_pos is None and (col, row) != start_pos:
                end_pos = (col, row)
            else:
                grid[row][col] = 1 - grid[row][col]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start_pos is not None and end_pos is not None:
                editing = False

    screen.fill(WHITE)

    for row in range(grid_height):
        for col in range(grid_width):
            if grid[row][col] == 1:
                pygame.draw.rect(screen, GRAY, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    if start_pos is not None:
        pygame.draw.rect(screen, RED, (start_pos[0] * GRID_SIZE, start_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    else:
        start_text = font.render("Click to set start position", True, (0, 0, 0))
        screen.blit(start_text, (10, 10))

    if end_pos is not None:
        pygame.draw.rect(screen, GREEN, (end_pos[0] * GRID_SIZE, end_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    else:
        end_text = font.render("Click to set end position", True, (0, 0, 0))
        screen.blit(end_text, (10, 40))

    edit_text = font.render("Click anywhere else to create obstacles", True, (0, 0, 0))
    screen.blit(edit_text, (10, 70))

    game_text = font.render("Press SPACE to start simulation", True, (0, 0, 0))
    screen.blit(game_text, (10, 100))

    pygame.display.flip()

running = True
block_x, block_y = start_pos[0] * GRID_SIZE, start_pos[1] * GRID_SIZE
target_x, target_y = end_pos
block_speed = 1
counter = 0
movement_speed = 0.1
path = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            col = x // GRID_SIZE
            row = y // GRID_SIZE
            grid[row][col] = 1 - grid[row][col]

    if block_x == target_x * GRID_SIZE and block_y == target_y * GRID_SIZE:
        running = False

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        next_x, next_y = block_x + dx * block_speed * GRID_SIZE, block_y + dy * block_speed * GRID_SIZE
        next_col, next_row = next_x // GRID_SIZE, next_y // GRID_SIZE

        if 0 <= next_col < grid_width and 0 <= next_row < grid_height and not grid[next_row][next_col]:
            counter += movement_speed
            if counter >= 1:
                block_x, block_y = next_x, next_y
                counter = 0
            break

    path.append((block_x, block_y))

    screen.fill(WHITE)

    for row in range(grid_height):
        for col in range(grid_width):
            if grid[row][col] == 1:
                pygame.draw.rect(screen, GRAY, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    for point in path:
        pygame.draw.rect(screen, GREEN, (point[0], point[1], GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, RED, (start_pos[0] * GRID_SIZE, start_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, GREEN, (end_pos[0] * GRID_SIZE, end_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, RED, (block_x, block_y, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()
    clock.tick(FPS)