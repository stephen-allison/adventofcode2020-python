from itertools import count, islice


def get_code():
    with open('input.txt', 'r') as f:
        return [int(line.strip()) for line in f.readlines()]


def two_sum_to(numbers, target):
    nums = set(numbers)
    return any(target - n in nums - {n} for n in nums)


def scan_xmas(code, preamble_length):
    for index in count(preamble_length):
        val = code[index]
        start = index - preamble_length
        if not two_sum_to(islice(code, start, index), val):
            return val, index


def crack_xmas(code, target):
    seqs = [[n] for n in code]
    for i in count(1):
        for n, j in enumerate(islice(code, i, None)):
            seq = seqs[n]
            seq.append(j)
            if sum(seq) == target:
                return seq, n


def solve():
    code = get_code()
    target, loc = scan_xmas(code, 25)
    print(f'target code {target} at {loc}')
    seq , loc = crack_xmas(code, target)
    print(f'min + max is {max(seq) + min(seq)} at {loc} to {loc + len(seq)}')


if __name__ == '__main__':
    solve()
