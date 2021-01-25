#!/usr/bin/env python
import readline
import sys
from collections import deque


def run_program(program, patch=None, stdin=None, stdout=None):
    ip = 0
    mem = dict(enumerate(program))

    if patch:
        for i, v in patch.items():
            mem[i] = v

    def load_value(off, mode):
        if mode == 0:
            return mem[mem[off]]
        elif mode == 1:
            return mem[off]
        else: raise Exception(f'unhandled mode {mode}')

    def store_value(x, off, mode):
        if mode == 0:
            mem[mem[off]] = x
        else: raise Exception(f'unhandled mode {mode}')

    def read_input_init():
        if stdin is not None:
            sin = iter(stdin)
            return lambda: next(sin)
        return lambda: int(input('> '))
    read_input = read_input_init()

    def write_output(x):
        if stdout is not None:
            stdout.append(x)
        # print(x, end=' ', flush=True, file=sys.stderr)

    def op_add(modes):
        nonlocal ip
        x = load_value(ip + 1, modes[0])
        y = load_value(ip + 2, modes[1])
        store_value(x + y, ip + 3, modes[2])
        ip += 4

    def op_mul(modes):
        nonlocal ip
        x = load_value(ip + 1, modes[0])
        y = load_value(ip + 2, modes[1])
        store_value(x * y, ip + 3, modes[2])
        ip += 4

    def op_halt(*args):
        nonlocal ip
        ip = -1

    def op_in(modes):
        nonlocal ip
        x = read_input()
        store_value(x, ip + 1, modes[0])
        ip += 2

    def op_out(modes):
        nonlocal ip
        x = load_value(ip + 1, modes[0])
        write_output(x)
        ip += 2

    def op_jt(modes):
        nonlocal ip
        x = load_value(ip + 1, modes[0])
        if x != 0:
            ip = load_value(ip + 2, modes[1])
        else:
            ip += 3

    def op_jf(modes):
        nonlocal ip
        x = load_value(ip + 1, modes[0])
        if x == 0:
            ip = load_value(ip + 2, modes[1])
        else:
            ip += 3

    def op_lt(modes):
        nonlocal ip
        x = load_value(ip + 1, modes[0])
        y = load_value(ip + 2, modes[1])
        store_value(1 if x < y else 0, ip + 3, modes[2])
        ip += 4

    def op_eq(modes):
        nonlocal ip
        x = load_value(ip + 1, modes[0])
        y = load_value(ip + 2, modes[1])
        store_value(1 if x == y else 0, ip + 3, modes[2])
        ip += 4

    opcodes = {
        1: op_add,
        2: op_mul,
        3: op_in,
        4: op_out,
        5: op_jt,
        6: op_jf,
        7: op_lt,
        8: op_eq,
        99: op_halt,
    }

    while 0 <= ip < len(program):
        op = mem[ip]
        modes, op = divmod(op, 100)
        modes = [(modes // (10 ** i) % 10) for i in range(3)]
        f = opcodes[op]
        f(modes)

    return mem[0]


def solve(fn='data/day05.txt'):
    with open(fn) as fp:
        data = fp.read()
    program = list(map(int, data.split(',')))

    def run_diagnostic(code):
        stdout = deque()
        run_program(program, stdin=[code], stdout=stdout)
        x = stdout.pop()
        assert sum(stdout) == 0
        return x

    x = run_diagnostic(1)
    print('Part 1:', x)

    x = run_diagnostic(5)
    print('Part 2:', x)


if __name__ == '__main__':
    solve(*sys.argv[1:])
