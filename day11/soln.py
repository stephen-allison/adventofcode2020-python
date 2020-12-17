from itertools import product, count, takewhile
from collections import defaultdict


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


class Grid:

    @staticmethod
    def load():
        with open('input.txt', 'r') as f:
            grid = [list(line.strip()) for line in f.readlines()]
            return Grid(grid)

    def __init__(self, grid, neighbours_map = None):
        self._grid = grid
        self.w = len(grid[0])
        self.h = len(grid)
        self.neighbours_map = neighbours_map

    def in_bounds(self, x, y):
        return (0 <= x < self.w) and (0 <= y < self.h)

    def state_at(self, x, y):
        return self._grid[y][x]

    def map_neighbours(self, found_neighbour):
        self.neighbours_map = defaultdict(list)
        for x, y, state in self:
            neighbours = []
            if state == FLOOR:
                continue
            for los in lines_of_sight(x, y):
                for cell in takewhile(lambda p: self.in_bounds(*p), los):
                    if found_neighbour(self.state_at(*cell)):
                        neighbours.append(cell)
                        break
            self.neighbours_map[(x,y)] = neighbours

    def fresh(self):
        new_grid = [['?' for x in range(self.w)] for y in range(self.h)]
        return Grid(new_grid, self.neighbours_map)

    def set_state(self, x, y, state):
        self._grid[y][x] = state

    def neighbour_states(self, x, y):
        return [self.state_at(*n) for n in self.neighbours_map[(x, y)]]

    def __iter__(self):
        for y, x in product(range(self.h), range(self.w)):
            yield (x, y, self.state_at(x, y))

    def __eq__(self, other):
        if not other:
            return False
        return self._grid == other._grid


def iterate(grid, tolerance):
    new_grid = grid.fresh()
    for x, y, cell_state in grid:
        occupied_neighbours = grid.neighbour_states(x, y).count(OCCUPIED)
        next_state = cell_state
        if cell_state == EMPTY and occupied_neighbours == 0:
            next_state = OCCUPIED
        elif cell_state == OCCUPIED and occupied_neighbours >= tolerance:
            next_state = EMPTY
        new_grid.set_state(x, y, next_state)
    return new_grid


def _solve(found_neighbour, tolerance):
    grid = Grid.load()
    grid.map_neighbours(found_neighbour)
    last_grid = None
    iters = 0
    while grid != last_grid:
        last_grid = grid
        grid = iterate(last_grid, tolerance)
        iters += 1
    occupied = sum([s == OCCUPIED for _, _, s in grid])
    print(f'{occupied} seats are occupied after {iters} rounds')


def solve2():
    _solve(lambda s: s in (EMPTY, OCCUPIED), 5)


def solve1():
    _solve(lambda _: True, 4)


if __name__ == '__main__':
    solve1()
    solve2()
