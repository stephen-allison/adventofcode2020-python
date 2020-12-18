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

    def set_arg(self, expr):
        if self._left:
            self._right = expr
        else:
            self._left = expr

    def complete(self):
        return self._left and self._right and self.op

    def __str__(self):
        return f'expr: L:{self._left} O:{self.op} R:{self._right}'

    def __repr__(self):
        return str(self)


class Num:
    def __init__(self, val):
        self.val = int(val)

    def eval(self):
        return self.val

    def __str__(self):
        return f'Num({self.val})'

    def __repr__(self):
        return str(self)


def scan_expression(expression, depth=0):
    buffer = []
    output = []
    i = 0
    expr = Expr()
    while i < len(expression):
        c = expression[i]
        if expr.complete() and c != ')':
            expr = Expr(left=expr)

        if c in '0123456789':
            buffer.append(c)
        elif buffer:
            n = (int(''.join(buffer)))
            output.append(n)
            expr.set_arg(Num(n))
            buffer = []

        if c in ops.keys():
            output.append(c)
            expr.op = ops[c]

        if c == '(':
            shift, scan, sub_expr = scan_expression(expression[i+1:], depth+1)
            i += (shift + 1)
            output.append(scan)
            expr.set_arg(sub_expr)

        elif c == ')':
            if depth > 0:
                return i, output, expr
        i += 1

    if buffer:
        n = (int(''.join(buffer)))
        output.append(n)
        expr.set_arg(Num(n))
        buffer = []

    return i, output, expr


def evaluate(expression):
    i, s, exp = scan_expression(expression)
    ans = (exp.eval())
    print(f'{expression} = {ans}')
    print(s)
    print(exp)
    ex2 = list_to_expr(s)
    ans2 = ex2.eval()
    assert ans == ans2
    return ans

def test():
    i, out, expr = scan_expression('7 + 2 * (3 + 1 * 2)')
    print(out)
    ex = list_to_expr(out)
    print(ex.eval())


def list_to_expr(expr_list):
    exprs = []
    for item in expr_list:
        if type(item) == list:
            ex = list_to_expr(item)
        elif item in ops.keys():
            ex = item
        else:
            ex = Num(item)
        exprs.append(ex)

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


if __name__ == '__main__':
    solve()
    #test()

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
