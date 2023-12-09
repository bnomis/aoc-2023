#!/usr/bin/env python
import pathlib
from typing import Self


class Mapper:
    def __init__(self, frm: int, too: int, range: int) -> None:
        self.frm = frm
        self.too = too
        self.range = range

    def __str__(self) -> str:
        return f'frm: {self.frm} too: {self.too} ran: {self.range}'

    def map(self, frm: int) -> int:
        if frm < self.frm:
            return -1
        if frm > self.frm + self.range - 1:
            return -1
        offset = frm - self.frm
        return self.too + offset

    def reverse(self) -> Self:
        return Mapper(self.too, self.frm, self.range)


class Category:
    def __init__(self, mappers: list[Mapper]):
        self.mappers = mappers

    def __str__(self) -> str:
        lines = []
        lines.append('Category')
        for m in self.mappers:
            lines.append(f'  {m}')
        return '\n'.join(lines)

    def map(self, frm: int) -> int:
        for m in self.mappers:
            too = m.map(frm)
            if too != -1:
                return too
        return frm

    def mapper_count(self) -> int:
        return len(self.mappers)

    def reverse(self) -> Self:
        mappers = []
        for m in self.mappers:
            mappers.append(m.reverse())
        return Category(mappers)


class Config:
    def __init__(
        self,
        seeds: list[int],
        categories: list[Category],
    ):
        self.seeds = seeds
        self.categories = categories

    def __str__(self) -> str:
        lines = []
        lines.append(f'seeds: {self.seeds}')
        for c in self.categories:
            lines.append(f'  {c}')
        return '\n'.join(lines)

    def seed2loc(self, seed: int) -> int:
        value = seed
        for c in self.categories:
            value = c.map(value)
        return value

    def lowest_location(self) -> int:
        locs = []
        for s in self.seeds:
            locs.append(self.seed2loc(s))
        return min(locs)

    def reverse(self) -> Self:
        categories = []
        for c in reversed(self.categories):
            categories.append(c.reverse())
        return Config(self.seeds, categories)


class Ranger:
    def __init__(self, start: int, range: int):
        self.start = start
        self.range = range

    def __contains__(self, item):
        if item < self.start:
            return False
        if item > self.start + self.range - 1:
            return False
        return True


class Rangers:
    def __init__(self, ranges):
        self.ranges = ranges

    def __contains__(self, item):
        for r in self.ranges:
            if item in r:
                return True
        return False


def load_lines():
    path = pathlib.Path(__file__).absolute().parent
    path = path / 'input.txt'
    lines = []
    with path.open() as fp:
        for line in fp.readlines():
            line = line.strip()
            if line:
                lines.append(line)
    return lines


def parse_seeds_line(line):
    _, ss = line.split(':')
    seeds = []
    for s in ss.split():
        seeds.append(int(s.strip()))
    return seeds


def parse_mapper(line) -> Mapper:
    too, frm, ran = line.split()
    too = int(too.strip())
    frm = int(frm.strip())
    ran = int(ran.strip())
    return Mapper(frm, too, ran)


def parse_category(lines, index) -> Category:
    mappers = []
    while index < len(lines):
        line = lines[index]
        if line.endswith('map:'):
            break
        mappers.append(parse_mapper(line))
        index += 1
    return Category(mappers)


def load_config() -> Config:
    seeds = []
    categories = []
    lines = load_lines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith('seeds:'):
            seeds = parse_seeds_line(line)
            index += 1
        elif line.endswith('map:'):
            index += 1
            c = parse_category(lines, index)
            index += c.mapper_count()
            categories.append(c)
    return Config(seeds, categories)


def part1():
    config = load_config()
    return config.lowest_location()


def part2():
    config = load_config()
    rev = config.reverse()
    ranges = []
    seed_count = len(config.seeds)
    index = 0
    while index < seed_count:
        ranges.append(Ranger(config.seeds[index], config.seeds[index + 1]))
        index += 2
    rangers = Rangers(ranges)
    location = 0
    while True:
        seed = rev.seed2loc(location)
        if seed in rangers:
            return location
        location += 1
    return 0


def main():
    print('day05')
    p1 = part1()
    print(f'  part 1: {p1}')

    p2 = part2()
    print(f'  part 2: {p2}')


if __name__ == '__main__':
    main()
