#!/usr/bin/env python
import sys


def run_program(program, patch=None):
    ip = 0
    mem = dict(enumerate(program))

    if patch:
        for i, v in patch.items():
            mem[i] = v

    def op_add(x, y, z):
        nonlocal mem, ip
        mem[z] = mem[x] + mem[y]
        ip += 4

    def op_mul(x, y, z):
        nonlocal mem, ip
        mem[z] = mem[x] * mem[y]
        ip += 4

    def op_halt(*args):
        nonlocal ip
        ip = -1

    opcodes = {
        1: op_add,
        2: op_mul,
        99: op_halt,
    }

    while 0 <= ip < len(program):
        op = mem[ip]
        f = opcodes[op]
        f(mem[ip+1], mem[ip+2], mem[ip+3])

    return mem[0]


def solve(fn='data/day02.txt'):
    with open(fn) as fp:
        data = fp.read()
    program = list(map(int, data.split(',')))

    patch = {1:12, 2:2}
    x = run_program(program, patch)
    print('Part 1:', x)

    goal = 19690720

    for a in range(100):
        for b in range(100):
            patch = {1: a, 2: b}
            x = run_program(program, patch)
            if x == goal:
                print('Part 2:', 100 * a + b, (a, b))
                return

    # example binary search part 2
    (la, lb), (ra, rb) = (0, 0), (99, 99)
    while (la, lb) <= (ra, rb):
        if la == ra:
            a, b = la, (lb + rb) // 2
        else:
            a, b = (la + ra) // 2, 0

        patch = {1: a, 2: b}
        x = run_program(program, patch)
        if x == goal:
            print('Part 2:', 100 * a + b)

        if x > goal:
            if b > 0:
                ra, rb = a, b - 1
            else:
                ra, rb = a - 1, 99
        else:
            if b < 99:
                la, lb = a, b + 1
            else:
                la, lb = a + 1, 0


if __name__ == '__main__':
    solve(*sys.argv[1:])
