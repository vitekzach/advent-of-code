import pytest

from year_2025.day_05.functions import IngredientDB


@pytest.mark.parametrize(
    ["ingredient_id", "expected_fresh"],
    [
        (1, False),
        (5, True),
        (8, False),
        (11, True),
        (17, True),
        (32, False),
    ],
)
def test_check_ingredient(ingredient_id: int, expected_fresh: bool):
    i = IngredientDB()
    i.load_fresh_ranges(
        [
            "3-5",
            "10-14",
            "16-20",
            "12-18",
        ]
    )
    i.check_ingredient(ingredient_id)
    if expected_fresh:
        assert len(i.fresh_ingredients) == 1
    else:
        assert len(i.spoiled_ingredients) == 1


@pytest.mark.parametrize(
    ["range_1", "range_2", "result"],
    [
        ([1, 5], [6, 10], "none_left"),
        ([11, 15], [6, 10], "none_right"),
        ([1, 9], [3, 4], "full"),
        ([3, 5], [5, 9], "left"),
        ([5, 9], [3, 5], "right"),
        ([3, 4], [1, 5], "inside"),
    ],
)
def test_compare_ranges(range_1: list[int], range_2: list[int], result: str):
    i = IngredientDB()
    res = i.compare_ranges(range_1, range_2)
    assert res == result
