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
    grid = Grid(12, 10)
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
    def __init__(self, side, cell_side):
        self.side = side
        self.cell_side = cell_side
        self.contents = {}
        self.opts = []

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
        print(tile)
        print('~~~')
        if x == y == 0:
            tile.match_orientation((True, False, False, True))
            return True

        neighbours = [self.contents.get(pos) for pos in
                            [(x,y-1), (x+1, y), (x, y+1), (x-1, y)]]

        for _ in tile.orientations():
            matches = []
            for i, n in enumerate(neighbours):
                if n and tile.edge(i) in n._edges:
                    print(f'possible match {i} {tile._edges} <> {n._edges}')

                if not n:
                    matched = True
                elif i == TOP:
                    matched = tile.edge(TOP) == n.edge(BOTTOM)
                elif i == RIGHT:
                    matched = tile.edge(RIGHT) == n.edge(LEFT)
                elif i == BOTTOM:
                    matched = tile.edge(BOTTOM) == n.edge(TOP)
                elif i == LEFT:
                    print(f'n.Right={n.edge(RIGHT)} t.Left={tile.edge(LEFT)}')
                    matched = tile.edge(LEFT) == n.edge(RIGHT)
                matches.append(matched)
            print(f'all matches {matches}')
            if all(matches):
                break
        return all(matches)

    def place(self, x, y, tiles):
        options = [t for t in tiles if self.try_tile(t, x, y)]
        self.opts.append(((x,y),options))
        if options:
            log(f'placed {options[0].name} at {x},{y}')
            self.contents[(x,y)] = options[0]
            return options[0]
        return None

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

    def edge(self, edge_num):
        return self._edges[edge_num]

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

    def orientations(self):
        def rotate_round():
            for i in range(4):
                self.rotate_cw()
                yield
        yield
        yield from rotate_round()

        self.flip_x()
        yield from rotate_round()
        self.flip_x()

        self.flip_y()
        yield from rotate_round()
        self.flip_y()

        self.flip_x()
        self.flip_y()
        yield from rotate_round()



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
    #test_tile()
    #return
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
    all_tiles = set(tiles) - {corner0}
    if newSolve:
        print(corner0)
        print('---')
        grid.place(0, 0, [corner0])
        log(grid)
        print('')
        to_add = edges - {corner0}
        for i in range(1,12):
            added = grid.place(i, 0, to_add)
            to_add -= {added}
            all_tiles -= {added}
        log(grid)
        for x,y in product([0,11], range(1,11)):
            added = grid.place(x, y, to_add)
            to_add -= {added}
            all_tiles -= {added}
        log(grid)
        for i in range(0,12):
            added = grid.place(i, 11, to_add)
            to_add -= {added}
            all_tiles -= {added}
        log(grid)
        for y in range(1, 11):
            for x in range(1, 11):
                added = grid.place(x, y, all_tiles)
                all_tiles -= {added}
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

    t.rotate_ccw()
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

