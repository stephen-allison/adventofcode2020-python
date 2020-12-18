from operator import add, mul

def load_expressions():
    with open('input.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]

ops = {
    '+': add,
    '*': mul
}

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

        if c in ops.keys():
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


def evaluate(expression):
    i, s = scan_expression(expression)
    exp = list_to_expr(s, build)
    ans = exp.eval()
    return ans


def list_to_expr(expr_list, builder):
    exprs = []
    for item in expr_list:
        if type(item) == list:
            ex = list_to_expr(item, builder)
        elif item in ops.keys():
            ex = item
        else:
            ex = Num(item)
        exprs.append(ex)
    return builder(exprs)


def build(exprs):
    expr_iter = iter(exprs)
    last = None
    ex = None
    for item in expr_iter:
        if item in ops.keys():
            ex = Expr(left=last, right=next(expr_iter), op=ops[item])
            last = ex
        else:
            last = item
    return ex


def build2(exprs):
    expr_iter = iter(exprs)
    last = None
    ex = None
    for item in expr_iter:
        if item in ops.keys():
            ex = Expr(left=last, right=next(expr_iter), op=ops[item])
            last = ex
        else:
            last = item
    return ex


def solve():
    assert evaluate('2 * 3 + (4 * 5)') == 26
    assert evaluate('1 + ((2 * 5) + 3) + 9') == 23
    assert evaluate('1 + (2 * 3) + (4 * (5 + 6))') == 51
    assert evaluate('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632
    answers = [evaluate(exp) for exp in load_expressions()]
    print(f'part one answer = {sum(answers)}')


def test():
    i, out = scan_expression('7 + 2 * (3 + 1 * 2)')
    print(out)
    ex = list_to_expr(out, build)
    print(ex.eval())


if __name__ == '__main__':
    test()
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