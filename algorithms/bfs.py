import pygame

from utils.pygame_utils import reconstruct_path


def bfs(draw_spot, grid, start, end):
    queue = [start]
    came_from = {start: None}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.pop(0)

        if current == end:
            reconstruct_path(came_from, end, draw_spot)
            return True

        for neighbor in current.neighbors:
            if neighbor not in came_from and not neighbor.is_barrier():
                queue.append(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()

        draw_spot()

        if current != start:
            current.make_closed()

    return False
