import pygame

from utils.pygame_utils import reconstruct_path


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
