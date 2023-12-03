from functions import (
    get_symbol_and_borders_from_line,
    generate_number_potential_neighbours,
    symbol_in_number_neighbours,
    get_viable_part_numbers,
    get_viable_part_numbers_sum,
    get_gear_adjacent_numbers_from_line,
    get_gear_adjacent_numbers,
    get_viable_gears,
    get_gear_ratios,
)


def test_get_numbers_from_line():
    inputs = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
    ]
    outputs = [
        [
            {"symbol": "467", "valid": None, "border_beginning": 0, "border_end": 2},
            {"symbol": "114", "valid": None, "border_beginning": 5, "border_end": 7},
        ],
        [],
        [
            {"symbol": "35", "valid": None, "border_beginning": 2, "border_end": 3},
            {"symbol": "633", "valid": None, "border_beginning": 6, "border_end": 8},
        ],
        [],
        [
            {"symbol": "617", "valid": None, "border_beginning": 0, "border_end": 2},
        ],
    ]

    for (
        str_input,
        output,
    ) in zip(inputs, outputs):
        assert get_symbol_and_borders_from_line(str_input, "number") == output

    inputs = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]
    outputs = [
        [],
        [
            {"symbol": "*", "valid": None, "border_beginning": 3, "border_end": 3},
        ],
        [],
        [],
        [
            {"symbol": "*", "valid": None, "border_beginning": 3, "border_end": 3},
        ],
        [],
        [],
        [],
        [
            {"symbol": "*", "valid": None, "border_beginning": 5, "border_end": 5},
        ],
        [],
    ]

    for (
        str_input,
        output,
    ) in zip(inputs, outputs):
        assert get_symbol_and_borders_from_line(str_input, "gear") == output


def test_generate_number_potential_neighbours():
    inputs = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
    ]

    numbers = [
        {"symbol": "467", "valid": None, "border_beginning": 0, "border_end": 2},
        {"symbol": "114", "valid": None, "border_beginning": 5, "border_end": 7},
        {"symbol": "35", "valid": None, "border_beginning": 2, "border_end": 3},
        {"symbol": "633", "valid": None, "border_beginning": 6, "border_end": 8},
        {"symbol": "617", "valid": None, "border_beginning": 0, "border_end": 2},
    ]

    number_lines = [0, 0, 2, 2, 4]
    outputs = [
        [
            ".",
            ".",
            ".",
            ".",
            "*",
        ],
        [
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
        ],
        [
            ".",
            ".",
            "*",
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
        ],
        [
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
            "#",
            ".",
            ".",
            ".",
        ],
        [".", ".", ".", ".", "*"],
    ]

    for (
        number,
        number_line,
        output,
    ) in zip(numbers, number_lines, outputs):
        assert generate_number_potential_neighbours(inputs, number_line, number) == output


def test_symbol_in_number_neighbours():
    inputs = [
        [
            ".",
            ".",
            ".",
            ".",
            "*",
        ],
        [
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
        ],
        [
            ".",
            ".",
            "*",
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
        ],
        [
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
            ".",
            "#",
            ".",
            ".",
            ".",
        ],
        [".", ".", ".", ".", "*"],
    ]

    outputs = [True, False, True, True, True]

    for input, output in zip(inputs, outputs):
        assert symbol_in_number_neighbours(input) == output


def test_get_viable_part_numbers():
    text_input = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]

    output = [467, 35, 633, 617, 592, 755, 664, 598]

    assert get_viable_part_numbers(text_input) == output


def test_get_viable_part_numbers_sum():
    text_input = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]

    output = 4361

    assert get_viable_part_numbers_sum(text_input) == output


