import re
from pprint import pprint

def load():
    data = []
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            words = re.findall('(\w+)', line)
            contains_loc = words.index('contains')
            ingredients = words[:contains_loc]
            allergens = words[contains_loc + 1:]
            data.append((set(ingredients), set(allergens)))
    return data


def solve():
    data = load()
    all_ingredients = set()
    all_allergens = set()
    for ingredients, allergens in data:
        all_ingredients |= ingredients
        all_allergens |= allergens

    possible = {allergen: set(all_ingredients) for allergen in all_allergens}
    for ingredients, allergens in data:
        for a in allergens:
            possible[a] &= ingredients
    safe = set(all_ingredients)
    for bad in possible.values():
        safe -= bad
    print(f'safe: {len(safe)}')
    count = 0
    for ingredients, _ in data:
        for i in safe:
            if i in ingredients:
                count += 1
    print(f'part one answer is {count}')

    found = set(k for k,v in possible.items() if len(v) == 1)
    while any(len(vals) > 1 for vals in possible.values()):
        print(f'found {found}')
        new_finds = set()
        processed = set()
        for agen in found:
            for algn, ingr in possible.items():
                if algn != agen:
                    ingr -= possible[agen]
                    if len(ingr) == 1:
                        new_finds.add(algn)
            processed.add(agen)
        found -= processed
        found |= new_finds
    pprint(possible)
    dangerous = [v.pop() for k,v in sorted(possible.items())]
    print('part 2 = ', ','.join(dangerous))

if __name__ == '__main__':
    solve()
