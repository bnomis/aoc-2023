#!/usr/bin/env python
import pathlib

import numpy


def prev_is_north(prev: list[int], current: list[int]) -> bool:
    return prev[1] < current[1]


def prev_is_south(prev: list[int], current: list[int]) -> bool:
    return prev[1] > current[1]


def prev_is_east(prev: list[int], current: list[int]) -> bool:
    return prev[0] > current[0]


def prev_is_west(prev: list[int], current: list[int]) -> bool:
    return prev[0] < current[0]


def pipe_to_next(prev: list[int], current: list[int], pipe: str) -> list[int]:
    if pipe == '|':
        return vertical_pipe_to_next(prev, current)
    if pipe == '-':
        return horizontal_pipe_to_next(prev, current)
    if pipe == 'L':
        return l_pipe_to_next(prev, current)
    if pipe == 'J':
        return j_pipe_to_next(prev, current)
    if pipe == '7':
        return seven_pipe_to_next(prev, current)
    if pipe == 'F':
        return f_pipe_to_next(prev, current)
    raise Exception(f'Unknown pipe {pipe}')


def vertical_pipe_to_next(prev: list[int], current: list[int]) -> list[int]:
    if prev_is_south(prev, current):
        return go_north(current)
    return go_south(current)


def horizontal_pipe_to_next(prev: list[int], current: list[int]) -> list[int]:
    if prev_is_east(prev, current):
        return go_west(current)
    return go_east(current)


def l_pipe_to_next(prev: list[int], current: list[int]) -> list[int]:
    if prev_is_north(prev, current):
        return go_east(current)
    return go_north(current)


def j_pipe_to_next(prev: list[int], current: list[int]) -> list[int]:
    if prev_is_north(prev, current):
        return go_west(current)
    return go_north(current)


def seven_pipe_to_next(prev: list[int], current: list[int]) -> list[int]:
    if prev_is_south(prev, current):
        return go_west(current)
    return go_south(current)


def f_pipe_to_next(prev: list[int], current: list[int]) -> list[int]:
    if prev_is_south(prev, current):
        return go_east(current)
    return go_south(current)


def go_north(coord: list[int]) -> list[int]:
    return [coord[0], coord[1] - 1]


def go_south(coord: list[int]) -> list[int]:
    return [coord[0], coord[1] + 1]


def go_east(coord: list[int]) -> list[int]:
    return [coord[0] + 1, coord[1]]


def go_west(coord: list[int]) -> list[int]:
    return [coord[0] - 1, coord[1]]


def pipe_connects_north(pipe: str) -> bool:
    return pipe in ['|', 'L', 'J']


def pipe_connects_south(pipe: str) -> bool:
    return pipe in ['|', '7', 'F']


def pipe_connects_east(pipe: str) -> bool:
    return pipe in ['-', 'L', 'F']


def pipe_connects_west(pipe: str) -> bool:
    return pipe in ['-', 'J', '7']


def tile_at(tiles: list[str], coord: list[int]) -> str:
    return tiles[coord[1]][coord[0]]


def tile_connects_north(tiles: list[str], coord: list[int]) -> bool:
    return pipe_connects_north(tile_at(tiles, coord))


def tile_connects_south(tiles: list[str], coord: list[int]) -> bool:
    return pipe_connects_south(tile_at(tiles, coord))


def tile_connects_east(tiles: list[str], coord: list[int]) -> bool:
    return pipe_connects_east(tile_at(tiles, coord))


def tile_connects_west(tiles: list[str], coord: list[int]) -> bool:
    return pipe_connects_west(tile_at(tiles, coord))


def tile_to_next(tiles: list[str], prev: list[int], current: list[int]) -> list[int]:
    pipe = tiles[current[1]][current[0]]
    return pipe_to_next(prev, current, pipe)


def find_s(tiles: list[str]) -> list[int]:
    y = 0
    for row in tiles:
        for x in range(len(row)):
            if tiles[y][x] == 'S':
                return [x, y]
        y += 1
    return [0, 0]


def load_lines() -> list[str]:
    path = pathlib.Path(__file__).absolute().parent
    path = path / 'input.txt'
    lines = []
    with path.open() as fp:
        for line in fp.readlines():
            line = line.strip()
            if line:
                lines.append(line)
    return lines


