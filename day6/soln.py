from functools import reduce
import operator


def load():
    with open('input.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]


def grouped_data(data, op):
    group = []
    for line in data:
        if line:
            group.append(set(line))
        else:
            yield reduce(op, group)
            group = []
    yield reduce(op, group)


def solve():
    print(sum(map(len, grouped_data(load(), operator.or_))))
    print(sum(map(len, grouped_data(load(), operator.and_))))


if __name__ == '__main__':
    solve()
