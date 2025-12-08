from year_2025.day_04.functions import Floor


def test_acessible_rows_print():
    input_matrix = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    f = Floor()
    f.parse_matrix(input_matrix)
    f.parse_for_viable()
    rolls = f.get_accessible_rolls()
    assert rolls == 13
