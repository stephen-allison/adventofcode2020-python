from itertools import islice

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def advance(self, n=1):
        next_node = self
        for _ in range(n):
            next_node = next_node.next
        return next_node

    def clockwise_nodes(self, count):
        return [self.advance(n) for n in range(1, count + 1)]


class CircularBuffer:
    def __init__(self, nodes):
        self.nodes = {n.value: n for n in nodes}
        self.current = nodes[0]
        for node, next_node in zip(nodes, islice(nodes, 1, None)):
            node.next = next_node
        nodes[-1].next = nodes[0]

    def __len__(self):
        return len(self.nodes)

    def find(self, node_value):
        return self.nodes.get(node_value)

    def move(self, dest, count, src=None):
        src = src or self.current
        to_move = src.clockwise_nodes(count)
        first = to_move[0]
        last = to_move[-1]
        src.next = last.next
        last.next = dest.next
        dest.next = first


def play(input, rounds=10):
    nodes = [Node(i) for i in input]
    cups = CircularBuffer(nodes)
    min_input = min(input)
    max_input = max(input)
    for _ in range(rounds):
        to_move = cups.current.clockwise_nodes(3)
        dest_val = cups.current.value - 1
        dest = None
        while not dest:
            dest = cups.find(dest_val)
            if dest in to_move:
                dest = None
            dest_val -= 1
            if dest_val < min_input:
                dest_val = max_input
        cups.move(dest, 3)
        cups.current = cups.current.next
    return cups


def solve():
    input = [int(i) for i in '643719258']
    cups = play(input, 100)
    nodes = cups.find(1).clockwise_nodes(len(cups) - 1)
    result = ''.join([str(n.value) for n in nodes])
    print(f'part one answer = {result}')

    print('part two...')
    input.extend(i for i in range(len(input) + 1, 1_000_001))
    cups = play(input, 10_000_000)
    val1 = cups.find(1).advance().value
    val2 = cups.find(1).advance(2).value
    print(f'part 2 answer is {val1 * val2}')


if __name__ == '__main__':
    solve()
