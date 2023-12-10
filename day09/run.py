#!/usr/bin/env python
import functools
import operator
import pathlib


class Sequence:
    def __init__(self, line: str) -> None:
        nums = []
        for num in line.split():
            nums.append(int(num.strip()))
        self.nums = nums

    def list_of_zeros(self, nums: list[int]) -> bool:
        for n in nums:
            if n != 0:
                return False
        return True

    def differences(self, nums: list[int]) -> list[int]:
        differences = []
        length = len(nums)
        for index in range(length - 1):
            differences.append(nums[index + 1] - nums[index])
        return differences

    def reduce_to_zeros(self, nums: list[int]) -> list[list[int]]:
        rows: list[list[int]] = []
        rows.append(nums)
        index = 1
        while True:
            differences = self.differences(rows[index - 1])
            if not self.list_of_zeros(differences):
                rows.append(differences)
                index += 1
            else:
                break
        return rows

    def extrapolate(self) -> int:
        rows = self.reduce_to_zeros(self.nums)
        new_rows = []
        last_diff = 0
        for r in reversed(rows):
            last = r[-1]
            if last_diff == 0:
                next_one = last
            else:
                next_one = last + last_diff
            last_diff = next_one
            r.append(next_one)
            new_rows.append(r)
        return new_rows[-1][-1]

    def detrapolate(self) -> int:
        rows = self.reduce_to_zeros(self.nums)
        new_rows = []
        last_diff = 0
        for r in reversed(rows):
            last = r[0]
            if last_diff == 0:
                prev_one = last
            else:
                prev_one = last - last_diff
            last_diff = prev_one
            r.insert(0, prev_one)
            new_rows.append(r)
        return new_rows[-1][0]


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


def load_sequences() -> list[Sequence]:
    sequences = []
    for line in load_lines():
        sequences.append(Sequence(line))
    return sequences


def part1():
    values = []
    sequences = load_sequences()
    for s in sequences:
        values.append(s.extrapolate())
    return functools.reduce(operator.add, values)


def part2():
    values = []
    sequences = load_sequences()
    for s in sequences:
        values.append(s.detrapolate())
    return functools.reduce(operator.add, values)


def main():
    print('day09')
    p1 = part1()
    print(f'  part 1: {p1}')
    p2 = part2()
    print(f'  part 2: {p2}')


if __name__ == '__main__':
    main()
