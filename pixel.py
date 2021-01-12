import pygame

from colors import *

# square unit class
class Pixel:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_obstacle(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def paint_closed(self):
        self.color = RED

    def paint_open(self):
        self.color = GREEN

    def paint_obstacle(self):
        self.color = BLACK

    def paint_start(self):
        self.color = ORANGE

    def paint_end(self):
        self.color = TURQUOISE

    def paint_path(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass
    
    def __lt__(self, other):
        return False