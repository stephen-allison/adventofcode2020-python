import re
from functools import partial


def between(low, high, val):
    return low <= int(val) <= high


def length(required, val):
    return len(val) == required


def height_check(height, unit):
    if unit == 'in':
        return between(59, 76, height)
    elif unit == 'cm':
        return between(150, 193, height)

def print_record(record):
    sr = sorted(record.split(' '))
    if 'cid' not in record:
        sr[1:1] = ['cid:-']
    print('\t'.join(sr))


rules = {
    'byr': (re.compile('byr:(\d{4})\\b'), partial(between, 1920, 2002)),
    'iyr': (re.compile('iyr:(\d{4})\\b'), partial(between, 2010, 2020)),
    'eyr': (re.compile('eyr:(\d{4})\\b'), partial(between, 2020, 2030)),
    'hgt': (re.compile('hgt:(\d+)(in|cm)\\b'), height_check),
    'hcl': (re.compile('hcl:#([0-9a-f]*)\\b'), partial(length, 6)),
    'ecl': (re.compile('ecl:(amb|blu|brn|gry|grn|hzl|oth)'), None),
    'pid': (re.compile('pid:(\d{9})\\b'), None)
}


def load():
    with open('input.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]


def records(data):
    record = []
    for line in data:
        if line:
            record.append(line)
        else:
            yield ' '.join(record)
            record = []
    yield ' '.join(record)


def records_with_fields(records):
    required = rules.keys()
    for record in records:
        field_check = [f'{f}:' in record for f in required]
        if all(field_check):
            yield record


def records_with_validated_fields(records):
    for r in records:
        if validate_fields(r):
            yield r


def validate_fields(record):
    for field, (pattern, test) in rules.items():
        match = re.search(pattern, record)
        if not match:
            return False
        elif test:
            if not test(*match.groups()):
                return False
    return True


def solve():
    recs = records(load())
    valid_recs = records_with_fields(recs)
    valid = 0
    for r in records_with_validated_fields(valid_recs):
        print_record(r)
        valid += 1
    print(f'fully validated records: {valid}')

if __name__ == "__main__":
    solve()
