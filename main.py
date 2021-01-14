import pygame

from grid import Visualizer

WIDTH = 800
TITLE = 'A* Visualizer'

if __name__ == '__main__':
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption(TITLE)

    Visualizer(WIN, WIDTH)
