import os

import pygame

SLOT_SIZE = 24
WIDTH = 1980
ROWS = WIDTH // SLOT_SIZE

FLASH_ASSET_PATH = os.path.join(os.path.dirname(__file__), "flash_asset.png")
FLASH_STILL_ASSET_PATH = os.path.join(os.path.dirname(__file__), "flash_still.png")

FLASH_IMAGE = pygame.image.load(FLASH_ASSET_PATH)
FLASH_IMAGE = pygame.transform.scale(FLASH_IMAGE, (SLOT_SIZE, SLOT_SIZE))

FLASH_STILL_IMAGE = pygame.image.load(FLASH_STILL_ASSET_PATH)
FLASH_STILL_IMAGE = pygame.transform.scale(FLASH_STILL_IMAGE, (SLOT_SIZE, SLOT_SIZE))

WIN = pygame.display.set_mode((WIDTH, 1080))
pygame.display.set_caption("DFS Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, total_rows):
        self.row = row
        self.col = col
        self.x = row * SLOT_SIZE
        self.y = col * SLOT_SIZE
        self.color = WHITE
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == GREY

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = GREY

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE
        self.image = FLASH_IMAGE

    def make_start(self):
        self.color = ORANGE
        self.image = FLASH_STILL_IMAGE

    def draw_spot(self, win):
        if hasattr(self, 'image'):  # Check if the spot has an image attribute
            win.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, SLOT_SIZE, SLOT_SIZE))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def reconstruct_path(came_from, current, draw):
    while current and current in came_from:
        current = came_from[current]
        if current:
            current.make_path()
            draw()


def dfs(draw_spot, grid, start, end):
    stack = [start]
    came_from = {start: None}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            reconstruct_path(came_from, end, draw_spot)
            return True

        for neighbor in current.neighbors:
            if neighbor not in came_from and not neighbor.is_barrier():
                stack.append(neighbor)
                came_from[neighbor] = current
                neighbor.make_closed()

        draw_spot()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows):
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * SLOT_SIZE), (WIDTH, i * SLOT_SIZE))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * SLOT_SIZE, 0), (j * SLOT_SIZE, WIDTH))


def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw_spot(win)

    pygame.display.update()


def get_clicked_pos(pos):
    y, x = pos
    row = y // SLOT_SIZE
    col = x // SLOT_SIZE
    return row, col


def main(win):
    grid = make_grid(ROWS)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    dfs(lambda: draw(win, grid), grid, start, end)
                elif event.key == pygame.K_ESCAPE:
                    for row in grid:
                        for spot in row:
                            spot.reset()
                    start = end = None

    pygame.quit()


main(WIN)
