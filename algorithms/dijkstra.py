import heapq

import pygame

from utils.pygame_utils import reconstruct_path


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
