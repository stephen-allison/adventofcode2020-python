from operator import add, mul
from functools import partial

OPS = {'+': add, '*': mul}
SUBEXPR_START = '('
SUBEXPR_END = ')'
V1_PRECEDENCE = [['+', '*']]
V2_PRECEDENCE = [['+'], ['*']]


def load_expressions():
    with open('input.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]


class Expr:
    def __init__(self, left=None, right=None, op=None):
        self._left = left
        self._right = right
        self._op = op

    def eval(self):
        return self._op(self._left.eval(), self._right.eval())

    def __str__(self):
        return f'expr: L:{self._left} Op:{self._op} R:{self._right}'


class Num:
    def __init__(self, val):
        self.val = int(val)

    def eval(self):
        return self.val

    def __str__(self):
        return f'Num({self.val})'


def tokenize(expression):
    digits = []
    tokens = []

    def store_number_token():
        if digits:
            n = (int(''.join(digits)))
            tokens.append(n)
            digits[:] = []

    for c in expression:
        if c in '0123456789':
            digits.append(c)
        else:
            if digits:
                store_number_token()
            if c in OPS or c in (SUBEXPR_START, SUBEXPR_END):
                tokens.append(c)

    store_number_token()

    return tokens


def build_expression(tokens, builder, start=0, expression_end=None):
    exprs = []
    i = start
    while i < len(tokens):
        item = tokens[i]
        if item == SUBEXPR_START:
            i, ex = build_expression(tokens, builder, i + 1, SUBEXPR_END)
        elif item == expression_end:
            break
        elif item in OPS:
            ex = item
        else:
            ex = Num(item)
        exprs.append(ex)
        i += 1
    return i, builder(exprs)


def group_expressions(precedence, exprs):
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
    s = tokenize(expression)
    _, exp = build_expression(s, builder)
    ans = exp.eval()
    return ans


def solve():
    builder = partial(group_expressions, V1_PRECEDENCE)

    assert evaluate('2 * 3 + (4 * 5)', builder) == 26
    assert evaluate('1 + ((2 * 5) + 3) + 9', builder) == 23
    assert evaluate('1 + (2 * 3) + (4 * (5 + 6))', builder) == 51

    answers = [evaluate(exp, builder) for exp in load_expressions()]
    print(f'part one answer = {sum(answers)}')

    builder2 = partial(group_expressions, V2_PRECEDENCE)
    answers = [evaluate(exp, builder2) for exp in load_expressions()]
    print(f'part two answer = {sum(answers)}')


if __name__ == '__main__':
    solve()

'''
2 * 3 + (4 * 5)

Part two tree:
  *
 / \
2   +
   3 \
      *
     4 5
Part one tree:
   +
  / \
 *   *
2 3 4 5

Part one tree:
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
