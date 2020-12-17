import numpy as np

def get_instructions():
    with open('input.txt', 'r') as f:
        instructions = []
        for line in f.readlines():
            line = line.strip()
            instructions.append((line[0], int(line[1:])))
        return instructions

def n(x, y, h, d):
    return x, y+d, h

def N(pos, wp, d):
    dwp = np.array([[0],[d]])
    return pos, wp + dwp

def s(x, y, h, d):
    return x, y-d, h

def S(pos, wp, d):
    dwp = np.array([[0],[d]])
    return pos, wp - dwp

def e(x, y, h, d):
    return x+d, y, h

def E(pos, wp, d):
    dwp = np.array([[d],[0]])
    return pos, wp + dwp

def w(x, y, h, d):
    return x-d, y, h

def W(pos, wp, d):
    dwp = np.array([[d],[0]])
    return pos, wp - dwp

def r(x, y, h, d):
    return x, y, (h + d) % 360

def R(pos, wp, d):
    theta = np.deg2rad(d)
    rm = np.array([[np.cos(theta), np.sin(theta)],
                   [-np.sin(theta), np.cos(theta)]])
    return pos, rm @ wp

def l(x, y, h, d):
    return x, y, (h - d) % 360

def L(pos, wp, d):
    theta = np.deg2rad(d)
    rm = np.array([[np.cos(theta), -np.sin(theta)],
                   [np.sin(theta), np.cos(theta)]])
    return pos, rm @ wp

def f(x, y, h, d):
    return {0: n, 90: e, 180: s, 270: w}[h](x, y, h, d)

def F(pos, wp, d):
    move = wp * d
    return pos + move, wp

def follow(instructions):
    x = y = 0
    h = 90
    for cmd, dist in instructions:
        fn = globals()[cmd.lower()]
        x, y, h = fn(x, y, h, dist)
    print(f'part one: manhattan distance = {abs(x) + abs(y)}')

def follow_waypoint(instructions):
    wp = np.array([[10],
                    [1]])
    pos = np.array([[0],
                    [0]])
    for cmd, dist in instructions:
        fn = globals()[cmd]
        pos, wp = fn(pos, wp, dist)
    x = pos[0][0]
    y = pos[1][0]
    print(f'part two: manhattan distance = {abs(round(x)) + abs(round(y))}')

def solve():
    instructions = get_instructions()
    follow(instructions)
    follow_waypoint(instructions)

if __name__ == '__main__':
    solve()
