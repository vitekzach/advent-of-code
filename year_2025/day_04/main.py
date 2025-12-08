from year_2025.day_04.functions import Floor

with open("year_2025/day_04/input.txt", "r") as file:
    input_matrix = file.read()

f = Floor()
f.parse_matrix(input_matrix)
f.parse_for_viable()
amnt = f.get_accessible_rolls()

print(f"Part 1 accessbile rows: {amnt}")

f.remove_accessbile_rolls_repeated()
print(f"Part 2 removed rolls: {f.removed_accessible_rolls}")
