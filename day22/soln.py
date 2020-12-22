from collections import deque
from itertools import count


def decks():
    with open('input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        p1 = map(int, lines[1:lines.index('')])
        p2 = map(int, lines[lines.index('Player 2:') + 1:])
        return deque(p1), deque(p2)

def score(deck):
    return sum(n*c for n,c in zip(count(1), reversed(deck)))

def solve():
    p1_deck, p2_deck = decks()
    while p1_deck and p2_deck:
        p1 = p1_deck.popleft()
        p2 = p2_deck.popleft()
        if p1 > p2:
            p1_deck.extend([p1,p2])
        elif p1 < p2:
            p2_deck.extend([p2,p1])
    print('part 1 answer =', max(score(p1_deck), score(p2_deck)))


if __name__ == '__main__':
    solve()
