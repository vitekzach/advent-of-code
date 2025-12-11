from year_2025.day_08.functions import Playground

with open("year_2025/day_08/input.txt", "r") as file:
    coords = file.read()

p = Playground()
p.load_playground(coords)
size = p.get_circuit_size(1000)
one_circuit = p.one_circuit_size()

print(f"Part 1: Size of circuit: {size}")
print(f"Part 2: Size of circuit: {one_circuit}")
