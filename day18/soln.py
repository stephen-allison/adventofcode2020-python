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

    def store_pending_number_token():
        if digits:
            n = (int(''.join(digits)))
            tokens.append(n)
            digits[:] = []

    for c in expression:
        if c in '0123456789':
            digits.append(c)
        else:
            store_pending_number_token()
            if c in OPS or c in (SUBEXPR_START, SUBEXPR_END):
                tokens.append(c)

    store_pending_number_token()
    return tokens


def build_expression(tokens, grouper, start=0, expression_end=None):
    exprs = []
    i = start
    while i < len(tokens):
        token = tokens[i]
        if token == SUBEXPR_START:
            i, ex = build_expression(tokens, grouper, i + 1, SUBEXPR_END)
        elif token == expression_end:
            break
        elif token in OPS:
            ex = token
        else:
            ex = Num(token)
        exprs.append(ex)
        i += 1
    return i, grouper(exprs)


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
    grouper = partial(group_expressions, V1_PRECEDENCE)

    assert evaluate('2 * 3 + (4 * 5)', grouper) == 26
    assert evaluate('1 + ((2 * 5) + 3) + 9', grouper) == 23
    assert evaluate('1 + (2 * 3) + (4 * (5 + 6))', grouper) == 51
    assert evaluate('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', grouper) == 12240

    answers = [evaluate(exp, grouper) for exp in load_expressions()]
    print(f'part one answer = {sum(answers)}')

    grouper = partial(group_expressions, V2_PRECEDENCE)
    assert evaluate('2 * 3 + (4 * 5)', grouper) == 46
    assert evaluate('1 + ((2 * 5) + 3) + 9', grouper) == 23
    assert evaluate('1 + (2 * 3) + (4 * (5 + 6))', grouper) == 51
    assert evaluate('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', grouper) == 669060
    answers = [evaluate(exp, grouper) for exp in load_expressions()]
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
