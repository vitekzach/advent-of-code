import re
from dataclasses import dataclass

from scipy.optimize import LinearConstraint, milp


@dataclass
class QueueItem:
    lights_on: list[bool]
    button_presses: list[int]

    def __repr__(self) -> str:
        return f"{self.button_presses}"


@dataclass
class JoltageQueueItem:
    joltages: list[int]
    distance: int
    button_presses: list[int]
    viable_buttons: list[int]

    def __repr__(self) -> str:
        return f"d: {self.distance} j:{self.joltages} v:{self.viable_buttons} bp:{self.button_presses}"


class Machine:
    def __init__(self) -> None:
        self.lights_count: int = 0
        self.lights_on: list[bool] = []
        self.desired_lights: list[bool] = []
        self.buttons: list[list[int]] = []
        self.best_solution: list[int] = []
        self.best_joltage_solution: list[int] = []
        self.queue: list[QueueItem] | None = None
        self.joltages: list[int] = []

    def load_machine(self, config: str) -> None:
        lights_match = re.search(re.compile(r"\[([#\.]+)\]"), config)
        if lights_match is None:
            raise ValueError("No lights found")
        desired_lights = lights_match.group(1)
        self.desired_lights = [True if x == "#" else False for x in desired_lights]
        self.lights_on = [False for x in range(len(self.desired_lights))]

        buttons_groups = re.findall(re.compile(r"\(([\d,]+)\)"), config)
        for group in buttons_groups:
            nums = group.split(",")
            button_group = [int(x) for x in nums]
            self.buttons.append(button_group)

        joltages_match = re.search(re.compile(r"\{([\d,]+)\}"), config)
        if joltages_match is None:
            raise ValueError("No joltages found")

        joltages = joltages_match.group(1)
        self.joltages = [int(x) for x in joltages.split(",")]

    def press_button(
        self, button_idx: int, current_lights: list[bool] | None = None, update_self: bool = True
    ) -> list[bool]:
        # print(f"Pressing button({button_idx}): {self.buttons[button_idx]}")
        if current_lights is None:
            current_lights = self.lights_on
        button = self.buttons[button_idx]
        lights_on = [not x if i in button else x for i, x in enumerate(current_lights)]
        if update_self:
            self.lights_on = lights_on
        return lights_on

    def press_joltage_button(self, button_idx: int, current_joltage: list[int]) -> list[int]:
        # print(f"Pressing joltage button({button_idx}): {self.buttons[button_idx]}")
        button = self.buttons[button_idx]
        new_joltage = [x + 1 if i in button else x for i, x in enumerate(current_joltage)]
        return new_joltage

    def is_solved(self, current_lights: list[bool] | None = None):
        if current_lights is None:
            current_lights = self.lights_on

        is_solved = [x == current_lights[i] for i, x in enumerate(self.desired_lights)]
        return all(is_solved)

    def calculate_joltage_distance(self, current_joltages: list[int]) -> int:
        d = sum([abs(j - current_joltages[i]) for i, j in enumerate(self.joltages)])
        return d

    def joltage_valid(self, current_joltges: list[int]) -> bool:
        v = [j >= current_joltges[i] for i, j in enumerate(self.joltages)]

        if all(v):
            return True
        return False

    def full_joltage_meters(self, current_joltages: list[int]) -> list[int]:
        f = [i for i, g in enumerate(self.joltages) if g == current_joltages[i]]
        return f

    def find_joltage_soluction_milp(self) -> int:
        lcs = []
        for i, joltage in enumerate(self.joltages):
            c = [int(i in x) for x in self.buttons]
            lc = LinearConstraint(c, lb=joltage, ub=joltage)
            lcs.append(lc)
            cf = [1] * len(self.buttons)

        r = milp(c=cf, constraints=lcs, integrality=1)
        if not r.success:
            print(r.success, r.message)

        return int(r.fun)

    def find_joltage_soltution_failed(self) -> None:
        queue: list[JoltageQueueItem] = []
        for button in range(len(self.buttons)):
            joltages_zero = [0 for x in self.joltages]
            queue_item = JoltageQueueItem(
                joltages_zero, self.calculate_joltage_distance(joltages_zero), [button], list(range(len(self.buttons)))
            )
            queue.append(queue_item)

        while queue:
            queue = sorted(queue, key=lambda x: (x.distance, -len(self.buttons[x.button_presses[-1]])))

            current_press = queue.pop(0)
            current_joltage = current_press.joltages

            if len(current_press.button_presses) >= len(self.best_joltage_solution) and self.best_joltage_solution:
                continue

            button = current_press.button_presses[-1]
            new_joltage = self.press_joltage_button(button, current_joltage)
            new_is_valid = self.joltage_valid(new_joltage)
            if not new_is_valid:
                print("Not valid")
                continue
            new_distance = self.calculate_joltage_distance(new_joltage)
            full_meters = self.full_joltage_meters(new_joltage)
            new_viable_buttons = [
                x for x in current_press.viable_buttons if not set(self.buttons[x]) & set(full_meters)
            ]
            # print(current_press)
            print(f"nd: {new_distance} nj: {new_joltage} nvb: {new_viable_buttons} cpb: {current_press.button_presses}")
            # if len(new_viable_buttons) != len(current_press.viable_buttons):
            #     print(
            #         f"Viable pruned from {current_press.viable_buttons} to {new_viable_buttons} via full meters {full_meters}"
            #     )
            if new_is_valid and new_distance == 0:
                print("Found solution!")
                ql_b = len(queue)
                queue = [x for x in queue if len(x.button_presses) < len(current_press.button_presses)]
                ql_a = len(queue)
                print(f"Pruned {ql_b - ql_a} from queue")
                if not self.best_joltage_solution:
                    print(f"First solution, len {len(current_press.button_presses)}")
                    self.best_joltage_solution = current_press.button_presses
                    print(input("waiting"))
                elif len(current_press.button_presses) < len(self.best_joltage_solution):
                    print(
                        f"Better solution, len {len(current_press.button_presses)} from {len(self.best_joltage_solution)}"
                    )
                    self.best_joltage_solution = current_press.button_presses
                    print(input("waiting"))
            else:
                queue += [
                    JoltageQueueItem(
                        new_joltage,
                        new_distance,
                        current_press.button_presses + [i],
                        new_viable_buttons,
                    )
                    for i in new_viable_buttons
                ]
            # print(f"ql: {len(queue)}")

            # for b in self.buttons:

    def bfs_buttons(self) -> None:
        self.queue = [QueueItem(self.lights_on[:], [i]) for i in range(len(self.buttons))]
        # iter = 0

        while len(self.queue) > 0:
            # iter += 1
            # if iter % 10000 == 0:
            #     print(f"Iter ")
            current_press = self.queue.pop(0)
            # print(f"CQ: {len(self.queue)}, PL:{len(current_press.button_presses)}, CBL{len(self.best_solution)}")
            lights_on = current_press.lights_on
            # print(f"CP: {current_press}, LO: {self.get_lights_on(lights_on)}")

            # check for current recursion deeper than already found - exit condition
            if len(current_press.button_presses) >= len(self.best_solution) and self.best_solution:
                # state = self.get_state_str(lights_on)
                # state += f" bp:{current_press}, bs: {self.best_solution} Exit condition hit"
                # print(state)
                continue

            button = current_press.button_presses[-1]
            new_lights = self.press_button(button, lights_on, False)
            new_solved = self.is_solved(new_lights)
            if new_solved:
                # queue_len_before = len(self.queue)
                self.queue = [x for x in self.queue if len(x.button_presses) < len(current_press.button_presses)]
                # queue_len_after = len(self.queue)
                # print(f"Pruned {queue_len_before - queue_len_after} queue items")
                if not self.best_solution:
                    self.best_solution = current_press.button_presses
                elif len(current_press.button_presses) < len(self.best_solution):
                    self.best_solution = current_press.button_presses
                # print(f"bs: {self.best_solution}, cp: {current_press}, cq: {self.queue}")
            else:
                # s = self.get_state_str(new_lights)
                # print(f"{s} - bp:{current_press}")

                self.queue += [
                    QueueItem(new_lights, current_press.button_presses + [i])
                    for i in range(len(self.buttons))
                    if i not in current_press.button_presses
                ]
                # print(f"NQ: {self.queue}")
        # print(
        #     f"Best solution: {[self.get_button_str(x) for x in self.best_solution]} in {len(self.best_solution)} presses"
        # )

    def recurse_buttons(
        self, buttons_pressed: list[int] = [], lights_on: list[bool] | None = None
    ) -> tuple[list[int], list[bool]]:
        if lights_on is None:
            lights_on = self.lights_on

        if len(buttons_pressed) >= 3:
            print("Stop here too deep")
            return [], []

        # check for current recursion deeper than already found - exit condition
        if len(buttons_pressed) >= len(self.best_solution) and self.best_solution:
            state = self.get_state_str(lights_on)
            state += f" bp:{buttons_pressed}, bs: {self.best_solution} Exit condition hit"
            return [], []

        for i, b in enumerate(self.buttons):
            # press button
            current_solution = buttons_pressed + [i]
            new_lights = self.press_button(i, lights_on, False)
            is_solved = self.is_solved(new_lights)
            state = self.get_state_str(new_lights)
            state += f" bp:{current_solution}, solved:{is_solved}"
            print(state)
            if is_solved:
                if not self.best_solution or len(current_solution) < len(self.best_solution):
                    print("Solved!")
                    self.best_solution = current_solution
                    print(self.best_solution)
                    return [], []
            self.recurse_buttons(current_solution, new_lights)

        return [], []

    def get_lights_on(self, lights_on: list[bool] | None = None) -> str:
        if lights_on is None:
            lights_on = self.lights_on
        state = "["
        for i in lights_on:
            if i:
                state += "#"
            else:
                state += "."
        state += "] "

        return state

    def get_button_str(self, button_idx: int) -> str:
        return f"({button_idx}): [{self.buttons[button_idx]}]"

    def get_state_str(self, lights_on: list[bool] | None = None) -> str:
        state = "D:["
        for i in self.desired_lights:
            if i:
                state += "#"
            else:
                state += "."
        state += f"] C:{self.get_lights_on(lights_on)}"

        for group in self.buttons:
            state += f"({','.join([str(x) for x in group])}) "

        solved = self.is_solved(lights_on)
        state += f" S:{solved}"
        return state

    def print_state(self, lights: list[bool] | None = None) -> None:
        state = self.get_state_str(lights)
        print(state)


# print("\033c", end="")
# machines = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
# [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
# [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

# machines_split = machines.split("\n")

# running_total = 0
# for machine_spec in machines_split:
#     m = Machine()
#     m.load_machine(machine_spec)
#     res = m.find_joltage_soluction_milp()
#     print(res)
#     running_total += res
# print(running_total)

# print(f"Overall fewest presses: {running_total}")

# m.press_button(1)
# m.print_state()
# m.press_button(3)
# m.print_state()

# m.recurse_buttons()
# m.print_state()
# m.press_button(4)
# m.print_state()
# m.press_button(5)
# m.print_state()
