from itertools import count


def load():
    with open('input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        return (int(lines[0]), lines[1].split(','))


def solve():
    dt, ts = load()
    in_service = [int(t) for t in ts if t != 'x']
    ns = []
    for t in in_service:
        next_t = (1 + dt//t) * t
        delay = next_t - dt
        ns.append((delay, t))
    b = min(ns)
    print(f'part1 = {b[0] * b[1]}')


# https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Search_by_sieving
def solve2():
    _, ts = load()
    ts = [(int(t),i) for i, t in enumerate(ts) if t != 'x']
    vals_at_zero = [(t - off) % t for t, off in ts]
    lcm = 1
    pos = 0
    for i, (t, off) in enumerate(ts):
        lcm *= next_t   #everything is prime, so just multiply
        try:
            next_t, next_off = ts[i+1]
        except IndexError:
            break
        for n in count(start=pos, step=lcm):
            pos = n
            if (n % next_t) == vals_at_zero[i+1]:
                break
    print(f'part2 = {n}')


if __name__ == '__main__':
    solve()
    solve2()