def load_tiles() -> list[str]:
    return load_lines()


def can_go_north(tiles: list[str], coord: list[int]) -> bool:
    return coord[1] > 0


def can_go_south(tiles: list[str], coord: list[int]) -> bool:
    return coord[1] < len(tiles)


def can_go_west(tiles: list[str], coord: list[int]) -> bool:
    return coord[0] > 0


def can_go_east(tiles: list[str], coord: list[int]) -> bool:
    return coord[0] < len(tiles[0])


def find_connector(tiles: list[str], coord: list[int]):
    if can_go_north(tiles, coord):
        north = go_north(coord)
        if tile_connects_south(tiles, north):
            return north
    if can_go_south(tiles, coord):
        south = go_south(coord)
        if tile_connects_north(tiles, south):
            return south
    if can_go_east(tiles, coord):
        east = go_east(coord)
        if tile_connects_west(tiles, east):
            return east
    if can_go_west(tiles, coord):
        west = go_west(coord)
        if tile_connects_east(tiles, west):
            return west
    raise Exception('Dont know where to go')


def home(home_coord: list[int], coord: list[int]) -> bool:
    return home_coord == coord


def not_home(home_coord: list[int], coord: list[int]) -> bool:
    return not home(home_coord, coord)


def count_steps(tiles: list[str], start: list[int]) -> int:
    prev_tile = start
    next_tile = find_connector(tiles, start)
    steps = 1
    while not_home(start, next_tile):
        next_next_tile = tile_to_next(tiles, prev_tile, next_tile)
        prev_tile = next_tile
        next_tile = next_next_tile
        steps += 1
    return steps


def paint_tile(tiles: list[str], coord: list[int]) -> list[str]:
    s = tiles[coord[1]]
    tiles[coord[1]] = s[:coord[0]] + '@' + s[coord[0] + 1:]
    return tiles


def paint_pipe(tiles: list[str]) -> list[str]:
    start = find_s(tiles)
    prev_tile = start
    next_tile = find_connector(tiles, start)
    tiles = paint_tile(tiles, start)
    while not_home(start, next_tile):
        next_next_tile = tile_to_next(tiles, prev_tile, next_tile)
        prev_tile = next_tile
        tiles = paint_tile(tiles, next_tile)
        next_tile = next_next_tile
    return tiles


def tile_is_straight(tiles: list[str], coord: list[int]) -> bool:
    tile = tile_at(tiles, coord)
    return tile in ['-', '|']


def tile_is_not_straight(tiles: list[str], coord: list[int]) -> bool:
    return not tile_is_straight(tiles, coord)


def tiles_to_path(tiles: list[str]) -> list[list[int]]:
    path = []
    start = find_s(tiles)
    path.append(start)
    prev_tile = start
    next_tile = find_connector(tiles, start)
    while not_home(start, next_tile):
        path.append(next_tile)
        next_next_tile = tile_to_next(tiles, prev_tile, next_tile)
        prev_tile = next_tile
        next_tile = next_next_tile
    return path


def make_det(a: list[int], b: list[int]) -> float:
    a = numpy.array([a, b])
    return numpy.linalg.det(a)


# https://en.wikipedia.org/wiki/Shoelace_formula
def path_to_area(path: list[list[int]]) -> float:
    dets = []
    length = len(path)
    for index in range(length - 1):
        dets.append(make_det(path[index], path[index + 1]))
    dets.append(make_det(path[-1], path[0]))
    return abs(sum(dets) / 2)


# https://en.wikipedia.org/wiki/Pick%27s_theorem
def interior_points(path: list[list[int]], area: float) -> int:
    return int(area - (len(path) / 2) + 1)


def print_tiles(tiles: list[str]):
    for row in tiles:
        print(row)


def part1():
    tiles = load_tiles()
    start = find_s(tiles)
    return int(count_steps(tiles, start) / 2)


def part2():
    tiles = load_tiles()
    path = tiles_to_path(tiles)
    area = path_to_area(path)
    return interior_points(path, area)


def main():
    print('day10')
    p1 = part1()
    print(f'  part 1: {p1}')
    p2 = part2()
    print(f'  part 2: {p2}')


if __name__ == '__main__':
    main()
