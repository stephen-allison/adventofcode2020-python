def get_map():
    with open('input.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]


def route(the_map, dx, dy):
    height = len(the_map)
    width = len(the_map[0])
    x = y = 0
    while y < height:
        yield the_map[y][x]
        x = (x + dx) % width
        y = y + dy


def count_trees(route):
    return list(route).count('#')


def solve_i():
    route1 = route(get_map(), 3, 1)
    print(count_trees(route1))


def solve_ii():
    from functools import reduce
    slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    the_map = get_map()
    routes = [route(the_map, *slope) for slope in slopes]
    trees = [count_trees(r) for r in routes]
    print(reduce(lambda a,b: a*b, trees, 1))


if __name__ == '__main__':
    solve_i()
    solve_ii()
