from functions import get_viable_part_numbers_sum, get_gear_ratios

with open("input.txt", "r") as file:
    text_lines = file.read()

text_lines = text_lines.split("\n")[:-1]

part_1_solution = get_viable_part_numbers_sum(text_lines)

print(f"Sum of viable parts for part1: {part_1_solution}")

part_2_solution = get_gear_ratios(text_lines)
print(f"Sum of viable gear ratios for part2: {part_2_solution}")
