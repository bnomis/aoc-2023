#!/usr/bin/env python
import pathlib


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


def nums_to_set(nums):
    my = set()
    for w in nums.split():
        w = int(w.strip())
        my.add(w)
    return my


def parse_line(line):
    card, nums = line.split(':')
    _, card_num = card.split()
    card_num = int(card_num.strip())
    winners, mine = nums.split('|')
    wins = nums_to_set(winners)
    my = nums_to_set(mine)
    return {
        'card': card_num,
        'winners': wins,
        'mine': my,
    }


def load_parsed_lines():
    lines = []
    for line in load_lines():
        lines.append(parse_line(line))
    return lines


def get_wins(line):
    return line['winners'] & line['mine']


def count_wins(line):
    return len(get_wins(line))


def wins_to_score(wins):
    if wins == 0:
        return 0

    value = 1
    for _ in range(wins - 1):
        value = value * 2
    return value


def part1():
    scores = []
    for line in load_lines():
        d = parse_line(line)
        wins = count_wins(d)
        score = wins_to_score(wins)
        scores.append(score)
    return sum(scores)


def lines_to_wins(lines):
    wins = []
    for line in lines:
        wins.append(count_wins(line))
    return wins


def card_to_copies(wins, card):
    copies = []
    for i in range(wins[card]):
        copies.append(card + 1 + i)
    return copies


def cards(wins, card, total):
    total += 1
    copies = card_to_copies(wins, card)
    if not copies:
        return total
    for c in copies:
        total = cards(wins, c, total)
    return total


def part2():
    wins = lines_to_wins(load_parsed_lines())
    total = 0
    for i in range(len(wins)):
        total += cards(wins, i, 0)
    return total


def main():
    p1 = part1()
    p2 = part2()
    print(f'day04\n  part 1: {p1}\n  part 2: {p2}')


if __name__ == '__main__':
    main()
