from collections import Counter, defaultdict
from itertools import chain, cycle, product
from pprint import pprint

def log(*args):
    print(*args)

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

def load_tiles():
    tiles = []
    tile_lines = []
    tile_name = None
    grid = Grid(12)
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                tiles.append(Tile(tile_name, tile_lines, grid))
            elif line.startswith('Tile'):
                tile_name = line
                tile_lines = []
            else:
                tile_lines.append(line)
    log(f'Loaded {len(tiles)} tiles')
    return tiles, grid


class Grid:
    def __init__(self, side):
        self.side = side
        self.contents = {}

    def add_tile(self, tile):
        if tile.grid_pos in self.contents:
            if self.contents[tile.grid_pos] != tile:
                log('*******************')
                log(f'adding {tile.name} but')
                log(f'{tile.grid_pos} taken by {self.contents[tile.grid_pos].name}')
                log('*******************')
                raise Exception('tile taken')
        self.contents[tile.grid_pos] = tile

    def try_tile(self, tile, x, y):
        if x == y == 0:
            tile.match_orientation((True, False, False, True))

        neighbours = [self.contents[pos] for pos in
                            [(x,y-1), (x+1, y), (x, y+1), (x-1, y)]
                            if pos in self.contents]

        log(f'{len(neighbours)} to match')
        matches = []
        if all(matches):
            self.contents[(x,y)] = tile

    def __str__(self):
        rows = []
        for y in range(self.side):
            row_gen = []
            for x in range(self.side):
                tile = self.contents.get((x,y))
                if tile:
                    row_gen.append(tile.get_lines())
                else:
                    row_gen.append('-'*10 for _ in range(10))
            gen = zip(*row_gen)
            lines = [' '.join(g) for g in gen]
            rows.extend(lines)
            rows.append('\n')
        return '\n'.join(rows)



class Tile:
    def __init__(self, name, tile_lines, grid):
        self.name = name[:-1]
        self.id_number = int(self.name.split(' ')[1])
        self.side_length = len(tile_lines)
        self._lines = tile_lines
        self._extract_edges()
        self.outside_edges = []
        self.grid_pos = None
        self.grid = grid

    def _extract_edges(self):
        top = self._lines[0]
        right = ''.join(line[-1] for line in self._lines)
        bottom = self._lines[-1]
        left = ''.join(line[0] for line in self._lines)
        self._edges = (top, right, bottom, left)

    def edges(self):
        for edge in self._edges:
            yield edge
        for edge in self._edges:
            yield edge[::-1]

    def set_grid_pos(self, x, y):
        log(f'{self.name} @ {x},{y}')
        self.grid_pos = (x, y)
        self.grid.add_tile(self)

    def get_lines(self):
        return (l for l in self._lines)

    def mark_outside_edge(self, edge_str):
        self.outside_edges.append(edge_str)

    def orientation(self):
        return tuple(e in self.outside_edges for e in self._edges)

    def match_orientation(self, orientation):
        while self.orientation() != orientation:
            self.rotate_cw()

    def match_edge(self, tile):
        for i, edge in enumerate(self._edges):
            for j, other_edge in enumerate(tile.edges()):
                if edge == other_edge:
                    self._reorientate_match(tile, i, j)
                    #log(self)
                    #log(self.orientation())
                    #log('~~~~')
                    #log(tile)
                    #log(tile.orientation())
                    try:
                        log(f'match! {self.name} {i} {edge} <-> {other_edge} {j} {tile.name}')
                        log(f'  {self.name} {self.orientation()} <-> {tile.orientation()} {tile.name}')
                        x, y = self.grid_pos
                        if i == 0:
                            tile.set_grid_pos(x, y - 1)
                        elif i == 1:
                            tile.set_grid_pos(x + 1, y)
                        elif i == 2:
                            tile.set_grid_pos(x, y + 1)
                        elif i == 3:
                            tile.set_grid_pos(x - 1, y)
                        return True
                    except:
                        log('placement failed')
                        return False
        return False

    def _reorientate_match(self, other, side, other_side):
        if other_side in (4, 6):
            other.flip_x()
            other_side -= 4
        elif other_side in (5, 7):
            other.flip_y()
            other_side -= 4
        ops = {
            (TOP,TOP): (other.flip_y,),
            (TOP,RIGHT): (other.rotate_cw, other.flip_x),
            (TOP,BOTTOM): tuple(),
            (TOP,LEFT): (other.rotate_ccw,),

            (RIGHT,TOP): (other.rotate_cw, other.flip_y),
            (RIGHT,RIGHT): (other.flip_x,),
            (RIGHT,BOTTOM): (other.rotate_ccw,),
            (RIGHT,LEFT): tuple(),

            (BOTTOM,TOP): tuple(),
            (BOTTOM,RIGHT): (other.rotate_ccw,),
            (BOTTOM,BOTTOM): (other.flip_y,),
            (BOTTOM,LEFT): (other.rotate_cw, other.flip_x),

            (LEFT,TOP): (other.rotate_cw,),
            (LEFT,RIGHT): tuple(),
            (LEFT,BOTTOM): (other.rotate_ccw, other.flip_y),
            (LEFT,LEFT): (other.flip_x,)
        }
        alignments = ops[(side, other_side)]
        for op in alignments:
            op()


    def _cols(self):
        cols = []
        for i in range(self.side_length):
            cols.append(''.join(line[i] for line in self._lines))
        return cols

    def rotate_ccw(self):
        self._lines = [c for c in self._cols()[::-1]]
        self._extract_edges()

    def rotate_cw(self):
        self._lines = [c[::-1] for c in self._cols()]
        self._extract_edges()

    def flip_x(self):
        self._lines = [c[::-1] for c in self._lines]
        self._extract_edges()

    def flip_y(self):
        self.rotate_cw()
        self.flip_x()
        self.rotate_ccw()

    def __str__(self):
        return '\n'.join(self._lines)

    def __repr__(self):
        return self.name


