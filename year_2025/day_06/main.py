from year_2025.day_06.functions import MathHomework

with open("year_2025/day_06/input.txt", "r") as file:
    problem = file.read()


m = MathHomework()
m.ingest_homework(problem)
m.solve_problems()
gt = m.get_grand_total()
# print(m.problems)
print(f"Day 1: Grand total is: {gt['p1']}")
print(f"Day 2: Grand total is: {gt['p2']}")
