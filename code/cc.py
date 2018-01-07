#!/usr/bin/python3

def do_it(width, up_height, middle_height, down_height):
    f = lambda c, a: c * (width * a)
    l = lambda o, h: list(o) * h

    def part1(up, h):
        ul = ['.', 'B']
        ur = ['.', 'R']
        dl = ['B', '.']
        dr = ['R', '.']

        return sum([
            l([f(ul[up], 2) + f('b', 1)  + f('.', 3) + f('r', 1) + f(ur[up], 2)], h),
            l([f(ul[up], 1) + f('b', 3)  + f('.', 1) + f('r', 3) + f(ur[up], 1)], h),
            l([f('b', 4)  + f('#', 1) + f('r', 4)], h),
            l([f(dl[up], 1) + f('b', 2) + f('#', 3) + f('r', 2) + f(dr[up], 1)], h),
            l([f(dl[up], 2) + f('#', 5) + f(dr[up], 2)], h),
            l([f(dl[up], 2) + f('.', 1) + f('#', 3) + f('.', 1) + f(dr[up], 2)], h),
            l([f(dl[up], 2) + f('.', 2) + f('#', 1) + f('.', 2) + f(dr[up], 2)], h),
        ], [])

    def part2():
        return [f('B', 2) + f('.', 5) + f('R', 2)] * middle_height

    xx = part1(0, up_height) + part2() + part1(1, down_height)
    d = {
        '.': '\033[30m ',
        '#': '\033[34m█',
        'b': '\033[94m█',
        'B': '\033[96m█',
        'r': '\033[31m█',
        'R': '\033[91m█',
    }
    return '\n'.join(''.join(d[x] for x in xxx) for xxx in xx) + '\n'

if __name__ == "__main__":
    from sys import argv
    width = int(argv[1])
    up_height = int(argv[2])
    middle_height = int(argv[3])
    down_height = int(argv[4])
    print(do_it(width, up_height, middle_height, down_height), end='')
