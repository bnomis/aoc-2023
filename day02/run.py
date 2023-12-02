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


def parse_grab(grab):
    out = {}
    for choice in grab.split(','):
        count, colour = choice.split()
        colour = colour.strip()
        count = int(count.strip())
        out[colour] = count
    return out


def load_games():
    games = []
    for li in read_lines():
        li = li.strip()
        _, content = li.split(':')
        grabs = []
        for grab in content.split(';'):
            grabs.append(parse_grab(grab))
        games.append(grabs)
    return games


def impossible_grab(config, grab):
    for colour, value in grab.items():
        if value > config[colour]:
            return True
    return False


def part1():
    config = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }
    total = 0
    for game, grabs in enumerate(load_games(), start=1):
        possible = True
        for g in grabs:
            if impossible_grab(config, g):
                possible = False
                break
        if possible:
            total += game
    return total


def game_power(game):
    counts = {}
    for g in game:
        for colour, num in g.items():
            if colour not in counts:
                counts[colour] = []
            counts[colour].append(num)
    maxs = []
    for colour, values in counts.items():
        maxs.append(max(values))
    return functools.reduce(operator.mul, maxs)


def part2():
    powers = []
    for game in load_games():
        powers.append(game_power(game))
    return sum(powers)


def main():
    p1 = part1()
    p2 = part2()
    print(f'day 02:\n  part 1: {p1}\n  part 2: {p2}')


if __name__ == '__main__':
    main()
