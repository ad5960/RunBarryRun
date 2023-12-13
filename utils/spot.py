import pygame

from constants.colors import WHITE, GREY, GREEN, BLACK, ORANGE, PURPLE, TURQUOISE
from constants.load_assets import SEARCH_STILL_IMAGE, OBSTACLE_STILL_IMAGE, FINISH_STILL_IMAGE, FLASH_IMAGE, \
    FLASH_STILL_IMAGE
from constants.window_config import SLOT_SIZE


# Model representation of an individual spot on the grid
class Spot:
    def __init__(self, row, col, total_rows, total_columns):
        self.row = row
        self.col = col
        self.x = row * SLOT_SIZE
        self.y = col * SLOT_SIZE
        self.color = WHITE
        self.neighbors = []
        self.total_rows = total_rows
        self.total_columns = total_columns

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
        self.image = SEARCH_STILL_IMAGE

    def make_open(self):
        self.color = WHITE

    def make_barrier(self):
        self.color = BLACK
        self.image = OBSTACLE_STILL_IMAGE

    def make_end(self):
        self.color = TURQUOISE
        self.image = FINISH_STILL_IMAGE

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

        if self.col < self.total_columns - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
