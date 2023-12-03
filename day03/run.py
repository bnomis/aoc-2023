#!/usr/bin/env python
import functools
import operator
import pathlib


def read_lines():
    this_dir = pathlib.Path(__file__).absolute().parent
    path = this_dir / 'input.txt'
    with path.open() as fp:
        lines = fp.readlines()
    return lines


def load_grid():
    grid = []
    for line in read_lines():
        line = line.strip()
        if line:
            grid.append(line)
    return grid


def is_symbol(grid, x, y):
    if x < 0:
        return False
    if y < 0:
        return False
    line_length = len(grid[y])
    if x > (line_length - 1):
        return False
    if y > (len(grid) - 1):
        return False
    c = grid[y][x]
    if c == '.' or c.isdigit():
        return False
    return True


def adjacent_coords(grid, x, y):
    max_width = len(grid[y]) - 1
    max_height = len(grid) - 1
    coords = []
    if y > 0:
        this_line = y - 1
        if x > 0:
            coords.append([x - 1, this_line])
        coords.append([x, this_line])
        if x < max_width:
            coords.append([x + 1, this_line])
    if x > 0:
        coords.append([x - 1, y])
    if x < max_width:
        coords.append([x + 1, y])
    if y < max_height:
        this_line = y + 1
        if x > 0:
            coords.append([x - 1, this_line])
        coords.append([x, this_line])
        if x < max_width:
            coords.append([x + 1, this_line])
    return coords


def symbol_adjacent(grid, x, y):
    for coord in adjacent_coords(grid, x, y):
        if is_symbol(grid, coord[0], coord[1]):
            return True
    return False


def line_to_num_pos(line):
    nums = []
    length = len(line)
    index = 0
    while index < length:
        if line[index].isdigit():
            num = []
            while index < length and line[index].isdigit():
                num.append(index)
                index += 1
            nums.append(num)
        else:
            index += 1
    return nums


def part1():
    part_nums = []
    grid = load_grid()
    for y, line in enumerate(grid):
        for n in line_to_num_pos(line):
            part = False
            for c in n:
                if symbol_adjacent(grid, c, y):
                    part = True
                    break
            if part:
                ns = []
                for c in n:
                    ns.append(grid[y][c])
                ns = ''.join(ns)
                part_nums.append(int(ns))
    return sum(part_nums)


def isgear(c):
    return c == '*'


def line_to_star_pos(line):
    star_pos = []
    for index in range(len(line)):
        if isgear(line[index]):
            star_pos.append(index)
    return star_pos


def coords_to_num(grid, coords):
    s = ''
    for c in coords:
        s += grid[c[1]][c[0]]
    return int(s)


def part2():
    grid = load_grid()
    # find numbers and stars
    num_pos = {}
    star_pos = {}
    for y, line in enumerate(grid):
        num_pos[y] = line_to_num_pos(line)
        star_pos[y] = line_to_star_pos(line)
    # number co-ords
    nums = []
    for row, num_list in num_pos.items():
        for n in num_list:
            num = []
            for c in n:
                num.append([c, row])
            nums.append(num)
    # ratios
    ratios = []
    for row, stars in star_pos.items():
        for s in stars:
            parts = []
            seen = []
            for coord in adjacent_coords(grid, s, row):
                if coord in seen:
                    continue
                for n in nums:
                    if coord in n:
                        parts.append(n)
                        seen.extend(n)
                        break
            if len(parts) > 1:
                pnum = []
                for p in parts:
                    pnum.append(coords_to_num(grid, p))
                ratios.append(functools.reduce(operator.mul, pnum))
    return sum(ratios)


def main():
    p1 = part1()
    p2 = part2()
    print(f'day 03:\n  part 1: {p1}\n  part 2: {p2}')


if __name__ == '__main__':
    main()
