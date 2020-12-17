def get_codes():
    with open('input.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]


def test():
    tests = [('FBFBBFFRLR', (44, 5)),
             ('BFFFBBFRRR', (70, 7)),
             ('FFFBBBFRRR', (14, 7)),
             ('BBFFBBFRLL', (102, 4))
            ]
    for code, expected in tests:
        res = process_code(code)
        assert expected == res


def row_from_code(code):
    row_code = code[:7]
    bits = {
        'F': 0,
        'B': 1
    }
    return iterate_code(row_code, bits)


def col_from_code(code):
    col_code = code[7:]
    bits = {
        'L': 0,
        'R': 1
    }
    return iterate_code(col_code, bits)


def iterate_code(code, bit_map):
    val = 0
    for c in code:
        bit = bit_map[c]
        val <<= 1
        val |= bit
    return val


def process_code(code):
    return row_from_code(code), col_from_code(code)


def seat_id(row, col):
    return (row * 8) + col


def solve():
    codes = get_codes()
    ids = [seat_id(*process_code(c)) for c in codes]
    max_id = max(ids)
    print(f'highest seat id is {max_id}')

    occupancy = [False] * (max_id + 1)
    for id in ids:
        occupancy[id] = True

    search_from = occupancy.index(True)
    try:
        while True:
            next_empty = occupancy.index(False, search_from)
            if occupancy[next_empty - 1] and occupancy[next_empty + 1]:
                print(f"empty seat is {next_empty}")
                break
            else:
                search_from = next_empty
    except (ValueError, IndexError):
        print('no empty seat found')


if __name__ == '__main__':
    test()
    solve()
