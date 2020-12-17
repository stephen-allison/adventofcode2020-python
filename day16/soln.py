from collections import defaultdict
from functools import reduce
from itertools import chain
import re

RULE = re.compile('(.*): (\d+)-(\d+) or (\d+)-(\d+)')


def parse_rule(line):
    match = re.match(RULE, line)
    name, lo1, hi1, lo2, hi2 = match.groups()
    return (name, (int(lo1), int(hi1)), (int(lo2), int(hi2)))


def parse_ticket(line):
    return tuple(int(c) for c in line.split(','))


PARSERS = {
    'your ticket:': (parse_ticket, 'your_ticket'),
    'nearby tickets:': (parse_ticket, 'nearby_tickets')
}


def parse_input(filename):
    with open(filename, 'r') as f:
        parser = parse_rule
        section = 'rules'
        parsed = defaultdict(list)
        for line in (line.strip() for line in f.readlines()):
            if line in PARSERS.keys():
                parser, section = PARSERS[line]
            elif line:
                parsed[section].append(parser(line))
    return parsed['rules'], parsed['nearby_tickets'], parsed['your_ticket'][0]


def value_valid(rule, value):
    _, (l1, h1), (l2, h2) = rule
    return (l1 <= value <= h1) or (l2 <= value <= h2)


def valid_fields(rules, value):
    return {r[0] for r in rules if value_valid(r, value)}


def possible_field_positions(ticket_data, rules):
    for row in ticket_data:
        possible_fields = [valid_fields(rules, val) for val in row]
        if all(possible_fields):
            yield possible_fields


def find_field_positions(rows, rules):
    unresolved = [{r[0] for r in rules} for _ in rules]
    field_positions = {}
    for possibles in rows:
        for p, f in zip(unresolved, possibles):
            p &= f
    while any(unresolved):
        found = set()
        for i, poss in enumerate(unresolved):
            if len(poss) == 1:
                found |= poss
                field_positions[poss.pop()] = i
        for poss in unresolved:
                poss -= found
    return field_positions


def solve():
    rules, nearby_tickets, ticket = parse_input('input.txt')
    total = sum(filter(lambda v: not any(valid_fields(rules, v)),
                chain(*nearby_tickets)))
    print(f'part i answer = {total}')

    poss = possible_field_positions(nearby_tickets, rules)
    field_positions = find_field_positions(poss, rules)
    val = 1
    for field, pos in field_positions.items():
        if 'departure' in field:
            val *= ticket[pos]
    print(f'part ii answer = {val}')


if __name__ == '__main__':
    solve()
