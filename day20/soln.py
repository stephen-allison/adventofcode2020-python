from collections import Counter, defaultdict
from itertools import chain, cycle, product
from pprint import pprint

def log(*args):
    print(*args)

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

MONSTER = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #'
]

def load_tiles():
    tiles = []
    tile_lines = []
    tile_name = None
    grid = Grid(12, 10)
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                tiles.append(Tile(tile_name, tile_lines))
            elif line.startswith('Tile'):
                tile_name = line
                tile_lines = []
            else:
                tile_lines.append(line)
    log(f'Loaded {len(tiles)} tiles')
    return tiles, grid


class Grid:
    def __init__(self, side, cell_side):
        self.side = side
        self.cell_side = cell_side
        self.contents = {}

    def place(self, x, y, tiles):
        options = [t for t in tiles if self.try_tile(t, x, y)]
        if options:
            self.contents[(x,y)] = options[0]
            return options[0]
        return None

    def try_tile(self, tile, x, y):
        if x == y == 0:
            tile.match_orientation((True, False, False, True))
            return True

        neighbours = [self.contents.get(pos) for pos in
                            [(x,y-1), (x+1, y), (x, y+1), (x-1, y)]]

        for _ in tile.orientations():
            matches = []
            for i, n in enumerate(neighbours):
                if not n:
                    matched = True
                elif i == TOP:
                    matched = tile.edge(TOP) == n.edge(BOTTOM)
                elif i == RIGHT:
                    matched = tile.edge(RIGHT) == n.edge(LEFT)
                elif i == BOTTOM:
                    matched = tile.edge(BOTTOM) == n.edge(TOP)
                elif i == LEFT:
                    matched = tile.edge(LEFT) == n.edge(RIGHT)
                matches.append(matched)
            if all(matches):
                break
        return all(matches)

    def __str__(self):
        rows = []
        for y in range(self.side):
            row_gen = []
            for x in range(self.side):
                tile = self.contents.get((x,y))
                if tile:
                    row_gen.append(tile.get_lines())
                else:
                    row_gen.append('-'*self.cell_side for _ in range(self.cell_side))
            gen = zip(*row_gen)
            lines = [' '.join(g) for g in gen]
            rows.extend(lines)
            rows.append('\n')
        return '\n'.join(rows)


class Tile:
    def __init__(self, name, tile_lines):
        self.name = name[:-1]
        self.outside_edges = []
        self.side_length = len(tile_lines)
        self._lines = tile_lines
        self._extract_edges()

    def _extract_edges(self):
        top = self._lines[0]
        right = ''.join(line[-1] for line in self._lines)
        bottom = self._lines[-1]
        left = ''.join(line[0] for line in self._lines)
        self._edges = (top, right, bottom, left)

    def possible_edges(self):
        '''all possible edges that a tile might have, flipped or non-flipped'''
        for edge in self._edges:
            yield edge
        for edge in self._edges:
            yield edge[::-1]

    def edge(self, edge_num):
        return self._edges[edge_num]

    def get_lines(self):
        return (l for l in self._lines)

    def get_char(self, x, y):
        return self._lines[y][x]

    def count_char(self, char):
        return sum(line.count(char) for line in self._lines)

    def find(self, pattern):
        matching_locations = []
        for y, x in product(range(self.side_length), range(self.side_length)):
            try:
                match = []
                for cx, cy in pattern:
                    check_pos = (x+cx, y+cy)
                    if self.get_char(*check_pos) == '#':
                        match.append(check_pos)
                if len(match) == len(pattern):
                    log(f'matched monster at {x}, {y}')
                    matching_locations.extend(match)
            except IndexError:
                pass
        return matching_locations

    def mark_outside_edge(self, edge_str):
        self.outside_edges.append(edge_str)

    def orientation(self):
        '''tuple of bool - each entry is True if that edge (T,R,B,L)
        is an outside edge'''
        return tuple(e in self.outside_edges for e in self._edges)

    def match_orientation(self, orientation):
        '''rotate until outside edges match given orientation'''
        while self.orientation() != orientation:
            self.rotate_cw()

    def orientations(self):
        '''all possible transformations of tile'''
        def rotate_round():
            for i in range(4):
                self.rotate_cw()
                yield
        yield from rotate_round()
        self.flip_x()
        yield from rotate_round()

    def _cols(self):
        cols = []
        for i in range(self.side_length):
            cols.append(''.join(line[i] for line in self._lines))
        return cols

    def rotate_cw(self):
        self._lines = [c[::-1] for c in self._cols()]
        self._extract_edges()

    def flip_x(self):
        self._lines = [c[::-1] for c in self._lines]
        self._extract_edges()

    def centre(self):
        return [l[1:-1] for l in self._lines[1:-1]]

    def __str__(self):
        return '\n'.join(self._lines)

    def __repr__(self):
        return self.name