def test_get_gear_adjacent_numbers_from_line():
    line_numbers = [
        [
            {"symbol": "467", "valid": None, "border_beginning": 0, "border_end": 2},
            {"symbol": "114", "valid": None, "border_beginning": 5, "border_end": 7},
        ],
        [],
        [
            {"symbol": "35", "valid": None, "border_beginning": 2, "border_end": 3},
            {"symbol": "633", "valid": None, "border_beginning": 6, "border_end": 8},
        ],
        [],
        [
            {"symbol": "617", "valid": None, "border_beginning": 0, "border_end": 2},
        ],
        [
            {"symbol": "58", "valid": None, "border_beginning": 7, "border_end": 8},
        ],
        [
            {"symbol": "755", "valid": None, "border_beginning": 6, "border_end": 8},
        ],
        [],
        [
            {"symbol": "664", "valid": None, "border_beginning": 1, "border_end": 3},
            {"symbol": "598", "valid": None, "border_beginning": 5, "border_end": 7},
        ],
    ]

    potential_indexes = [[2, 3, 4], [2, 4], [2, 3, 4], [2, 3, 4], [2, 4], [2, 3, 4], [4, 5, 6], [4, 6], [4, 5, 6]]

    outputs = [
        [{"symbol": "467", "valid": None, "border_beginning": 0, "border_end": 2}],
        [],
        [{"symbol": "35", "valid": None, "border_beginning": 2, "border_end": 3}],
        [],
        [{"symbol": "617", "valid": None, "border_beginning": 0, "border_end": 2}],
        [],
        [{"symbol": "755", "valid": None, "border_beginning": 6, "border_end": 8}],
        [],
        [{"symbol": "598", "valid": None, "border_beginning": 5, "border_end": 7}],
    ]

    for line_number_list, index_list, output_list in zip(line_numbers, potential_indexes, outputs):
        assert get_gear_adjacent_numbers_from_line(line_number_list, index_list) == output_list


def test_get_gear_adjacent_numbers():
    texts = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]

    number_line_dict = {
        0: [
            {"border_beginning": 0, "border_end": 2, "symbol": "467", "valid": True},
            {"border_beginning": 5, "border_end": 7, "symbol": "114", "valid": False},
        ],
        1: [],
        2: [
            {"border_beginning": 2, "border_end": 3, "symbol": "35", "valid": True},
            {"border_beginning": 6, "border_end": 8, "symbol": "633", "valid": True},
        ],
        3: [],
        4: [{"border_beginning": 0, "border_end": 2, "symbol": "617", "valid": True}],
        5: [{"border_beginning": 7, "border_end": 8, "symbol": "58", "valid": False}],
        6: [{"border_beginning": 2, "border_end": 4, "symbol": "592", "valid": True}],
        7: [{"border_beginning": 6, "border_end": 8, "symbol": "755", "valid": True}],
        8: [],
        9: [
            {"border_beginning": 1, "border_end": 3, "symbol": "664", "valid": True},
            {"border_beginning": 5, "border_end": 7, "symbol": "598", "valid": True},
        ],
    }

    gears = [
        {"symbol": "*", "valid": None, "border_beginning": 3, "border_end": 3},
        {"symbol": "*", "valid": None, "border_beginning": 3, "border_end": 3},
        {"symbol": "*", "valid": None, "border_beginning": 5, "border_end": 5},
    ]

    line_numbers = [1, 4, 8]

    outputs = [
        [
            {"symbol": "467", "valid": True, "border_beginning": 0, "border_end": 2},
            {"symbol": "35", "valid": True, "border_beginning": 2, "border_end": 3},
        ],
        [{"symbol": "617", "valid": True, "border_beginning": 0, "border_end": 2}],
        [
            {"symbol": "755", "valid": True, "border_beginning": 6, "border_end": 8},
            {"symbol": "598", "valid": True, "border_beginning": 5, "border_end": 7},
        ],
    ]

    for line_number, gear, output in zip(line_numbers, gears, outputs):
        assert get_gear_adjacent_numbers(gear, number_line_dict, texts, line_number) == output


def test_get_viable_parts_ratios():
    texts = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]

    output = [
        {
            "symbol": "*",
            "valid": True,
            "border_beginning": 3,
            "ratio": 16345,
            "border_end": 3,
            "neighbors": [
                {"symbol": "467", "valid": None, "border_beginning": 0, "border_end": 2},
                {"symbol": "35", "valid": None, "border_beginning": 2, "border_end": 3},
            ],
        },
        {
            "symbol": "*",
            "valid": True,
            "border_beginning": 5,
            "ratio": 451490,
            "border_end": 5,
            "neighbors": [
                {"symbol": "755", "valid": None, "border_beginning": 6, "border_end": 8},
                {"symbol": "598", "valid": None, "border_beginning": 5, "border_end": 7},
            ],
        },
    ]

    assert get_viable_gears(texts) == output


def test_get_gear_ratios():
    texts = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]

    output = 467835

    assert get_gear_ratios(texts) == output
