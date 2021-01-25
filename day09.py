#!/usr/bin/env python
import itertools
import readline
import sys
from collections import deque


class State:
    def __init__(self, program, stdin=None):
        self.mem = dict(enumerate(program))
        self.stdin = deque(stdin or list())
        self.ip = 0
        self.relative_base = 0
        self.program_size = len(program)


def vm_run(state, add_stdin=None):
    ip = state.ip
    ip_bound = state.program_size
    relative_base = state.relative_base
    stdout = deque()
    mem = state.mem
    stdin = state.stdin
    if add_stdin:
        stdin.extend(add_stdin)
    waiting_input = False

    def load_value(off, mode):
        if mode == 0:
            return mem.get(mem[off], 0)
        elif mode == 1:
            return mem[off]
        elif mode == 2:
            return mem.get(relative_base + mem[off])
        else: raise Exception(f'unhandled mode {mode}')

    def store_value(x, off, mode):
        if mode == 0:
            mem[mem[off]] = x
        elif mode == 2:
            mem[relative_base + mem[off]] = x
        else: raise Exception(f'unhandled mode {mode}')

    def has_input():
        return len(stdin) > 0

    def read_input():
        if stdin is not None:
            return stdin.popleft()
        else:
            return int(input('> '))

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
        nonlocal ip, waiting_input
        if has_input():
            x = read_input()
            store_value(x, ip + 1, modes[0])
            ip += 2
        else:
            waiting_input = True

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

    def op_base(modes):
        nonlocal ip, relative_base
        relative_base += load_value(ip + 1, modes[0])
        ip += 2

    opcodes = {
        1: op_add,
        2: op_mul,
        3: op_in,
        4: op_out,
        5: op_jt,
        6: op_jf,
        7: op_lt,
        8: op_eq,
        9: op_base,
        99: op_halt,
    }

    while 0 <= ip < ip_bound and not waiting_input:
        op = mem[ip]
        modes, op = divmod(op, 100)
        modes = [(modes // (10 ** i) % 10) for i in range(3)]
        f = opcodes[op]
        f(modes)

    state.ip = ip
    state.relative_base = relative_base
    return list(stdout)


def solve(fn='data/day09.txt'):
    with open(fn) as fp:
        data = fp.read()
    program = list(map(int, data.split(',')))

    state = State(program)
    x, = vm_run(state, [1])
    print('Part 1:', x)

    state = State(program)
    x, = vm_run(state, [2])
    print('Part 2:', x)


if __name__ == '__main__':
    solve(*sys.argv[1:])
