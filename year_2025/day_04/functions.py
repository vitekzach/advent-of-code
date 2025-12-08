from dataclasses import dataclass


@dataclass
class Cell:
    has_paper_roll: bool
    is_viable: bool
    paper_roll_neighbors: int = 0


class Floor:
    def __init__(self) -> None:
        self.empty_char = "."
        self.paper_roll_char = "@"
        self.viable_paper_roll_char = "x"
        self.removed_paper_roll_char = "X"
        self.matrix: list[list[Cell]] = []
        self.viable_limit = 4
        self.removed_accessible_rolls = 0

    def parse_matrix(self, matrix_repr: str):
        rows = matrix_repr.split("\n")
        matrix = []
        for row in rows:
            row_list = []
            for cell in row:
                cell_obj = Cell(
                    cell == self.paper_roll_char or cell == self.viable_paper_roll_char,
                    cell == self.viable_paper_roll_char,
                )
                row_list.append(cell_obj)
            matrix.append(row_list)
        self.matrix = matrix

    def print_matrix(self):
        for row in self.matrix:
            row_repr = ""
            for cell in row:
                if cell.is_viable:
                    cell_repr = self.viable_paper_roll_char
                elif cell.has_paper_roll:
                    cell_repr = self.paper_roll_char
                else:
                    cell_repr = self.empty_char

                row_repr += cell_repr
            print(row_repr)

    def get_neighbor_indices(self, row: int, col: int) -> list[list[int]]:
        neighbor_indices = []
        for col_offset in range(-1, 2):
            for row_offset in range(-1, 2):
                neighbor_row = row + row_offset
                neighbor_col = col + col_offset

                neighbor_row_viable = neighbor_row >= 0 and neighbor_row < len(self.matrix)
                neighbor_col_viable = neighbor_col >= 0 and neighbor_col < len(self.matrix[row])
                is_current = neighbor_row == row and neighbor_col == col
                if neighbor_row_viable and neighbor_col_viable and not is_current:
                    neighbor_indices.append([neighbor_row, neighbor_col])

        return neighbor_indices

    def parse_for_viable(self):
        for row_idx, row in enumerate(self.matrix):
            for col_idx, cell in enumerate(row):
                for neighbor in self.get_neighbor_indices(row_idx, col_idx):
                    neighbor_row = neighbor[0]
                    neighbor_col = neighbor[1]
                    neighbor_cell = self.matrix[neighbor_row][neighbor_col]
                    if neighbor_cell.has_paper_roll:
                        cell.paper_roll_neighbors += 1
                        # print(
                        #     f"[{col_idx},{row_idx}]: (neighbor [{neighbor_col},{neighbor_row}]), now neighbors: {cell.paper_roll_neighbors}"
                        # )

        for row in self.matrix:
            for col in row:
                if col.paper_roll_neighbors < self.viable_limit and col.has_paper_roll:
                    col.is_viable = True

    def get_accessible_rolls(self) -> int:
        accessible_rows = 0
        for row in self.matrix:
            for cell in row:
                if cell.is_viable:
                    accessible_rows += 1

        return accessible_rows

    def remove_accessbile_rolls(self) -> int:
        removed_rolls = 0
        for row in self.matrix:
            for cell in row:
                if cell.is_viable:
                    removed_rolls += 1
                    cell.has_paper_roll = False
                cell.paper_roll_neighbors = 0
                cell.is_viable = False

        self.removed_accessible_rolls += removed_rolls

        return removed_rolls

    def remove_accessbile_rolls_repeated(self):
        removed_rolls = self.remove_accessbile_rolls()
        # print(f"Removed {removed_rolls} rolls")

        while removed_rolls > 0:
            self.parse_for_viable()
            removed_rolls = self.remove_accessbile_rolls()
            # print(f"Removed {removed_rolls} rolls")


# matrix = """..@@.@@@@.
# @@@.@.@.@@
# @@@@@.@.@@
# @.@@@@..@.
# @@.@@@@.@@
# .@@@@@@@.@
# .@.@.@.@@@
# @.@@@.@@@@
# .@@@@@@@@.
# @.@.@@@.@."""

# f = Floor()
# f.parse_matrix(matrix)
# f.print_matrix()
# print(f.get_neighbor_indices(0, 0))
# print(f.get_neighbor_indices(0, 9))
# print(f.get_neighbor_indices(9, 5))
# print(f.get_neighbor_indices(5, 5))
# f.parse_for_viable()
# print("\n\n")
# print(f.matrix[0][2])
# f.print_matrix()
# print(f.get_accessible_rolls())
# print(f.remove_accessbile_rolls())
# f.print_matrix()
# f.parse_for_viable()
# f.print_matrix()
# print(f.remove_accessbile_rolls())
# f.remove_accessbile_rolls_repeated()
# f.print_matrix()
# print(f.removed_accessible_rolls)
