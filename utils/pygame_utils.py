import pygame

from constants.colors import BLACK, GREY, WHITE
from constants.window_config import SLOT_SIZE, WIDTH
from utils.spot import Spot


# This file contains functions for drawing and interaction
# with the grid as well as visualization of pathfinding algorithms in a pyGame window


# Reconstruct the path and visualize it on the grid
def reconstruct_path(came_from, current, draw):
    while current and current in came_from:
        current = came_from[current]
        if current:
            current.make_path()
            draw()
            pygame.time.Clock().tick(60)


# Draw the menu on the pyGame window
def draw_menu(win, algorithm_chosen):
    if not algorithm_chosen:
        font = pygame.font.Font(None, 36)
        text_dfs = font.render("Press 1 for DFS", True, BLACK)
        text_bfs = font.render("Press 2 for BFS", True, BLACK)
        text_astar = font.render("Press 3 for A*", True, BLACK)
        text_dijkstra = font.render("Press 4 for Dijkstra's Algorithm", True, BLACK)

        win.blit(text_dfs, (10, 10))
        win.blit(text_bfs, (10, 50))
        win.blit(text_astar, (10, 90))
        win.blit(text_dijkstra, (10, 120))


# Create a grid of Spot instances
def make_grid(rows, columns):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(columns):
            spot = Spot(i, j, rows, columns)
            grid[i].append(spot)
    return grid


# Draw grid lines on the pyGame window
def draw_grid(win, rows):
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * SLOT_SIZE), (WIDTH, i * SLOT_SIZE))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * SLOT_SIZE, 0), (j * SLOT_SIZE, WIDTH))


# Draw the pyGame grid and menu window
def draw(win, grid, algorithm_chosen):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw_spot(win)
    if not algorithm_chosen:
        draw_menu(win, algorithm_chosen)

    pygame.display.update()


# Get grid positions and calculate row's and column
def get_clicked_pos(pos):
    y, x = pos
    row = y // SLOT_SIZE
    col = x // SLOT_SIZE
    return row, col
