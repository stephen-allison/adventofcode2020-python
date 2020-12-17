from itertools import product
from pprint import pprint
import re


def load(mask_factory):
    MASK = re.compile('mask = ([01X]{36})')
    MEM = re.compile('mem\[(\d+)\] = (\d+)')
    with open('input.txt', 'r') as f:
        actions = []
        for line in (line.strip() for line in f.readlines()):
            if match := re.match(MASK, line):
                actions.append(mask_factory(*match.groups()))
            elif match := re.match(MEM, line):
                actions.append(Mem(*match.groups()))
        return actions


def expand_mask(mask_str):
    expansions = [('z', 'o')] * mask_str.count('X')
    template = mask_str.replace('X', '%s')
    return [template % replacements for replacements in product(*expansions)]


def factoryV1(mask_str):
    return Mask(mask_str, MaskStrategy('X', '1', '0'))


def factoryV2(mask_str):
    return MaskV2(mask_str, MaskStrategy('0', '1o', 'z'))


class MaskStrategy:
    def __init__(self, unchanged_on, to_one_on, to_zero_on):
        self._unchanged_on = unchanged_on
        self._one_on = to_one_on
        self._zero_on = to_zero_on

    def unchanged(self, c):
        return c in self._unchanged_on

    def to_one(self, c):
        return c in self._one_on

    def to_zero(self, c):
        return c in self._zero_on


class Mask:
    def __init__(self, mask_str, strategy):
        self.mask_str = mask_str
        self.strategy = strategy

    def __repr__(self):
        return f'Mask: {self.mask_str}'

    def apply(self, val):
        bit_mask = 1 << len(self.mask_str) - 1
        masked = 0
        for c in self.mask_str:
            masked <<= 1
            if self.strategy.unchanged(c):
                masked |= (val & bit_mask) > 0
            elif self.strategy.to_one(c):
                masked |= 1
            elif self.strategy.to_zero(c):
                pass
            bit_mask >>= 1
        return masked

    def exec(self, machine):
        machine.mask = self


class MaskV2(Mask):
    def __init__(self, mask_str, strategy):
        self.masks = [Mask(m, strategy) for m in expand_mask(mask_str)]

    def __repr__(self):
        return f'MaskV2 with {len(self.masks)} expansions'

    def apply(self, val):
        return [m.apply(val) for m in self.masks]


class Mem:
    def __init__(self, addr, val):
        self.addr = int(addr)
        self.val = int(val)

    def __repr__(self):
        return f'Mem[{self.addr}] = {self.val}'

    def exec(self, machine):
        machine.set_mem(self.addr, self.val)


class Machine:
    def __init__(self):
        self.memory = {}
        self.mask = None

    def run(self, actions):
        for action in actions:
            action.exec(self)

    def set_mem(self, addr, val):
        masked_val = self.mask.apply(val)
        self.memory[addr] = masked_val

    def mem_sum(self):
        return sum(self.memory.values())


class MachineV2(Machine):
    def set_mem(self, addr, val):
        addrs = self.mask.apply(addr)
        for masked_addr in addrs:
            self.memory[masked_addr] = val


def solve():
    actions = load(mask_factory=factoryV1)
    machine = Machine()
    machine.run(actions)
    print(f'part 1 answer is {machine.mem_sum()}')


def solve2():
    actions = load(mask_factory=factoryV2)
    machine = MachineV2()
    machine.run(actions)
    print(f'part 2 answer is {machine.mem_sum()}')


if __name__ == '__main__':
    solve()
    solve2()
