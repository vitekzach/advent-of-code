import re
from dataclasses import dataclass, field
from math import log10


@dataclass
class MathProblem:
    numbers: list[str] = field(default_factory=list)
    operation: str | None = None
    solution_part1: int = 0
    solution_part2: int = 0


class MathHomework:
    def __init__(self) -> None:
        self.problems: list[MathProblem] = []

    def ingest_homework(self, worksheet: str) -> None:
        rows = worksheet.split("\n")

        last_row = rows[-1]
        col_breaks = [i for i, c in enumerate(last_row) if c in ["*", "+"]]
        col_breaks.append(len(last_row) + 1)

        for i, row in enumerate(rows):
            elements = []
            for j in range(len(col_breaks) - 1):
                col = row[col_breaks[j] : col_breaks[j + 1] - 1]
                elements.append(col)

            if i == 0:
                problems = len(elements)
                self.problems = [MathProblem() for x in range(problems)]

            if elements[0][0] in ["+", "*"]:
                for i, element in enumerate(elements):
                    self.problems[i].operation = element[0]
            else:
                for i, element in enumerate(elements):
                    self.problems[i].numbers.append(element)

            # elements_cleaned = [x.strip() for x in elements]
            # print(elements_cleaned)

    @staticmethod
    def solve_problem_part1(problem: MathProblem):
        solution = int(problem.numbers[0])
        for second in problem.numbers[1:]:
            if problem.operation == "+":
                solution += int(second)
            if problem.operation == "*":
                solution *= int(second)

        problem.solution_part1 = solution

    @staticmethod
    def solve_problem_part2(problem: MathProblem):
        numbers_length = len(problem.numbers[0])
        numbers = []
        for col in range(numbers_length - 1, -1, -1):
            num = [x[col] for x in problem.numbers]
            num_int = int("".join(num))
            numbers.append(num_int)

        solution = numbers[0]
        for second in numbers[1:]:
            if problem.operation == "+":
                solution += second
            if problem.operation == "*":
                solution *= second

        problem.solution_part2 = solution

    @staticmethod
    def solve_problem(problem: MathProblem):
        MathHomework.solve_problem_part1(problem)
        MathHomework.solve_problem_part2(problem)

    def solve_problems(self) -> None:
        [self.solve_problem(problem) for problem in self.problems]

    def get_grand_total(self) -> dict[str, int]:
        grand_total_p1 = sum([x.solution_part1 for x in self.problems])
        grand_total_p2 = sum([x.solution_part2 for x in self.problems])
        return {"p1": grand_total_p1, "p2": grand_total_p2}


# m = MathHomework()
# m.ingest_homework("""123 328  51 64
#  45 64  387 23
#   6 98  215 314
# *   +   *   +  """)
# m.solve_problems()
# for p in m.problems:
#     print(p)
# print(m.get_grand_total_part1())
# m.stringify_problems()
