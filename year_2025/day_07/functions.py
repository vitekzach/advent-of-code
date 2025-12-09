import copy
from csv import Error
from enum import Enum


class TileType(Enum):
    empty = "."
    source = "S"
    splitter = "^"
    beam = "|"


class Tile:
    def __init__(self, tile_type: TileType) -> None:
        self.type = tile_type
        # self.walks: list[list[str]] = []
        self.walks_count: int = 0

    def __str__(self):
        return self.type.value

    def __repr__(self) -> str:
        return f"State: {self.type.value}, Walks: {self.walks_count}"


class Manifold:
    def __init__(self) -> None:
        self.board: list[list[Tile]] = []
        self.split_times = 0
        self.list_of_possible_choices: list[list[str]] = []

    def load_manifold(self, board: str):
        rows = board.split("\n")

        for row in rows:
            row_list = [Tile(TileType(x)) for x in row]
            self.board.append(row_list)

    def print_board(self) -> None:
        for row in self.board:
            row_repr = [str(x) for x in row]
            row_repr_str = "".join(row_repr)
            print(row_repr_str)

    def print_board_diag(self) -> None:
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                print(f"x: {x} y: {y} tile: {tile.__repr__()}")

    def get_tile_above(self, x: int, y: int) -> Tile | None:
        if y == 0:
            return None
        return self.board[y - 1][x]

    def get_tile_left(self, x: int, y: int, board: list | None = None) -> Tile | None:
        if board is None:
            board = self.board
        if x == 0:
            return None
        return self.board[y][x - 1]

    def get_tile_right(self, x: int, y: int, board: list | None = None) -> Tile | None:
        if board is None:
            board = self.board
        if x == len(self.board[0]) - 1:
            return None
        return self.board[y][x + 1]

    def parse_board(self) -> None:
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile.type is TileType.source:
                    tile.walks_count = 1
                above = self.get_tile_above(x, y)
                # print(x, y, tile.__repr__(), above.__repr__())
                if above is not None:
                    if (tile.type is TileType.empty or tile.type is TileType.beam) and (
                        above.type is TileType.source or above.type is TileType.beam
                    ):
                        tile.type = TileType.beam
                        # print(f"above before: {tile.__repr__()}")
                        tile.walks_count += above.walks_count
                        # print(f"above after: {tile.__repr__()}")
                    if tile.type is TileType.splitter and (
                        above.type is TileType.source or above.type is TileType.beam
                    ):
                        self.split_times += 1
                        left = self.get_tile_left(x, y)
                        if left is not None:
                            # print(f"left before: {left.__repr__()}")
                            if left.type is TileType.empty or left.type is TileType.beam:
                                left.type = TileType.beam
                                left.walks_count += above.walks_count
                        right = self.get_tile_right(x, y)
                        if right is not None:
                            if right.type is TileType.empty or right.type is TileType.beam:
                                right.type = TileType.beam
                                right.walks_count += above.walks_count
            print(f"Row {y} done")

    def get_timeline_count(self) -> int:
        count = sum([x.walks_count for x in self.board[-1]])
        return count

    def parse_board_quantum(
        self,
        x: int | None = None,
        y: int | None = None,
        choices: list[str] | None = None,
        board: list[list[Tile]] | None = None,
    ) -> None:
        if choices is None:
            for i, tile in enumerate(self.board[0]):
                if tile.type is TileType.source:
                    # print(f"Source at {[0, i]}")
                    board = copy.deepcopy(self.board)
                    self.parse_board_quantum(i, 1, [], board)
                    return

        if x is None or y is None:
            raise Error("Zero coords")
        if choices is None:
            raise Error("No choices")
        if board is None:
            raise Error("No board")
        tile = board[y][x]
        # print(x, y, tile, choices)
        if tile.type is TileType.empty:
            tile.type = TileType.beam
            # print("made beam")
            if y < len(self.board) - 1:
                self.parse_board_quantum(x, y + 1, choices, board)
            else:
                self.list_of_possible_choices.append(choices)
                # print("End")
        if tile.type is TileType.splitter:
            left = self.get_tile_left(x, y, board)
            right = self.get_tile_right(x, y, board)
            for tile_affected, str_choice in zip([left, right], ["l", "r"]):
                if tile_affected is not None:
                    new_x = x - 1 if str_choice == "l" else x + 1
                    new_y = y
                    self.parse_board_quantum(new_x, new_y, choices[:] + [str_choice], copy.deepcopy(board))


manifold = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

# m = Manifold()
# m.load_manifold(manifold)
# # m.print_board()
# m.parse_board()

# # m.print_board()
# # print(m.split_times)
# m.print_board_diag()
# print(sum([x.walks_count for x in m.board[-1]]))

# m.parse_board_quantum()
# m.print_board()
# print(m.list_of_possible_choices)
# print(len(m.list_of_possible_choices))
# print(["a"] == ["a"])
# print([len(x) for x in m.list_of_possible_choices])
# print([x for x in m.list_of_possible_choices if len(x) == 3])
