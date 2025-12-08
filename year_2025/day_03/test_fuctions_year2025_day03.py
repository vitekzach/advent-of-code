import pytest

from year_2025.day_03.functions import JoltMaximizer


@pytest.mark.parametrize(
    ["bank", "expected_joltage", "cells_available"],
    (
        ("987654321111111", 98, 2),
        ("811111111111119", 89, 2),
        ("234234234234278", 78, 2),
        ("818181911112111", 92, 2),
        ("987654321111111", 987654321111, 12),
        ("811111111111119", 811111111119, 12),
        ("234234234234278", 434234234278, 12),
        ("818181911112111", 888911112111, 12),
    ),
)
def test_get_bank_max_joltage(
    bank: str,
    expected_joltage: int,
    cells_available: int,
):
    j = JoltMaximizer()
    b = j.get_bank_max_joltage(bank, cells_available)
    assert b.max_joltage_value == expected_joltage
