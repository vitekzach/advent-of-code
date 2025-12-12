from collections import Counter
from copy import deepcopy
from enum import Enum
from itertools import chain
from typing import Any


class TileColor(Enum):
    red = "#"
    gray = "gray"


class Tile:
    def __init__(self, x: int, y: int, color: TileColor) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.part_of_square: bool = False

    def __str__(self) -> str:
        match self.color:
            case TileColor.gray:
                char = "."
            case TileColor.red:
                char = "#"
            case _:
                char = "?"

        return f"[{self.x},{self.y}]"

    def __repr__(self) -> str:
        return self.__str__()


class Square:
    def __init__(self, t1: Tile, t2: Tile, id: int) -> None:
        self.t1: Tile = t1
        self.t2: Tile = t2
        self.t3 = Tile(t1.x, t2.y, TileColor.gray)
        self.t4 = Tile(t2.x, t1.y, TileColor.gray)
        self.area = (abs(t1.x - t2.x) + 1) * (abs(t1.y - t2.y) + 1)
        self.id = id

    def __str__(self):
        return f"{self.t1}, {self.t2}, {self.t3}, {self.t4}, Area:{self.area}"

    def contains_tile(self, tile: Tile, include_borders: bool = False) -> bool:
        min_xs = min(self.t1.x, self.t2.x)
        max_xs = max(self.t1.x, self.t2.x)
        min_ys = min(self.t1.y, self.t2.y)
        max_ys = max(self.t1.y, self.t2.y)
        if include_borders:
            x_axis = min_xs <= tile.x <= max_xs
            y_axis = min_ys <= tile.y <= max_ys
        else:
            x_axis = min_xs < tile.x < max_xs
            y_axis = min_ys < tile.y < max_ys

        print(self, tile, x_axis and y_axis)
        if x_axis and y_axis:
            return True

        return False


class Line:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return f"[{self.x1},{self.y1}]-[{self.x2},{self.y2}]"

    def coord_on_line(self, x: int, y: int, ignore_x: bool = False) -> bool:
        on_x = x == self.x1 and x == self.x2
        on_y = y == self.y1 and y == self.y2
        if not ignore_x:
            if on_y:
                if min(self.x1, self.x2) <= x <= max(self.x1, self.x2):
                    return True
        if on_x:
            if min(self.y1, self.y2) <= y <= max(self.y1, self.y2):
                return True

        return False

    def __repr__(self):
        return self.__str__()


class Raycast:
    def __init__(self) -> None:
        self.coords: list[list[int]] = []
        self.lines: list[list[int]] = []
        self.lines_unique: list[int] = []

    def add_point(self, coords_x: int, coords_y: int, lines: list[int]):
        self.coords.append([coords_x, coords_y])
        self.lines.append(lines)
        self.lines_unique = list(set(chain.from_iterable(self.lines)))

    def is_inside_polygon(self) -> bool:
        return len(self.lines_unique) % 2 == 1

    def __str__(self):
        return f"R:[{self.coords[0]},{self.coords[1]}], lu:{self.lines_unique}"

    def __repr__(self) -> str:
        return self.__str__()


class Floor:
    def __init__(self) -> None:
        self.tiles: list[Tile] = []
        self.max_dimension = 0
        self.squares: list[Square] = []
        self.lines: list[Line] = []
        self.interesting_xs: list[int] = []

    def load_floor(self, coords: str) -> None:
        lines = coords.split("\n")
        for tile in lines:
            x, y = tile.split(",")
            self.max_dimension = max(self.max_dimension, int(x), int(y))
            tile_obj = Tile(int(x), int(y), TileColor.red)
            self.tiles.append(tile_obj)

        self.tiles = sorted(self.tiles, key=lambda x: (x.y, x.x))

    def build_lines(self) -> None:
        self.lines = []
        x_tiles = sorted(self.tiles, key=lambda x: (x.y, x.x))
        x_unique = list(set([x.x for x in x_tiles]))
        self.interesting_xs = x_unique
        for x_coord in x_unique:
            x_line = [x for x in x_tiles if x.x == x_coord]
            for i in range(0, len(x_line), 2):
                tile_1 = x_line[i]
                tile_2 = x_line[i + 1]
                self.lines.append(Line(tile_1.x, tile_1.y, tile_2.x, tile_2.y))

        y_tiles = sorted(self.tiles, key=lambda x: (x.y, x.x))
        y_unique = list(set([x.y for x in y_tiles]))
        for y_coord in y_unique:
            y_line = [x for x in y_tiles if x.y == y_coord]
            for i in range(0, len(y_line), 2):
                tile_1 = y_line[i]
                tile_2 = y_line[i + 1]
                self.lines.append(Line(tile_1.x, tile_1.y, tile_2.x, tile_2.y))

    def calculate_distances(self) -> None:
        self.squares = []
        id = 0
        for i in range(0, len(self.tiles)):
            for j in range(i + 1, len(self.tiles)):
                d = Square(self.tiles[i], self.tiles[j], id)
                self.squares.append(d)
                id += 1

        self.squares = sorted(self.squares, key=lambda x: -x.area)

    def get_biggest_square(self) -> Square:
        self.calculate_distances()
        self.build_lines()
        return self.squares[0]

    def get_largest_inside_square(self) -> Square | None:
        self.calculate_distances()
        self.build_lines()
        all_squares = len(self.squares)
        for i, square in enumerate(self.squares):
            x = min(square.t1.x, square.t2.x)
            ys = [square.t1.y, square.t2.y]
            ys_results = []
            for y in ys:
                r = self.raycast(x, y)
                ys_results.append(r)
                print(x, y, ys_results)

            if all([x.is_inside_polygon() for x in ys_results]):
                return square

            print(f"Square ({square}) {i + 1}/{all_squares} done.")

        return None

    #         for tile in self.tiles:
    #             contains_any_tile = any([square.contains_tile(tile)])
    #             corners_in_some_square = []
    #     return None

    def print(self, special_x: int = -1, special_y: int = -1):
        corners_copy = deepcopy(self.tiles)
        current_tile = corners_copy.pop(0)
        # print(current_tile)
        for y in range(self.max_dimension + 2):
            line = ""
            for x in range(self.max_dimension + 2):
                if x == special_x and y == special_y:
                    line += "O"
                elif x == current_tile.x and y == current_tile.y:
                    line += current_tile.color.value
                else:
                    line += "."

                if x == current_tile.x and y == current_tile.y:
                    if not corners_copy:
                        break
                    else:
                        current_tile = corners_copy.pop(0)
                    # print(current_tile)
            print(line)

    def raycast(self, x: int, y: int) -> Raycast:
        ray = Raycast()
        # all_interesting = len(self.interesting_xs)
        for u, x_iter in enumerate([i for i in self.interesting_xs if i >= x]):
            lines = []
            for i, line in enumerate(self.lines):
                if line.coord_on_line(x_iter, y, True):
                    lines.append(i)
            ray.add_point(x_iter, y, lines)
            # print(f"{u}/{all_interesting} rays done")
            x += 1
        return ray


x = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
4,4
6,4
4,5
6,5
7,3"""

f = Floor()
f.load_floor(x)
s = f.get_largest_inside_square()
print(s)
# f.build_lines()
# # f.print(5, 5)
# r = f.raycast(2, 1)
# for o in r.coords:
#     f.print(o[0], o[1])
#     print("\n")
# print(r.is_inside_polygon())
# print(r.coords)
# print(r.lines)
# for u in r.lines_unique:
#     print(f"{u}: {f.lines[u]}")
# print(f.lines)