def solve():
    tiles, grid = load_tiles()
    counts = Counter(chain(*[t.edges() for t in tiles]))
    pprint(counts)

    edge_map = defaultdict(list)
    for t in tiles:
        for edge in t.edges():
            edge_map[edge].append(t)

    outside_tiles = []
    outside_edges = [k for k, v in counts.items() if v == 1]
    for e in outside_edges:
        ts = edge_map[e]
        assert len(ts) == 1
        t = ts[0]
        outside_tiles.append(t)
        t.mark_outside_edge(e)

    edges_counter = Counter(outside_tiles)
    corner_names = [k for k, v in edges_counter.items() if v == 4]
    print('Part 1 - corners are:', corner_names)
    corner_tiles = [t for t in tiles if t in corner_names]
    edges = set(t for t in outside_tiles)
    print(len(corner_tiles), len(set(edges)))

    grid_side = 11
    corner0 = corner_tiles[0]
    corner_positions = {
        (True, True, False, False): (grid_side, 0),
        (True, False, False, True): (0, 0),
        (False, True, True, False): (grid_side, grid_side),
        (False, False, True, True): (0, grid_side)
    }

    newSolve = True
    if newSolve:
        grid.try_tile(corner0, 0, 0)
        log(grid)

    if not newSolve:
        corner0.set_grid_pos(*corner_positions[corner0.orientation()])
        print(f'corner0 @ {corner0.grid_pos}')
        placed = {corner0}
        edges -= {corner0}
        i = 0
        while edges:
            i += 1
            if i > 100:
                break
            new_placed = set()
            for t in placed:
                for e in edges:
                    if t.match_edge(e):
                        new_placed.add(e)
            placed |= new_placed
            edges -= new_placed
            print(f'{len(placed)} {len(edges)}')
        print(f'done {len(placed)} {len(edges)}, {i}')

        rest = set(t for t in tiles if not t.grid_pos)
        print(f'rest {len(rest)}')
        while rest:
            i += 1
            if i > 1000:
                break
            new_placed = set()
            for t in placed:
                for r in rest:
                    if t.match_edge(r):
                        new_placed.add(r)
            placed |= new_placed
            rest -= new_placed
            print(f'{len(placed)} {len(rest)}')
        print(f'done {len(placed)} {len(rest)}, {i}')

        print(corner0.grid)

if __name__ == '__main__':
    solve()

