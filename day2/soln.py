def load():
    with open('input.txt', 'r') as f:
        return f.readlines()


def parse_line(line):
    step1 = line.split(' ')
    count = map(int, step1[0].split('-'))
    char = step1[1][:-1]
    password = step1[2]
    return tuple(count), char, password


def valid(count_range, char, password):
    min_count, max_count = count_range
    return min_count <= password.count(char) <= max_count


def valid_2(positions, char, password):
    a, b = positions
    return (password[a-1] == char) != (password[b-1] == char)


def check_line(line):
    return valid(*parse_line(line))


def check_line_2(line):
    return valid_2(*parse_line(line))


def solve():
    lines = load()
    validity = [check_line(l) for l in lines]
    print(validity.count(True))
    validity = [check_line_2(l) for l in lines]
    print(validity.count(True))


if __name__ == '__main__':
    solve()
