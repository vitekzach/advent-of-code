from year_2025.day_01.functions import Dial

with open("year_2025/day_01/input.txt", "r") as file:
    instructions = file.read().splitlines()

dial = Dial(50, 99)

for instruction in instructions:
    direction = instruction[0]
    amount = int(instruction[1:])

    dial.rotate(direction, amount)

print(dial.zero_hit_times, dial.zero_passed_times)
print(dial.zero_hit_times + dial.zero_passed_times)
