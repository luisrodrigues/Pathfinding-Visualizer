import pygame
import math
from queue import PriorityQueue

from colors import *
from pixel import Pixel

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Visualizer')

# square grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            pixel = Pixel(i, j, gap, rows)
            grid[i].append(pixel)
    
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# main draw function
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for pixel in row:
            pixel.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

# handle clicks
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos

    row = x // gap
    col = y // gap

    return row, col

# main loop
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    
    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue

            if pygame.mouse.get_pressed()[0]: # left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                pixel = grid[row][col]

                if not start:
                    start = pixel
                    start.paint_start()
                elif not end:
                    end = pixel
                    end.paint_end()
                elif pixel != end and pixel != start:
                    pixel.paint_obstacle()
            elif pygame.mouse.get_pressed()[2]: # right mouse button
                pass
    
    pygame.quit()

main(WIN, WIDTH)