class Image:
    def __init__(self, grid):
        self.pixels = {}
        self.grid_side = grid.side
        self.pixels = {k: t.centre() for k, t in grid.contents.items()}
        self.tile = Tile('Image 0:', self._as_string().split('\n'))

    def _as_string(self):
        rows = []
        for y in range(self.grid_side):
            row_gen = []
            for x in range(self.grid_side):
                cell = self.pixels.get((x,y))
                row_gen.append((l for l in cell))
            gen = zip(*row_gen)
            lines = [''.join(g) for g in gen]
            rows.extend(lines)
        return '\n'.join(rows)

    def find(self, pattern):
        found = []
        for _ in self.tile.orientations():
            found.append(self.tile.find(pattern))
        return found

    def __str__(self):
        return str(self.tile)


def monster_pattern():
    coords = []
    for y, line in enumerate(MONSTER):
        for x, ch in enumerate(line):
            if ch == '#':
                coords.append((x,y))
    return coords


def solve():
    tiles, grid = load_tiles()
    counts = Counter(chain(*[t.possible_edges() for t in tiles]))

    edge_map = defaultdict(list)
    for t in tiles:
        for edge in t.possible_edges():
            edge_map[edge].append(t)

    # find the outside edges, then build up from a corner
    outside_tiles = []
    # outward facing edges are not paired and so have count 1
    outside_edges = [edge for edge, occs in counts.items() if occs == 1]
    for e in outside_edges:
        ts = edge_map[e]
        assert len(ts) == 1
        t = ts[0]
        outside_tiles.append(t)
        t.mark_outside_edge(e)

    edges_counter = Counter(outside_tiles)
    # corners have two unpaired edges, each with 2 orientations
    # possible -> has count of 4
    corner_names = [k for k, v in edges_counter.items() if v == 4]
    print('Part 1 - corners are:', corner_names)
    corner_tiles = [t for t in tiles if t in corner_names]
    outside_edges = set(t for t in outside_tiles)

    corner0 = corner_tiles[0]
    unplaced = set(tiles) - {corner0}

    grid.place(0, 0, [corner0])
    log(grid)
    unplaced_edges = outside_edges - {corner0}
    for i in range(1,12):
        added = grid.place(i, 0, unplaced_edges)
        unplaced_edges -= {added}
    log(grid)
    for x,y in product([0,11], range(1,11)):
        added = grid.place(x, y, unplaced_edges)
        unplaced_edges -= {added}
    log(grid)
    for i in range(0,12):
        added = grid.place(i, 11, unplaced_edges)
        unplaced_edges -= {added}
    log(grid)
    #all edges now placed

    # place all the other tiles
    unplaced -= outside_edges
    for y in range(1, 11):
        for x in range(1, 11):
            added = grid.place(x, y, unplaced)
            unplaced -= {added}
    log(grid)


    img = Image(grid)
    log(img)
    log('\n'.join(MONSTER))
    monster = monster_pattern()
    matched = filter(None, img.find(monster))
    matched_sets = list(map(set, matched))
    hash_count = img.tile.count_char('#')
    print(f'part two ans: {hash_count - max(map(len, matched_sets))}')


def test_tile():
    lines = ['#.##',
             '.#..',
             '#.#.',
             '.##.']
    lines2 = ['#...',
              '....',
              '#..#',
              '##.#']
    lines3 = ['##.#',
              '....',
              '.##.',
              '.##.']
    lines4 = [
              '#..#',
              '.#..',
              '###.',
              '##..',
              ]
    g = Grid(4, 4)
    t = Tile('test 0:', lines, g)
    t2 = Tile('test 1:', lines2, g)
    t3 = Tile('test 2:', lines3, g)
    t4 = Tile('test 3:', lines4, g)
    t5 = Tile('test 4:', lines4, g)

    print(t5)
    print('double filp')
    t5.flip_x()
    print(t5)
    print('+=+=+=+')


    r_lines = ['.#.#',
               '#.#.',
               '##.#',
               '...#']
    print(t)
    print('=====')
    t.rotate_cw()
    print(t)
    print('=====')
    print('\n'.join(r_lines))
    assert str(t) == '\n'.join(r_lines)

    t.rotate_cw()
    t.rotate_cw()
    t.rotate_cw()
    g.place(1, 1, [t])
    print(g)
    print('')
    g.place(2, 1, [t2])
    print(g)
    g.place(1, 2, [t3])
    print(g)
    g.place(2, 2, [t4])
    print(g)
    g.place(2, 0, [t5])
    print(g)

if __name__ == '__main__':
    solve()

