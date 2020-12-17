from collections import defaultdict
from itertools import chain


def load_rules():
    with open('input.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]


def parse_rules(rules):
    bags = defaultdict(list)
    for rule in rules:
        bags[get_container(rule)] = get_contained(rule)
    return bags


def get_container(rule):
    return rule.split('bags', 1)[0].strip()


def get_contained(rule):
    contained_str = rule.split('contain', 1)[1].strip().replace('.', '')
    if 'no other bags' in contained_str:
        return []
    else:
        bags = contained_str.split(',')
        bag_counts = [tuple(b.strip().split(' ', 1)) for b in bags]
        return [(' '.join(b.split(' ')[:-1]), int(c)) for c,b in bag_counts]


def container_lookup(parsed):
    lookup = defaultdict(list)
    for container, contained in parsed.items():
        for bag, count in contained:
            if contained:
                lookup[bag].append(container)
    return lookup


def hold_me(kind, lookup):
    ctrs = []
    cs =  lookup[kind]
    while cs:
        ctrs.extend(cs)
        cs2 = list(chain(*[lookup[b] for b in cs if lookup[b] not in cs]))
        cs = cs2
    return set(ctrs)


def containerama(bag, contains_lookup):
    ctd = contains_lookup[bag]
    if ctd:
        return sum([c*containerama(b, contains_lookup) for b,c in ctd]) + 1
    else:
        return 1


def solve():
    kind = 'shiny gold'
    rules = load_rules()
    parsed = parse_rules(rules)
    lookup = container_lookup(parsed)
    print(f'{len(hold_me(kind, lookup))} bags can contain a {kind} bag')
    print(f'a {kind} bag contains {containerama(kind, parsed) - 1} bags')


if __name__ == '__main__':
    solve()
