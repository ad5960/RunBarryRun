import heapq

import pygame

from utils.pygame_utils import reconstruct_path


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