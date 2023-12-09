#!/usr/bin/env python
import functools
import operator
import pathlib


class Race:

    def __init__(self, time: int, record: int):
        self.time = time
        self.record = record

    def hold_to_distance(self, hold: int) -> int:
        if hold == 0 or hold >= self.time:
            return 0
        travel_time = self.time - hold
        return travel_time * hold

    def ways_to_beat(self) -> int:
        ways = 0
        hold = 0
        while self.hold_to_distance(hold) <= self.record:
            hold += 1
        while self.hold_to_distance(hold) > self.record:
            ways += 1
            hold += 1
        return ways


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


def line_to_nums(line: str) -> list[int]:
    nums = []
    _, ts = line.split(':')
    for t in ts.split():
        nums.append(int(t.strip()))
    return nums


def load_races() -> list[Race]:
    lines = load_lines()
    times = line_to_nums(lines[0])
    distances = line_to_nums(lines[1])
    races = []
    for index in range(len(times)):
        races.append(Race(times[index], distances[index]))
    return races


def line_to_num(line: str) -> int:
    _, ts = line.split(':')
    nums = []
    for t in ts.split():
        nums.append(t.strip())
    return int(''.join(nums))


def load_race() -> Race:
    lines = load_lines()
    time = line_to_num(lines[0])
    distance = line_to_num(lines[1])
    return Race(time, distance)


def part1():
    ways = []
    for r in load_races():
        ways.append(r.ways_to_beat())
    return functools.reduce(operator.mul, ways)


def part2():
    race = load_race()
    return race.ways_to_beat()


def main():
    print('day06')

    p1 = part1()
    print(f'  part 1: {p1}')

    p2 = part2()
    print(f'  part 2: {p2}')


if __name__ == '__main__':
    main()
