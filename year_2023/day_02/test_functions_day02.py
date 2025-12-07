from year_2023.day_02.functions import (
    game_possible,
    minimal_amounts_for_possible_game,
    minimal_amounts_game_power,
    minimal_power_game_sum,
    parse_line,
    possible_game_sum,
)


def test_parse_line():
    inputs = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]
    outputs = [
        {"game_id": 1, "amounts": {"blue": [3, 6], "red": [4, 1], "green": [2, 2]}},
        {"game_id": 2, "amounts": {"blue": [1, 4, 1], "red": [1], "green": [2, 3, 1]}},
        {"game_id": 3, "amounts": {"blue": [6, 5], "red": [20, 4, 1], "green": [8, 13, 5]}},
        {"game_id": 4, "amounts": {"blue": [6, 15], "red": [3, 6, 14], "green": [1, 3, 3]}},
        {"game_id": 5, "amounts": {"blue": [1, 2], "red": [6, 1], "green": [3, 2]}},
    ]

    for (
        str_input,
        output,
    ) in zip(inputs, outputs):
        assert parse_line(str_input) == output


def test_game_possible():
    inputs_records = [
        {"blue": [3, 6], "red": [4, 1], "green": [2, 2]},
        {"blue": [1, 4, 1], "red": [1], "green": [2, 3, 1]},
        {"blue": [6, 5], "red": [20, 4, 1], "green": [8, 13, 5]},
        {"blue": [6, 15], "red": [3, 6, 14], "green": [1, 3, 3]},
        {"blue": [1, 2], "red": [6, 1], "green": [3, 2]},
    ]

    inputs_bag_contents = {"blue": 14, "red": 12, "green": 13}

    outputs = [True, True, False, False, True]

    for inputs_record, output in zip(inputs_records, outputs):
        assert game_possible(inputs_record, inputs_bag_contents) == output


def test_possible_game_sum():
    inputs_records = [
        {"game_id": 1, "amounts": {"blue": [3, 6], "red": [4, 1], "green": [2, 2]}},
        {"game_id": 2, "amounts": {"blue": [1, 4, 1], "red": [1], "green": [2, 3, 1]}},
        {"game_id": 3, "amounts": {"blue": [6, 5], "red": [20, 4, 1], "green": [8, 13, 5]}},
        {"game_id": 4, "amounts": {"blue": [6, 15], "red": [3, 6, 14], "green": [1, 3, 3]}},
        {"game_id": 5, "amounts": {"blue": [1, 2], "red": [6, 1], "green": [3, 2]}},
    ]

    inputs_bag_contents = {"blue": 14, "red": 12, "green": 13}

    assert possible_game_sum(inputs_records, inputs_bag_contents) == 8


def test_minimal_amounts_for_possible_game():
    inputs_records = [
        {"blue": [3, 6], "red": [4, 1], "green": [2, 2]},
        {"blue": [1, 4, 1], "red": [1], "green": [2, 3, 1]},
        {"blue": [6, 5], "red": [20, 4, 1], "green": [8, 13, 5]},
        {"blue": [6, 15], "red": [3, 6, 14], "green": [1, 3, 3]},
        {"blue": [1, 2], "red": [6, 1], "green": [3, 2]},
    ]

    outputs = [
        {"blue": 6, "red": 4, "green": 2},
        {"blue": 4, "red": 1, "green": 3},
        {"blue": 6, "red": 20, "green": 13},
        {"blue": 15, "red": 14, "green": 3},
        {"blue": 2, "red": 6, "green": 3},
    ]

    for inputs_record, output in zip(inputs_records, outputs):
        assert minimal_amounts_for_possible_game(inputs_record) == output


def test_minimal_amounts_game_power():
    inputs_records = [
        {"blue": [3, 6], "red": [4, 1], "green": [2, 2]},
        {"blue": [1, 4, 1], "red": [1], "green": [2, 3, 1]},
        {"blue": [6, 5], "red": [20, 4, 1], "green": [8, 13, 5]},
        {"blue": [6, 15], "red": [3, 6, 14], "green": [1, 3, 3]},
        {"blue": [1, 2], "red": [6, 1], "green": [3, 2]},
    ]

    outputs = [48, 12, 1560, 630, 36]

    for inputs_record, output in zip(inputs_records, outputs):
        assert minimal_amounts_game_power(inputs_record) == output


def test_minimal_power_game_sum():
    inputs_record = [
        {"game_id": 1, "amounts": {"blue": [3, 6], "red": [4, 1], "green": [2, 2]}},
        {"game_id": 2, "amounts": {"blue": [1, 4, 1], "red": [1], "green": [2, 3, 1]}},
        {"game_id": 3, "amounts": {"blue": [6, 5], "red": [20, 4, 1], "green": [8, 13, 5]}},
        {"game_id": 4, "amounts": {"blue": [6, 15], "red": [3, 6, 14], "green": [1, 3, 3]}},
        {"game_id": 5, "amounts": {"blue": [1, 2], "red": [6, 1], "green": [3, 2]}},
    ]

    output = 2286

    assert minimal_power_game_sum(inputs_record) == output
