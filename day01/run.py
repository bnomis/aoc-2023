#!/usr/bin/env python
import pathlib


def read_lines():
    this_dir = pathlib.Path(__file__).absolute().parent
    path = this_dir / 'input.txt'
    with path.open() as fp:
        lines = fp.readlines()
    return lines


def part1():
    lines = read_lines()
    digits = []
    for li in lines:
        li = li.strip()
        di = []
        for c in li:
            if c.isdigit():
                di.append(c)
        nums = di[0] + di[-1]
        digits.append(int(nums))
    return sum(digits)


def find_num(li, index):
    first_chars = {
        'o': ['one'],
        't': ['two', 'three'],
        'f': ['four', 'five'],
        's': ['six', 'seven'],
        'e': ['eight'],
        'n': ['nine']
    }
    c = li[index]
    for possible in first_chars[c]:
        pos_len = len(possible)
        if li[index:index+pos_len] == possible:
            return possible
    return ''


def part2():
    nums = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
    }

    first_chars = {
        'o': ['one'],
        't': ['two', 'three'],
        'f': ['four', 'five'],
        's': ['six', 'seven'],
        'e': ['eight'],
        'n': ['nine']
    }
    first_char_keys = first_chars.keys()

    lines = read_lines()

    digits = []
    for li in lines:
        li = li.strip()
        di = []
        index = 0
        while index < len(li):
            c = li[index]
            if c.isdigit():
                di.append(c)
            else:
                if c in first_char_keys:
                    num = find_num(li, index)
                    if num:
                        di.append(nums[num])
            index += 1

        num_str = di[0] + di[-1]
        digits.append(int(num_str))

    return sum(digits)


def main():
    p1 = part1()
    p2 = part2()
    print(f'day 01:\n  part 1: {p1}\n  part 2: {p2}')


if __name__ == '__main__':
    main()
