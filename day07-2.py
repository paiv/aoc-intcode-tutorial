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


def vm_run(state, add_stdin=None):
    ip = state.ip
    stdout = deque()
    mem = state.mem
    stdin = state.stdin
    if add_stdin:
        stdin.extend(add_stdin)
    waiting_input = False

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

    while 0 <= ip < len(mem) and not waiting_input:
        op = mem[ip]
        modes, op = divmod(op, 100)
        modes = [(modes // (10 ** i) % 10) for i in range(3)]
        f = opcodes[op]
        f(modes)

    state.ip = ip
    return list(stdout)


def solve(fn='data/day07.txt'):
    with open(fn) as fp:
        data = fp.read()
    program = list(map(int, data.split(',')))

    def run_amplifier(phase=None):
        state = [State(program, stdin=[x]) for x in phase]
        sig = [0]
        while any(s.ip >= 0 for s in state):
            for s in state:
                sig = vm_run(s, sig)
        return sig

    x = max(map(run_amplifier, itertools.permutations(range(5, 10))))
    print('Part 2:', x)


if __name__ == '__main__':
    solve(*sys.argv[1:])
