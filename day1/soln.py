def load_numbers():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    numbers = map(int, lines)
    return set(numbers)


def two_sum_to(numbers, target):
    for n in numbers:
        if target - n in numbers:
            print(f'two sum {n} + {target - n} = {target}')
            return n* (target - n)

def three_sum_to(numbers, target):
    for n in numbers:
        remaining = target - n
        two_sum = two_sum_to(numbers - set([n]), remaining)
        if two_sum:
            print(n)
            return n*two_sum

def solve():
    numbers = load_numbers()
    print(f'Part 1 solution: {two_sum_to(numbers, 2020)}')
    print(f'Part 2 solution: {three_sum_to(numbers, 2020)}')

if __name__ == '__main__':
    solve()
