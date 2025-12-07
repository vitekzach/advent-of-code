from src import Table

input_file = "input.txt"
table = Table(input_file)

print(f"Solution from part 1: {table.pile_worth}")
print(f"Solution from part 2: {table.overall_copies_owned}")
