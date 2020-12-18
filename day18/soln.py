from operator import add, mul
from functools import partial

OPS = {
    '+': add,
    '*': mul
}

V1_PRECEDENCE = [['+', '*']]
V2_PRECEDENCE = [['+'], ['*']]


def load_expressions():
    with open('input.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]


class Expr:
    def __init__(self, left=None, right=None, op=None):
        self._left = left
        self._right = right
        self.op = op

    def eval(self):
        return self.op(self._left.eval(), self._right.eval())

    def __str__(self):
        return f'expr: L:{self._left} O:{self.op} R:{self._right}'


class Num:
    def __init__(self, val):
        self.val = int(val)

    def eval(self):
        return self.val

    def __str__(self):
        return f'Num({self.val})'


def scan_expression(expression, depth=0):
    buffer = []
    output = []
    i = 0

    while i < len(expression):
        c = expression[i]

        if c in '0123456789':
            buffer.append(c)
        elif buffer:
            n = (int(''.join(buffer)))
            output.append(n)
            buffer = []

        if c in OPS:
            output.append(c)

        if c == '(':
            shift, scan = scan_expression(expression[i+1:], depth+1)
            i += (shift + 1)
            output.append(scan)

        elif c == ')':
            if depth > 0:
                return i, output
        i += 1

    if buffer:
        n = (int(''.join(buffer)))
        output.append(n)
        buffer = []

    return i, output


def list_to_expr(expr_list, builder):
    exprs = []
    for item in expr_list:
        if type(item) == list:
            ex = list_to_expr(item, builder)
        elif item in OPS:
            ex = item
        else:
            ex = Num(item)
        exprs.append(ex)
    return builder(exprs)


def build(precedence, exprs):
    for prec in precedence:
        for i in range(len(exprs)):
            item = exprs[i]
            if item in prec:
                left = exprs[i-1]
                right = exprs[i+1]
                op = OPS[item]
                expr = Expr(left=left, right=right, op=op)
                exprs[i-1:i+2] = [None, None, expr]
        exprs = list(filter(None, exprs))
    return exprs[0]


def evaluate(expression, builder):
    i, s = scan_expression(expression)
    exp = list_to_expr(s, builder)
    ans = exp.eval()
    return ans


def solve():
    builder = partial(build, V1_PRECEDENCE)
    assert evaluate('2 * 3 + (4 * 5)', builder) == 26
    assert evaluate('1 + ((2 * 5) + 3) + 9', builder) == 23
    assert evaluate('1 + (2 * 3) + (4 * (5 + 6))', builder) == 51
    answers = [evaluate(exp, builder) for exp in load_expressions()]
    print(f'part one answer = {sum(answers)}')

    builder2 = partial(build, V2_PRECEDENCE)
    answers = [evaluate(exp, builder2) for exp in load_expressions()]
    print(f'part two answer = {sum(answers)}')


if __name__ == '__main__':
    solve()

'''
2 * 3 + (4 * 5)
   +
  / \
 *   *
2 3 4 5

  *
 / \
2   +
   3 \
      *
     4 5

'1 + 2 * 3 + 4 * 5 + 6'
            +
           / 6
          *
         / 5
        +
       / 4
      *
     / 3
    +
   1 2
'''
