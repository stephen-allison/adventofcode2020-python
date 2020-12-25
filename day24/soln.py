from collections import Counter
from itertools import chain

DIRECTIONS = {
    'e': (1, -1, 0),
    'w': (-1, 1, 0),
    'ne': (1, 0, -1),
    'sw': (-1, 0, 1),
    'nw': (0, 1, -1),
    'se': (0, -1, 1),
}


def load():
    with open('input.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]


def neighbours(tile):
    x, y, z = tile
    return [(x+dx, y+dy, z+dz) for dx, dy, dz in DIRECTIONS.values()]


def instructions_in_line(line):
    instrs = []
    while line:
        if line[0] in DIRECTIONS:
            instrs.append(line[0])
            line = line[1:]
        else:
            instrs.append(line[:2])
            line = line[2:]
    return instrs


def follow_path(instructions):
    position = (0, 0, 0)
    for move in instructions:
        dx, dy, dz = DIRECTIONS[move]
        x, y, z = position
        position = (x + dx, y + dy, z + dz)
    return position


def solve():
    instructions = [instructions_in_line(line) for line in load()]
    end_positions = [follow_path(inst) for inst in instructions]
    position_counts = Counter(end_positions)
    black_tiles = [tile for tile, count in
                      position_counts.items() if count % 2 != 0]
    print(f'part one - there are {len(black_tiles)} black tiles')

    black_tiles = set(black_tiles)
    for i in range(100):
        all_neighbours = chain(*[neighbours(t) for t in black_tiles])
        neighbour_counts = Counter(all_neighbours)
        turn_black = set(tile for tile, count in neighbour_counts.items()
                         if count == 2
                         and tile not in black_tiles)
        turn_white = set(tile for tile in black_tiles
                         if neighbour_counts[tile] == 0
                         or neighbour_counts[tile] > 2)
        black_tiles -= turn_white
        black_tiles |= turn_black
    print(f'part two - there are {len(black_tiles)} black tiles')



if __name__ == '__main__':
    solve()
