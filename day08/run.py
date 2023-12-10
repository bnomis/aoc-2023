#!/usr/bin/env python
import math
import pathlib


class Instructions:
    def __init__(self, ins: str) -> None:
        instructs = []
        for s in ins:
            if s == 'L':
                instructs.append(0)
            else:
                instructs.append(1)
        self.instructs = instructs
        self.index = 0
        self.max_index = len(instructs) - 1

    def __str__(self) -> str:
        return f'{self.instructs} {self.index}'

    def __iter__(self):
        return self

    def __next__(self):
        if self.index > self.max_index:
            self.index = 0
        value = self.instructs[self.index]
        self.index += 1
        return value

    def reset_index(self):
        self.index = 0


class Docs:
    def __init__(self, instructs: Instructions, nodes: dict) -> None:
        self.instructs = instructs
        self.nodes = nodes

    def __str__(self) -> str:
        lines = []
        lines.append(f'{self.instructs}')
        for k, v in self.nodes.items():
            lines.append(f'{k} = {v}')
        return '\n'.join(lines)

    def count_steps(self, frm: str, too: str) -> int:
        steps = 0
        node = self.nodes[frm]
        for index in self.instructs:
            next_node = node[index]
            steps += 1
            if next_node == too:
                return steps
            node = self.nodes[next_node]
        return 0

    def simulate(self, frm: str, too: str) -> int:
        # find lcm of all cycles
        starts = []
        for k in self.nodes.keys():
            if k[-1] == frm:
                starts.append(k)
        step_counts = []
        for start in starts:
            current_node = start
            steps = 0
            self.instructs.reset_index()
            for index in self.instructs:
                next_node = self.nodes[current_node][index]
                steps += 1
                if next_node[-1] == too:
                    step_counts.append(steps)
                    break
                current_node = next_node
        return math.lcm(*step_counts)


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


def load_nodes(lines: list[str]) -> dict:
    nodes = {}
    for line in lines:
        frm, dest = line.split('=')
        frm = frm.strip()
        dest = dest.strip()
        dest = dest[1:-1]
        dests = dest.split(',')
        nodes[frm] = [dests[0].strip(), dests[1].strip()]
    return nodes


def load_docs():
    lines = load_lines()
    instructs = Instructions(lines[0])
    nodes = load_nodes(lines[1:])
    return Docs(instructs, nodes)


def part1():
    docs = load_docs()
    return docs.count_steps('AAA', 'ZZZ')


def part2():
    docs = load_docs()
    return docs.simulate('A', 'Z')


def main():
    print('day08')
    p1 = part1()
    print(f'  part 1: {p1}')
    p2 = part2()
    print(f'  part 2: {p2}')


if __name__ == '__main__':
    main()
