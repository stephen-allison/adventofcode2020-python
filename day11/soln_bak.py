from itertools import product, count
from collections import defaultdict
from pprint import pprint

def get_grid():
    with open('input.txt', 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]
        return (grid, len(grid[0]), len(grid))

EMPTY = 'L'
OCCUPIED = '#'
FLOOR = '.'

DIFFS = [(-1, -1), (0, -1), (1, -1),
         (-1, 0),           (1, 0),
         (-1, 1),  (0, 1),  (1, 1)]

def lines_of_sight(x, y):
    def _n(x, y, dx, dy):
        for i in count(1):
            yield (x + i*dx, y + i*dy)
    return [_n(x, y, dx, dy) for dx, dy in DIFFS]


def map_neighbours(grid, grid_w, grid_h, found_function):
    neighbours_map = defaultdict(list)
    for y, x in product(range(grid_h), range(grid_w)):
        neighbours = []
        if cell_at(grid, x, y) == FLOOR:
            continue
        for los in lines_of_sight(x, y):
            for cell in los:
                if not in_bounds(cell, grid_w, grid_h):
                    break
                state = cell_at(grid, *cell)
                if found_function(state):
                    neighbours.append(cell)
                    break
        neighbours_map[(x,y)] = neighbours
    return neighbours_map


def in_bounds(point, grid_w, grid_h):
    x, y = point
    return (0 <= x < grid_w) and (0 <= y < grid_h)


def cell_at(grid, x, y):
    return grid[y][x]


def make_new_grid(w, h):
    new_grid = []
    for i in range(h):
        row = []
        for j in range(w):
            row.append('?')
        new_grid.append(row)
    return new_grid


def iterate(grid, grid_w, grid_h, neighbour_map, tolerance):
    new_grid = make_new_grid(grid_w, grid_h)
    for y, x in product(range(grid_h), range(grid_w)):
        n_locs = neighbour_map[(x,y)]
        n_states = [cell_at(grid, *loc) for loc in n_locs]

        occupied_neighbours = n_states.count(OCCUPIED)
        cell_state = next_state = grid[y][x]

        if cell_state == EMPTY and occupied_neighbours == 0:
            next_state = OCCUPIED
        elif cell_state == OCCUPIED and occupied_neighbours >= tolerance:
            next_state = EMPTY

        new_grid[y][x] = next_state
    return new_grid


def print_grid(grid):
    for row in grid:
        print(''.join(row))


def _solve(found_func, tolerance):
    grid, w, h = get_grid()
    grid_map = map_neighbours(grid, w, h, found_func)
    last_grid = None
    iters = 0
    while grid != last_grid:
        last_grid = grid
        grid = iterate2(last_grid, w, h, grid_map, tolerance)
        iters += 1
    occupied = sum([r.count(OCCUPIED) for r in grid])
    print(f'{occupied} seats are occupied after {iters} rounds')



def solve2():
    _solve(lambda s: s in (EMPTY, OCCUPIED), 5)


def solve1():
    _solve(lambda _: True, 4)


if __name__ == '__main__':
    solve1()
    solve2()
