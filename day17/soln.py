from collections import Counter
from functools import cache
from itertools import chain, product

@cache
def initial_state(filename, dims):
    active = set()
    with open(filename, 'r') as f:
        for y, row in enumerate(f.readlines()):
            for x, c in enumerate(row):
                if c == '#':
                    coord = [x, y] + [0] * (dims - 2)
                    active.add(tuple(coord))
        return active


def pairwise_add(a, b):
    return tuple(ai + bi for ai, bi in zip(a, b))


@cache
def neighbours(coord, deltas):
    return {pairwise_add(coord, delta) for delta in deltas}


def neighbour_offsets(dims):
    zero = tuple([0]*dims)
    return tuple(delta for delta in product(*[[-1,0,1]]*dims) if delta != zero)


def solve(dims, initial_file, turns=6):
    deltas = neighbour_offsets(dims)
    active = initial_state(initial_file, dims)
    for _ in range(turns):
        all_neighbours = chain(*[neighbours(cell, deltas) for cell in active])
        ctr = Counter(all_neighbours)
        deactivate = {c for c in active if ctr.get(c) not in (2, 3)}
        activate = {c for c, n in ctr.items() if (c not in active) and n == 3}
        active -= deactivate
        active |= activate
    return len(active)


if __name__ == '__main__':
    import time
    start = time.time()
    assert solve(3, 'test_input.txt') == 112
    print('3d test passed')
    print(f'3d solution is {solve(3, "input.txt")}')
    assert solve(4, 'test_input.txt') == 848
    print('4d test passed')
    print(f'4d solution is {solve(4, "input.txt")}')
    print(f'took {time.time() - start} seconds')
