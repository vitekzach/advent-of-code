from year_2025.day_03.functions import JoltMaximizer

with open("year_2025/day_03/input.txt", "r") as file:
    banks = file.read().split("\n")

j = JoltMaximizer()
for bank in banks:
    j.get_bank_max_joltage(bank, 2)
print(f"Max joltage day 1: {j.get_overall_joltage()}")

j = JoltMaximizer()
for bank in banks:
    j.get_bank_max_joltage(bank, 12)
print(f"Max joltage day 2: {j.get_overall_joltage()}")
