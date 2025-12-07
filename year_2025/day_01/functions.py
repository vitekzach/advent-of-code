from typing import Literal


class Dial:
    def __init__(self, init_position: int, max_position: int) -> None:
        self.position = init_position
        self.max_position = max_position
        self.all_positions = max_position + 1
        self.zero_hit_times = 0
        self.zero_passed_times = 0

    def rotate(self, direction: Literal["L", "R"], amount: int) -> None:
        if direction == "L":
            zero_passed_times = amount // self.all_positions
            if self.position - (amount % self.all_positions) < 0 and self.position != 0:
                zero_passed_times += 1

            self.zero_passed_times += zero_passed_times

            negative_shift = (amount - self.position) % self.all_positions
            if negative_shift != 0:
                self.position = self.all_positions - negative_shift
            else:
                self.position = 0

        elif direction == "R":
            zero_passed_times = amount // self.all_positions
            if self.position + (amount % self.all_positions) > self.all_positions and self.position != 0:
                zero_passed_times += 1

            self.zero_passed_times += zero_passed_times

            self.position = (self.position + amount) % self.all_positions

        if self.position == 0:
            self.zero_hit_times += 1
