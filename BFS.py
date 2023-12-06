import pygame

# Initialize Pygame
pygame.init()

# Grid settings
grid_size = 600
window_size = (grid_size, grid_size)
cell_size = 50
num_cells = grid_size // cell_size

# Create the window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Grid Game with BFS and Obstacles")

# States
PLACING_START = 0
PLACING_END = 1
GAME_RUNNING = 2
GAME_FINISHED = 3

# Initialize state and positions
current_state = PLACING_START
start_pos = None
end_pos = None
character_pos = None
path = []
obstacles = set()

def draw_grid():
    for x in range(0, grid_size, cell_size):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, grid_size))
    for y in range(0, grid_size, cell_size):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (grid_size, y))

def draw_positions():
    for obstacle in obstacles:
        pygame.draw.rect(screen, (128, 128, 128), (obstacle[0]*cell_size, obstacle[1]*cell_size, cell_size, cell_size))
    if start_pos:
        pygame.draw.rect(screen, (0, 255, 0), (start_pos[0]*cell_size, start_pos[1]*cell_size, cell_size, cell_size))
    if end_pos:
        pygame.draw.rect(screen, (0, 0, 255), (end_pos[0]*cell_size, end_pos[1]*cell_size, cell_size, cell_size))
    if character_pos:
        pygame.draw.rect(screen, (255, 0, 0), (character_pos[0]*cell_size, character_pos[1]*cell_size, cell_size, cell_size))

def get_grid_position(mouse_pos):
    x, y = mouse_pos
    return x // cell_size, y // cell_size

def bfs(start, end, obstacles):
    if start in obstacles or end in obstacles:
        return []  # No path if start or end is an obstacle
    queue = [(start, [start])]
    visited = set()

    while queue:
        current, path = queue.pop(0)
        if current == end:
            return path

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)
            if 0 <= next_pos[0] < num_cells and 0 <= next_pos[1] < num_cells and next_pos not in visited and next_pos not in obstacles:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))

    return []

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            grid_pos = get_grid_position(mouse_pos)

            if event.button == 1:  # Left click
                if current_state == PLACING_START:
                    start_pos = grid_pos
                    current_state = PLACING_END
                elif current_state == PLACING_END:
                    end_pos = grid_pos
                    path = bfs(start_pos, end_pos, obstacles)
                    if path:
                        character_pos = start_pos
                        current_state = GAME_RUNNING
                    else:
                        print("No path found")
            elif event.button == 3:  # Right click to place an obstacle
                obstacles.add(grid_pos)
                if current_state == GAME_RUNNING:
                    path = bfs(start_pos, end_pos, obstacles)
                    if path:
                        character_pos = start_pos
                    else:
                        print("No path found")

    screen.fill((0, 0, 0))
    draw_grid()
    draw_positions()

    if current_state == GAME_RUNNING:
        if path:
            character_pos = path.pop(0)
            if character_pos == end_pos:
                current_state = GAME_FINISHED
        pygame.time.delay(100)

    pygame.display.flip()

pygame.quit()
