from functools import reduce
from itertools import product


def get_joltages():
    with open('input.txt', 'r') as f:
        return [int(line.strip()) for line in f.readlines()]


test_input = [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34 ,10, 3]

small_input = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]


def solve_part_1():
    jolts = get_joltages()
    jolts.append(max(jolts) + 3)

    def f(acc, jolts):
        ones, threes, last = acc
        if jolts - last == 1:
            ones += 1
        elif jolts - last == 3:
            threes += 1
        return (ones, threes, jolts)

    o, t, _ = reduce(f, sorted(jolts), (0,0,0))
    print('answer =', o*t)


def solve_part_2():
    jolts = get_joltages()
    max_j = max(jolts) + 3
    jolts.append(max_j)
    ways_to = [0] * (max_j + 1)
    ways_to[0] = 1
    for j, diff in product(sorted(jolts), (1, 2, 3)):
        if j >= diff:
            ways_to[j] += ways_to[j - diff]
    print(f"# options = {ways_to[max_j]}")


if __name__ == '__main__':
    solve_part_1()
    solve_part_2()
