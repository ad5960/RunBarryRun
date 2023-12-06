import os

import pygame
import heapq

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


def draw(win, grid, algorithm_chosen):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw_spot(win)
    if not algorithm_chosen:
        draw_menu(win, algorithm_chosen)

    pygame.display.update()


def get_clicked_pos(pos):
    y, x = pos
    row = y // SLOT_SIZE
    col = x // SLOT_SIZE
    return row, col


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(draw_spot, grid, start, end):
    count = 0
    open_set = [(heuristic(start.get_pos(), end.get_pos()), count, start)]
    came_from = {start: None}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heapq.heappop(open_set)[2]

        if current == end:
            reconstruct_path(came_from, end, draw_spot)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                heapq.heappush(open_set, (f_score, count, neighbor))
                if neighbor != end:
                    neighbor.make_open()

        draw_spot()

        if current != start:
            current.make_closed()

    return False


def dijkstra(draw_spot, grid, start, end):
    heap = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while heap:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_cost, current = heapq.heappop(heap)

        if current == end:
            reconstruct_path(came_from, end, draw_spot)
            return True

        for neighbor in current.neighbors:
            new_cost = cost_so_far[current] + 1

            if new_cost < cost_so_far.get(neighbor, float('inf')):
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                heapq.heappush(heap, (priority, neighbor))
                came_from[neighbor] = current
                if neighbor != end:
                    neighbor.make_open()

        draw_spot()

        if current != start:
            current.make_closed()

    return False


def draw_menu(win, algorithm_chosen):
    if not algorithm_chosen:
        font = pygame.font.Font(None, 36)
        text_dfs = font.render("Press 1 for DFS", True, BLACK)
        text_astar = font.render("Press 2 for A*", True, BLACK)
        text_dijkstra = font.render("Press 3 for Dijkstra's Algorithm", True, BLACK)

        win.blit(text_dfs, (10, 10))
        win.blit(text_astar, (10, 50))
        win.blit(text_dijkstra, (10, 90))


def main(win):
    pygame.font.init()
    grid = make_grid(ROWS)

    start = None
    end = None
    algorithm_choice = None

    run = True
    started = False

    while run:
        draw(win, grid, algorithm_choice)
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
                if event.key == pygame.K_SPACE and not started and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    if algorithm_choice == 1:
                        dfs(lambda: draw(win, grid, algorithm_choice), grid, start, end)
                    elif algorithm_choice == 2:
                        a_star(lambda: draw(win, grid, algorithm_choice), grid, start, end)
                    elif algorithm_choice == 3:
                        dijkstra(lambda: draw(win, grid, algorithm_choice), grid, start, end)
                elif event.key == pygame.K_ESCAPE:
                    for row in grid:
                        for spot in row:
                            spot.reset()
                    start = end = None
                elif event.key == pygame.K_1:
                    algorithm_choice = 1
                elif event.key == pygame.K_2:
                    algorithm_choice = 2
                elif event.key == pygame.K_3:
                    algorithm_choice = 3

    pygame.quit()


main(WIN)
