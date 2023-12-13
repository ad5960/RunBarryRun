import pygame

from algorithms.astar import a_star
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra
from constants.window_config import WIDTH, WINDOW_TITLE, ROWS, COLUMNS, HEIGHT
from utils.pygame_utils import make_grid, draw, get_clicked_pos

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)


def main(win):
    pygame.font.init()
    grid = make_grid(ROWS + 1, COLUMNS + 1)

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
                        bfs(lambda: draw(win, grid, algorithm_choice), grid, start, end)
                    elif algorithm_choice == 3:
                        a_star(lambda: draw(win, grid, algorithm_choice), grid, start, end)
                    elif algorithm_choice == 4:
                        dijkstra(lambda: draw(win, grid, algorithm_choice), grid, start, end)
                elif event.key == pygame.K_ESCAPE:
                    main(WIN)
                    start = end = None
                elif event.key == pygame.K_1:
                    algorithm_choice = 1
                elif event.key == pygame.K_2:
                    algorithm_choice = 2
                elif event.key == pygame.K_3:
                    algorithm_choice = 3
                elif event.key == pygame.K_4:
                    algorithm_choice = 4

    pygame.quit()


if __name__ == "__main__":
    main(WIN)
