class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return f'Node({self.value})'

    def __iter__(self):
        yield self
        next_node = self.next
        while next_node != self:
            yield next_node
            next_node = next_node.next

    def advance(self, n=1):
        iterator = iter(self)
        node = next(iterator)
        for _ in range(n):
            node = next(iterator)
        return node


class CircularBuffer:
    def __init__(self, nodes):
        self.nodes = {n.value: n for n in nodes}
        self.start = nodes[0]
        for node, next_node in zip(nodes, nodes[1:]):
            node.next = next_node
        nodes[-1].next = nodes[0]

    def __iter__(self):
        yield from iter(self.start)

    def __len__(self):
        return len(self.nodes)

    def find(self, node_value):
        return self.nodes.get(node_value)

    def advance(self, n, node=None):
        node = node or self.start
        return node.advance(n)

    def clockwise_nodes(self, count, start=None):
        start = start or self.start
        return [self.advance(n, start) for n in range(1, count + 1)]

    def move(self, dest, count, src=None):
        src = src or self.start
        to_move = self.clockwise_nodes(count, src)
        first = to_move[0]
        last = to_move[-1]
        src.next = last.next
        last.next = dest.next
        dest.next = first


def play(input, rounds=10):
    nodes = [Node(i) for i in input]
    buffer = CircularBuffer(nodes)
    min_input = min(input)
    max_input = max(input)
    for _ in range(rounds):
        to_move = buffer.clockwise_nodes(3)
        dest_val = buffer.start.value - 1
        dest = None
        while True:
            if min_input <= dest_val <= max_input:
                dest = buffer.find(dest_val)
                if dest not in to_move:
                    break
            if dest_val <= min_input:
                dest_val = max_input
            else:
                dest_val -= 1
        buffer.move(dest, 3)
        buffer.start = buffer.start.next

    return buffer


def solve():
    input = [int(i) for i in '643719258']
    buffer = play(input, 100)
    nodes = buffer.clockwise_nodes(len(buffer) - 1, buffer.find(1))
    result = ''.join([str(n.value) for n in nodes])
    print(f'part one answer = {result}')
    print('part two...')

    input2 = input + [i for i in range(len(input) + 1, 1_000_001)]
    buffer = play(input2, 10_000_000)
    val1 = buffer.find(1).advance().value
    val2 = buffer.find(1).advance(2).value
    print(f'part 2 answer is {val1 * val2}')


def test():
    input = '389125467'
    nodes = [Node(int(i)) for i in input]
    buffer = CircularBuffer(nodes)
    for n in buffer:
        print(f'{n} -> {n.next}')
    node = buffer.advance(3)
    print('advance 3')
    print(f'{node} -> {node.next}')
    node5 = buffer.find(5)
    print('find 5')
    print(f'{node5} -> {node5.next}')
    print('nodes after')
    to_move = buffer.clockwise_nodes(3)
    for n in to_move:
        print(f'{n}')
    dest = buffer.find(2)
    buffer.move(dest, 3)
    print('moved')
    for n in buffer:
        print(f'{n} -> {n.next}')


if __name__ == '__main__':
    solve()
