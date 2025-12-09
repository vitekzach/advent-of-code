from year_2025.day_07.functions import Manifold

with open("year_2025/day_07/input.txt", "r") as file:
    input_board = file.read()

m = Manifold()
m.load_manifold(input_board)
m.print_board()
m.parse_board()
m.print_board()

print(f"Part 1: Beams split {m.split_times} times")
print(f"Part 2: Timeline count is {m.get_timeline_count()}")
