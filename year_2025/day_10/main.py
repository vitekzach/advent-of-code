from year_2025.day_10.functions import Machine

CLEAR = "\033[2K\r"

with open("year_2025/day_10/input.txt", "r") as file:
    machines = file.read()
machines_split = machines.split("\n")


def print_progress(
    current: int,
    total: int,
    width: int = 20,
    empty_char: str = " ",
    filled_char: str = "█",
    beginning_char: str = "[",
    end_char: str = "]",
) -> str:
    max_len = len(str(total))
    done = current / total
    filled = round(done * width)
    empty = width - filled
    bar = f"({current:{max_len}}/{total:{max_len}}) {beginning_char}{filled_char * filled}{empty_char * empty}{end_char} {round(done * 100, 2):3.2f}%"
    return bar


running_total = 0
machines_total = len(machines_split)
for i, machine_spec in enumerate(machines_split):
    print(
        f"{CLEAR if 0 < i < machines_total else ''}{print_progress(i + 1, machines_total)} Machines done",
        end="",
        flush=True,
    )
    m = Machine()
    m.load_machine(machine_spec)
    m.bfs_buttons()
    running_total += len(m.best_solution)

print()
print(f"Part 1: Overall fewest presses is {running_total}")

running_total_joltage = 0
unique_totals = []
for i, machine_spec in enumerate(machines_split):
    print(
        f"{CLEAR if 0 < i < machines_total else ''}{print_progress(i + 1, machines_total)} Machines done",
        end="",
        flush=True,
    )
    m = Machine()
    m.load_machine(machine_spec)
    r = m.find_joltage_soluction_milp()
    unique_totals.append(r)
    running_total_joltage += r

print()
print(f"Part 2: Overall fewest presses is {running_total_joltage}")
