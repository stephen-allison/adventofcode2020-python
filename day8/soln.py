from pprint import pprint


def get_code():
    with open('input.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]


def parse_code(lines):
    program = []
    for line in lines:
        tokens = line.split(' ')
        program.append((tokens[0], int(tokens[1])))
    return program


def run(prog):
    index = 0
    acc = 0
    completed = False
    while True:
        instruction, val = prog[index]
        yield index, acc, prog[index]
        next_index = index + 1
        if instruction == 'acc':
            acc += val
        elif instruction == 'jmp':
            next_index = index + val
        index = next_index
        if index == len(prog):
            print(f'end reached acc = {acc}')
            completed = True
            break
        elif index < 0 or index > len(prog):
            print(f'index {index} out of range')
            break


def execute_program(prog):
    executed = set()
    loop = False
    for index, acc, line in run(prog):
        if index in executed:
            loop = True
            break
        else:
            executed.add(index)
    return executed, acc, loop


def solve_1():
    prog = parse_code(get_code())
    executed, acc, loop = execute_program(prog)
    print(f'loop? {loop} when acc = {acc}')
    return executed, acc, loop


def solve_2():
    executed_lines, _, _ = solve_1()
    for line in executed_lines:
        prog = parse_code(get_code())
        cmd, val = prog[line]
        if cmd == 'jmp':
            prog[line] = ('nop', val)
        elif cmd == 'nop':
            prog[line] = ('jmp', val)
        else:
            continue
        _, acc, loop = execute_program(prog)
        if not loop:
            print(f'edited line {line} gives acc = {acc}')
            break


if __name__ == '__main__':
    solve_2()
