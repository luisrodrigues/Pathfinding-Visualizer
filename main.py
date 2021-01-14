import pygame
import math
from queue import PriorityQueue

from colors import *
from pixel import Pixel

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Visualizer')

# manhatthan distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# a* algorithm
def algorithm_astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {pixel: float("inf") for row in grid for pixel in row}
    g_score[start] = 0
    f_score = {pixel: float("inf") for row in grid for pixel in row}
    f_score[start] = h(start.get_position(), end.get_position())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            return True
        
        for n in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[n]:
                came_from[n] = current
                g_score[n] = temp_g_score
                f_score[n] = temp_g_score + h(n.get_position(), end.get_position())
                if n not in open_set_hash:
                    count += 1
                    open_set.put((f_score[n], count, n))
                    open_set_hash.add(n)
                    n.paint_open()
        
        draw()
        if current != start:
            current.paint_closed()

    return False 

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

                if not start and pixel != end:
                    start = pixel
                    start.paint_start()
                elif not end and pixel != start:
                    end = pixel
                    end.paint_end()
                elif pixel != end and pixel != start:
                    pixel.paint_obstacle()
            elif pygame.mouse.get_pressed()[2]: # right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                pixel = grid[row][col]
                pixel.reset()
                if pixel == start:
                    start = None
                if pixel == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for pixel in row:
                            pixel.update_neighbors(grid)
                    
                    algorithm_astar(lambda: draw(win, grid, ROWS, width), grid, start, end)
    
    pygame.quit()

main(WIN, WIDTH)
