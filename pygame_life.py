"""
    Pygame of life module. Contains the short engine
    to simluate the grid of life.
"""

import sys
import time
from collections import defaultdict
from copy import deepcopy

import pygame

from example_grids import SIMPLE, GOSPER_GLIDER
from grid_defs import Dim, Grid, Neighbours


def get_neighbours(grid: Grid, x: int, y: int) -> Neighbours:
    """
        Gets the neighbour states for a particular cell in
        (x, y) on the grid.
    """
    offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    possible_neighbours = {(x + x_add, y + y_add) for x_add, y_add in offsets}
    alive = {(pos[0], pos[1]) for pos in possible_neighbours if pos in grid.cells}
    return Neighbours(alive, possible_neighbours - alive)


def update_grid(grid: Grid) -> Grid:
    """
        Given a grid, this function returns the next iteration
        of the game of life.
    """
    new_cells = deepcopy(grid.cells)
    undead = defaultdict(int)

    for x, y in grid.cells:
        alive_neighbours, dead_neighbours = get_neighbours(grid, x, y)
        if len(alive_neighbours) not in [2, 3]:
            new_cells.remove((x, y))

        for pos in dead_neighbours:
            undead[pos] += 1

    for pos, _ in filter(lambda elem: elem[1] == 3, undead.items()):
        new_cells.add((pos[0], pos[1]))

    return Grid(grid.dim, new_cells)


def draw_grid(screen: pygame.Surface, grid: Grid) -> None:
    """
        This function draws the game of life on the given
        pygame.Surface object.
    """
    cell_width = screen.get_width() / grid.dim.width
    cell_height = screen.get_height() / grid.dim.height
    border_size = 2

    for x, y in grid.cells:
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (
                x * cell_width + border_size,
                y * cell_height + border_size,
                cell_width - border_size,
                cell_height - border_size,
            ),
        )


def convert_to_list(grid):
    """
        This function converts to a 2D array grid format from a set of alive cells format
    """
    new_grid = [deepcopy([False] * grid.dim.width) for _ in range(grid.dim.height)]
    for x,y in grid.cells:
        new_grid[y][x] = True
    
    return new_grid


def convert_to_set(grid):
    """
        This function converts to a set of alive cells format from 2D array grid format
    """
    new_grid = Grid(Dim(len(grid), len(grid[0])), set())
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col]:
                new_grid.cells.add((row, col))
    
    return new_grid


def main():
    """
        Main entry point
    """
    grid = GOSPER_GLIDER
    running_title = 'Game of Life (running)'
    paused_title = 'Game of Life (paused)'

    input_repeat_interval = 30
    input_repeat_delay = 200

    pygame.init()
    pygame.key.set_repeat(input_repeat_delay, input_repeat_interval)
    mon_height = pygame.display.Info().current_h
    mon_width = pygame.display.Info().current_w

    screen_percent = 0.88
    
    if mon_height < mon_width:
        screen_height = mon_height * screen_percent
        screen_width = screen_height * grid.dim.width / grid.dim.height
    else:
        screen_width = mon_width * screen_percent
        screen_height = screen_width * grid.dim.height / grid.dim.width


    screen = pygame.display.set_mode((screen_width, screen_height))
    running = True
    pygame.display.set_caption(running_title if running else paused_title)
    cell_width = screen.get_width() / grid.dim.width
    cell_height = screen.get_height() / grid.dim.height
    last_cell_edited = None

    update_speed = 0.1
    speed_change_factor = 1.1
    last_update_time = time.time()

    while True:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    pygame.display.set_caption(running_title if running else paused_title)
                if event.key == pygame.K_c:
                    grid.cells.clear()
                if event.key == pygame.K_UP:
                    update_speed /= speed_change_factor
                if event.key == pygame.K_DOWN:
                    update_speed *= speed_change_factor
                if event.key == pygame.K_RIGHT and not running:
                    grid = update_grid(grid)
                            
            mouse_press = pygame.mouse.get_pressed()
            if any(mouse_press):
                pos = pygame.mouse.get_pos()
                col = int(pos[0] // cell_width)
                row = int(pos[1] // cell_height)
                cell = (col, row)
                if 0 <= col < grid.dim.width and 0 <= row < grid.dim.height and last_cell_edited != cell:
                    if mouse_press[1]:
                        if cell in grid.cells:
                            grid.cells.discard(cell)
                        else:
                            grid.cells.add(cell)
                    elif mouse_press[0]:
                        grid.cells.add(cell)
                    elif mouse_press[2]:
                        grid.cells.discard(cell)

                    last_cell_edited = cell
            else:
                last_cell_edited = None
    

        screen.fill((0, 0, 0))
        draw_grid(screen, grid)
        pygame.display.flip()
        now = time.time()
        if running and now - last_update_time > update_speed:
            last_update_time = now
            grid = update_grid(grid)
        
if __name__ == "__main__":
    main()
