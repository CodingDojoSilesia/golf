#!/usr/bin/python3
from math import ceil, sqrt

from random import sample
from string import ascii_letters

cc = ascii_letters
rr = range(1, 10, 2)

WIDTH = 60  # height = 45
ARGS = [
    f'{name},{c},{x}'
    for c in cc
    for x in rr
    for name in ['zigzag', 'cross']
] + [
    f'{name},{c},{x},{y}'
    for c in cc
    for x in range(1, 4, 2)
    for y in range(1, 4, 2)
    for name in ['maze', 'hstrip']
] + [
    f'empty,{x}'
    for x in rr
] + [
    f'vstrip,{c}'
    for c in cc
]


def make_arguments():
    samples = sample(ARGS, 15 * 10)
    return [
        [':'.join(samples[i*15:(i+1)*15])]
        for i in range(20)
    ]


def do_it(args):
    drawer = Drawer()
    drawer.draw(args)
    return drawer.buf


class Drawer:
    width: int
    height: int
    maskoff: bool
    counter: int
    funcs: dict
    buf: str

    def make_funcs(self):
        return {
            'zigzag': self.draw_zigzag,
            'maze': self.draw_maze,
            'empty': self.draw_empty,
            'cross': self.draw_cross,
            'hstrip': self.draw_hstrip,
            'vstrip': self.draw_vstrip,
            'maskoff': self.set_maskoff,
        }

    def __init__(self, width=WIDTH):
        self.funcs = self.make_funcs()
        self.counter = 0
        self.maskoff = False
        self.buf = ''
        self.width = width
        self.height = width // 2 + width // 4

    def draw(self, main_args):
        self.buf = ''
        for arg in main_args.split(':'):
            if not arg:
                continue
            name, *args = arg.split(',')
            func = self.funcs[name]
            func(*args)
        self.draw_empty(self.height - self.counter)

    def _draw(self, s):
        data = self._crop_line(s)
        if data:
            self.buf += f'{data}\n'

    def _crop_line(self, s):
        if self.counter >= self.height:
            return None
        s *= ceil(self.width / len(s))
        s = s[:self.width]
        if self.maskoff:
            self.counter += 1
            return s
        mask = self.get_mask(self.counter)
        self.counter += 1
        return ''.join(a if b == '.' else b for a, b in zip(s, mask))

    def compute_x(self, y):
        half_w = self.width // 2
        quart_w = self.width // 4
        height = half_w + quart_w
        if y < half_w:
            x = sqrt(half_w**2 - (y - half_w)**2)
        elif y <= height:
            y = height - y
            x = sqrt(half_w**2 - (y * 2 - half_w)**2)
        else:
            return 0
        return round(x)

    def get_mask(self, y):
        half_w = self.width // 2
        x1 = self.compute_x(y)
        x2 = self.compute_x(y + 1)
        if x2 < x1:
            x2, x1 = x1, x2
        d = max(x2 - x1, 1)
        s1 = ' ' * (half_w - x1 - d) + '@' * d
        s2 = '.' * (half_w - len(s1))
        s = s1 + s2
        return s + s[::-1]

    def draw_zigzag(self, c, ww):
        ww = int(ww)
        for w in range(ww):
            s = ' ' * w + c + ' ' * (ww - w)
            s += ' ' * (ww - w - 1) + c + ' ' * w
            self._draw(s)

    def draw_maze(self, c, ww, hh):
        ww = int(ww)
        hh = int(hh)
        for h in range(hh):
            if h == hh - 1:
                s = c * ww
            else:
                s = c + ' ' * (ww - 1)
            if h == 0:
                s += c * ww
            else:
                s += c + ' ' * (ww - 1)
            self._draw(s)

    def draw_empty(self, ww):
        ww = int(ww)
        for w in range(ww):
            self._draw(' ')

    def draw_cross(self, c, ww):
        ww = int(ww)
        ww2 = ww // 2
        for w in range(ww):
            if w == ww2:
                s = c * ww + ' '
            else:
                s = ' ' * ww2 + c + ' ' * ww2 + ' '
            self._draw(s)

    def draw_hstrip(self, c, hh, shift):
        hh = int(hh)
        shift = int(shift)
        for h in range(hh):
            s = c + ' ' * shift
            self._draw(s)

    def draw_vstrip(self, c):
        self._draw(c)

    def set_maskoff(self):
        if self.counter == 0:
            self.maskoff = True


if __name__ == "__main__":
    from sys import argv, stdout
    if len(argv) < 2:
        main_args = ''
    else:
        main_args = argv[1]
    result = do_it(main_args)
    stdout.write(result)
