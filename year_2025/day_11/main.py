from year_2025.day_11.functions import Board

with open("year_2025/day_11/input.txt", "r") as file:
    board_str = file.read()

b = Board()
b.load_board(board_str)
b.find_paths("you", tuple())

print(f"Part 1: Amount of paths: {len(b.paths)}")

b = Board()
b.load_board(board_str)
possible_paths = [
    [["svr", "dac"], ["dac", "fft"], ["fft", "out"]],
    [["svr", "fft"], ["fft", "dac"], ["dac", "out"]],
]
overall_count = 0
for path in possible_paths:
    path_count = 1
    for pair in path:
        c = b.cached_paths(pair[0], pair[1])
        path_count *= c
    overall_count += path_count
print(overall_count)

# b.find_paths("fft", tuple(), "dac")
# filtered = [x for x in b.paths if "fft" in x and "dac" in x]

print(f"Part 2: Amount of paths: {overall_count}")
