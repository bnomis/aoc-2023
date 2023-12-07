#!/usr/bin/env python
import pathlib


def load_lines():
    path = pathlib.Path(__file__).absolute().parent
    path = path / 'test.txt'
    lines = []
    with path.open() as fp:
        for line in fp.readlines():
            line = line.strip()
            if line:
                lines.append(line)
    return lines


def part1():
    return 0


def part2():
    return 0


def main():
    p1 = part1()
    p2 = part2()
    print(f'day05\n  part 1: {p1}\n  part 2: {p2}')


if __name__ == '__main__':
    main()
