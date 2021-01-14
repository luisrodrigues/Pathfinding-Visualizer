import pygame
import math
from queue import PriorityQueue

# a* algorithm
def a_star(draw, grid, start, end):
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
            reconstruct_path(came_from, end, draw)
            end.paint_end() 
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

# draw optimal path
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.paint_path()
        draw() 

# manhatthan distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)