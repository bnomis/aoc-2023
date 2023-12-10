#!/usr/bin/env python
import enum
import functools
import operator
import pathlib


class HandType(enum.IntEnum):
    NONE = 0
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7


hand_type_enum_to_str = {
    HandType.NONE: 'none',
    HandType.FIVE_OF_A_KIND: 'five',
    HandType.FOUR_OF_A_KIND: 'four',
    HandType.FULL_HOUSE: 'full',
    HandType.THREE_OF_A_KIND: 'three',
    HandType.TWO_PAIR: 'two',
    HandType.ONE_PAIR: 'one',
    HandType.HIGH_CARD: 'high',
}


class Hand:
    CARD_LABELS = [
        'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'
    ]

    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid
        self._type = HandType.NONE
        self._labels = None

    def __str__(self) -> str:
        return f'{self.cards} {self.bid} {hand_type_enum_to_str[self._type]} {self._labels}'

    def get_labels(self) -> list[int]:
        if self._labels is None:
            self._labels = self.make_labels()
        return self._labels

    def make_labels(self) -> list[int]:
        labels = []
        for c in self.cards:
            for index in range(len(self.CARD_LABELS)):
                if self.CARD_LABELS[index] == c:
                    labels.append(index)
                    break
        return labels

    def get_hand_type(self) -> HandType:
        if self._type == HandType.NONE:
            self._type = self.make_hand_type()
        return self._type

    def make_labels_dict(self) -> dict:
        labels = {}
        for c in self.cards:
            if c not in labels:
                labels[c] = 0
            labels[c] += 1
        return labels

    def make_counts_dict(self, labels: dict) -> dict:
        counts = {}
        for k, v in labels.items():
            counts[v] = k
        return counts

    def make_hand_type(self) -> HandType:
        labels = self.make_labels_dict()
        label_count = len(labels)
        if label_count == 1:
            return HandType.FIVE_OF_A_KIND
        if label_count == 5:
            return HandType.HIGH_CARD

        counts = self.make_counts_dict(labels)
        sorted_counts = sorted(counts.keys(), reverse=True)
        if sorted_counts[0] == 4:
            return HandType.FOUR_OF_A_KIND
        if label_count == 2:
            return HandType.FULL_HOUSE
        if sorted_counts[0] == 3:
            return HandType.THREE_OF_A_KIND
        if label_count == 3:
            return HandType.TWO_PAIR
        return HandType.ONE_PAIR

    def __eq__(self, other):
        self_type = self.get_hand_type()
        other_type = other.get_hand_type()
        if self_type == other_type:
            self_labels = self.get_labels()
            other_labels = other.get_labels()
            for index in range(len(self_labels)):
                if self_labels[index] != other_labels[index]:
                    return False
            return True
        return False

    def __lt__(self, other):
        self_type = self.get_hand_type()
        other_type = other.get_hand_type()
        if self_type == other_type:
            self_labels = self.get_labels()
            other_labels = other.get_labels()
            for index in range(len(self_labels)):
                if self_labels[index] == other_labels[index]:
                    continue
                if self_labels[index] > other_labels[index]:
                    return True
                return False
        return self_type > other_type

    def __gt__(self, other):
        self_type = self.get_hand_type()
        other_type = other.get_hand_type()
        if self_type == other_type:
            self_labels = self.get_labels()
            other_labels = other.get_labels()
            for index in range(len(self_labels)):
                if self_labels[index] == other_labels[index]:
                    continue
                if self_labels[index] < other_labels[index]:
                    return True
                return False
        return self_type < other_type


class Hand2(Hand):
    CARD_LABELS = [
        'A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'
    ]

    def count_jokers(self) -> int:
        count = 0
        for c in self.cards:
            if c == 'J':
                count += 1
        return count

    def make_hand_type(self) -> HandType:
        joker_count = self.count_jokers()
        if joker_count == 0:
            return super().make_hand_type()
        if joker_count in [4, 5]:
            return HandType.FIVE_OF_A_KIND
        labels = self.make_labels_dict()
        del labels['J']
        label_count = len(labels)
        if label_count == 1:
            return HandType.FIVE_OF_A_KIND
        card_count = 5 - joker_count
        # two different cards + 3 jokers
        if card_count == 2:
            return HandType.FOUR_OF_A_KIND
        # three cards + 2 jokers
        if card_count == 3:
            # three different labels
            if label_count == 3:
                return HandType.THREE_OF_A_KIND
            # two labels
            return HandType.FOUR_OF_A_KIND
        # four cards + 1 joker
        if label_count == 4:
            return HandType.ONE_PAIR
        # AABC + J
        if label_count == 3:
            return HandType.THREE_OF_A_KIND
        # AABB + J or ABBB + J
        if list(labels.values())[0] == 2:
            return HandType.FULL_HOUSE
        return HandType.FOUR_OF_A_KIND


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


def load_hands() -> list[Hand]:
    hands = []
    for line in load_lines():
        cards, bid = line.split()
        h = Hand(cards, int(bid))
        h.get_hand_type()
        h.get_labels()
        hands.append(h)
    return hands


def load_hands2() -> list[Hand2]:
    hands = []
    for line in load_lines():
        cards, bid = line.split()
        h = Hand2(cards, int(bid))
        h.get_hand_type()
        h.get_labels()
        hands.append(h)
    return hands


def part1():
    scores = []
    hands = sorted(load_hands())
    index = 1
    for h in hands:
        # print(h)
        scores.append(index * h.bid)
        index += 1
    return functools.reduce(operator.add, scores)


def part2():
    scores = []
    hands = sorted(load_hands2())
    index = 1
    for h in hands:
        # if h.count_jokers() > 0:
        #     print(h)
        scores.append(index * h.bid)
        index += 1
    return functools.reduce(operator.add, scores)


def main():
    print('day07')
    p1 = part1()
    print(f'  part 1: {p1}')
    p2 = part2()
    print(f'  part 2: {p2}')


if __name__ == '__main__':
    main()
