#!/usr/bin/python3
from itertools import product
from random import sample


def make_arguments():
    ww = sample(range(18, 100, 2), 4)
    hh = sample(range(14, 100, 2), 4)
    texts = [
        'for you!', 'xxx',  'x' * 30, 'y' * 30,
        'coding-dojo-silesia' * 5, '---___---',
        '(╯°□°╯) ┻━┻', '┻━┻ \(`Д´)/ ┻━┻',
        'for firemark!', 'aaa',  ' ' * 30, '...' * 10,
    ]
    tt = sample(texts, 4)

    return product(tt, ww, hh)


def do_it(text, width, height):
    ss = []
    def f(s, p, l, r=None):
        pp = '{:%s^%d}' % (p, width - 2)
        r = r or l
        return l + pp.format(s) + r

    def g(sl, sr):
        l = (width - len(sl)) // 2
        return (' ' * l) + sl + sr

    special_lines = [
        f(r'(\)\/(/)', '─', '╭', '╮'),
        f('╱╱╱╲╲╲', ' ', '│'),
        f('╱╱╱║║╲╲╲', ' ', '│'),
        f('╱╱`║║║║`╲╲', ' ', '│'),
    ]

    dec = '=' * len(text)
    ff = lambda p: p * (width // 2 - 8)

    ss.append( g(r'.__.', "     {}.={}=.".format(ff(' '), dec)) )
    ss.append( g(r'.(\\//).', "  .{}[ {} ]".format(ff('-'), text)) )
    ss.append( g(r'.(\\()//).', "/ {}'={}='".format(ff(' '), dec)) )

    for line in special_lines:
        ss.append(line)

    hh = (height - 7) // 2 - 1
    for _ in range(hh):
        ss.append(f('║' * 4, ' ', '│'))

    for _ in range(2):
        ss.append(f('╬' * 4, '═', '╞', '╡'))

    for _ in range(hh):
        ss.append(f('║' * 4, ' ', '│'))

    ss.append(f('╨' * 4, '─', '╰', '╯'))

    return '\n'.join(ss) + '\n'


if __name__ == "__main__":
    from sys import argv
    text = argv[1]
    width = int(argv[2])
    height = int(argv[3])
    print(do_it(text, width, height), end='')
