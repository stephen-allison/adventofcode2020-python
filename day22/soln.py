from collections import deque
from itertools import count

PLAYER_1 = 'player1'
PLAYER_2 = 'player2'

def decks():
    with open('input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        p1 = map(int, lines[1:lines.index('')])
        p2 = map(int, lines[lines.index('Player 2:') + 1:])
        return deque(p1), deque(p2)


def score(deck):
    return sum(n*c for n,c in zip(count(1), reversed(deck)))


def sub_deck(deck, cards):
    return deque([deck[n] for n in range(cards)])


def combat(p1_deck, p2_deck):
    while p1_deck and p2_deck:
        p1 = p1_deck.popleft()
        p2 = p2_deck.popleft()
        if p1 > p2:
            p1_deck.extend([p1,p2])
        elif p1 < p2:
            p2_deck.extend([p2,p1])
    if p1_deck:
        return PLAYER_1, score(p1_deck)
    return PLAYER_2, score(p2_deck)


def recursive_combat(p1_deck, p2_deck):
    previous = set()
    while p1_deck and p2_deck:
        if (tuple(p1_deck), tuple(p2_deck)) in previous:
            return PLAYER_1, score(p1_deck)
        previous.add((tuple(p1_deck), tuple(p2_deck)))

        p1 = p1_deck.popleft()
        p2 = p2_deck.popleft()

        if len(p1_deck) >= p1 and len(p2_deck) >= p2:
            winner, _ = recursive_combat(sub_deck(p1_deck, p1),
                                         sub_deck(p2_deck, p2))
            if winner == PLAYER_1:
                p1_deck.extend([p1, p2])
            else:
                p2_deck.extend([p2, p1])
        else:
            if p1 > p2:
                p1_deck.extend([p1,p2])
            elif p1 < p2:
                p2_deck.extend([p2,p1])
    if p1_deck:
        return PLAYER_1, score(p1_deck)
    elif p2_deck:
        return PLAYER_2, score(p2_deck)


def play_recursive_combat():
    p1_deck, p2_deck = decks()
    winner, winning_score = recursive_combat(p1_deck, p2_deck)
    print(f'Recursive Combat winner is {winner} with {winning_score} points')


def play_combat():
    p1_deck, p2_deck = decks()
    winner, winning_score = combat(p1_deck, p2_deck)
    print(f'Combat winner is {winner} with {winning_score} points')


def solve():
    play_combat()
    play_recursive_combat()


if __name__ == '__main__':
    solve()
