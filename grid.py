import pygame

from colors import *

from pixel import Pixel

from algorithms import a_star

def Visualizer(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    # start and end nodes
    start = None
    end = None
    
    run = True

    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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
                if event.key == pygame.K_SPACE and start and end: # start algorithm
                    for row in grid:
                        for pixel in row:
                            pixel.update_neighbors(grid)
                    
                    a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:                     # clear grid
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()

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