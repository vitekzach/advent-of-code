from typing import Literal

import pytest

from year_2025.day_01.functions import Dial


@pytest.mark.parametrize(
    [
        "init_position",
        "direction",
        "amount",
        "expected_position",
        "expected_zero_hit_times",
        "expected_zero_passed_time",
    ],
    (
        (50, "L", 68, 82, 0, 1),
        (82, "L", 30, 52, 0, 0),
        (52, "R", 48, 0, 1, 0),
        (0, "L", 5, 95, 0, 0),
        (95, "R", 60, 55, 0, 1),
        (55, "L", 55, 0, 1, 0),
        (0, "L", 1, 99, 0, 0),
        (99, "L", 99, 0, 1, 0),
        (0, "R", 14, 14, 0, 0),
        (14, "L", 82, 32, 0, 1),
    ),
)
def test_rotate_dial(
    init_position: int,
    direction: Literal["L", "R"],
    amount: int,
    expected_position: int,
    expected_zero_hit_times: int,
    expected_zero_passed_time: int,
    max_position: int = 99,
):
    dial = Dial(init_position, max_position)

    dial.rotate(direction, amount)

    assert dial.position == expected_position
    assert dial.zero_hit_times == expected_zero_hit_times
    assert dial.zero_passed_times == expected_zero_passed_time
