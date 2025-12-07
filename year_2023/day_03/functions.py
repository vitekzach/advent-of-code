import re
from itertools import chain

# text = ["abc...a", "dfa..323"]
# numbers = {0: [{"number": -1, "valid": None, "border_beginning": -1, "border_end": -1}]}

NUMBER_PATTERN = re.compile(r"(?P<symbol>\d+)")
GEAR_PATTERN = re.compile(r"(?P<symbol>\*)")
SYMBOL_BLACKLIST = [
    ".",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]


def get_symbol_and_borders_from_line(line: str, mode: str) -> list[dict[str, int | bool]]:
    if mode == "number":
        pattern = NUMBER_PATTERN
    elif mode == "gear":
        pattern = GEAR_PATTERN
    # print(
    #     [
    #         {
    #             "symbol": m.group("symbol"),
    #             "border_beginning": m.start("symbol"),
    #             "border_end": m.end("symbol") - 1,
    #             "valid": None,
    #         }
    #         for m in re.finditer(pattern, line)
    #     ]
    # )
    return [
        {
            "symbol": m.group("symbol"),
            "border_beginning": m.start("symbol"),
            "border_end": m.end("symbol") - 1,
            "valid": None,
        }
        for m in re.finditer(pattern, line)
    ]


def generate_potential_index_neighbours(
    text_lines: list[str], line_number: int, number: dict[str, int | bool]
) -> list[list[int, int]]:
    line_length = len(text_lines[0])
    line_count = len(text_lines)

    # print("--------------------")
    # print("\n".join(text_lines))
    # print(line_number)
    # print(number)

    above = []
    # get top row neighbours only if line is not the top row
    if line_number > 0:
        # clamp beginning and end to text borders
        beginning = max([0, number["border_beginning"] - 1])
        end = min([number["border_end"] + 1, line_length - 1])

        # generate indexes and add to object
        indexes = list(range(beginning, end + 1))
        number_indexes = [[line_number - 1, index] for index in indexes]
        above = number_indexes
        # print(f"Top: {indexes}")

    middle = []
    # get indexes for middle
    # clamp beginning and end to text borders
    if number["border_beginning"] > 0:
        middle.append([line_number, max([0, number["border_beginning"] - 1])])
        # print(f"Added middle beginning: {[number["border_beginning"] - 1, line_number]}")
    if number["border_beginning"] < line_length - 1:
        middle.append([line_number, min([number["border_end"] + 1, line_length - 1])])
        # print(f"Added middle ending: {[number["border_end"] + 1, line_number]}")

    below = []
    # get bottom row neighbours only if line is not the bottom row
    if line_number <= line_count - 2:
        # clamp beginning and end to text borders
        beginning = max([0, number["border_beginning"] - 1])
        end = min([number["border_end"] + 1, line_length - 1])

        # generate indexes and add to object
        indexes = list(range(beginning, end + 1))
        number_indexes = [[line_number + 1, index] for index in indexes]
        below = number_indexes
    return [above, middle, below]


def generate_number_potential_neighbours(
    text_lines: list[str], line_number: int, number: dict[str, int | bool]
) -> list[str]:
    neighbours = []
    indexes = generate_potential_index_neighbours(text_lines, line_number, number)
    neighbours = list(chain.from_iterable(indexes))

    # print(f"Line length: {line_length}")
    # print(f"Line count: {line_count}")
    # print(neighbours)

    string_neighbours = [text_lines[neighbour[0]][neighbour[1]] for neighbour in neighbours]
    return string_neighbours


def number_in_range(number: dict[str, int | str | None], potential_indexes: list[[int, int]]) -> bool:
    number_range = list(range(number["border_beginning"], number["border_end"] + 1))
    return bool(set(number_range) & set(potential_indexes))


def get_gear_adjacent_numbers_from_line(
    line_numbers: list[dict[str, int | str | None]], potential_indexes: list[[int, int]]
) -> list[dict[str, int | str | None]]:
    # print("  Line numbers", line_numbers)
    # print("  Potential indexes", potential_indexes)
    # print("  result", [number for number in line_numbers if number_in_range(number, potential_indexes)])
    return [number for number in line_numbers if number_in_range(number, potential_indexes)]


def get_gear_adjacent_numbers(
    gear: dict[str, int | str | None],
    number_line_dict: dict[int, list[dict[str, int | None | str]]],
    texts: list[str],
    line_number: int,
) -> list[dict[str, int | None | str]]:
    neighbours = generate_potential_index_neighbours(texts, line_number, gear)

    # print("Line number", line_number)
    # print("Neighbours", neighbours)

    line_count = len(texts) - 1

    adjacent_numbers = []

    if line_number > 0:
        # top of current line
        indexes_top = [x[1] for x in neighbours[0]]
        gear_adjacent_numbers = get_gear_adjacent_numbers_from_line(number_line_dict[line_number - 1], indexes_top)
        # print("top", gear_adjacent_numbers)
        adjacent_numbers.extend(gear_adjacent_numbers)

    # current line
    indexes_middle = [x[1] for x in neighbours[1]]
    gear_adjacent_numbers = get_gear_adjacent_numbers_from_line(number_line_dict[line_number], indexes_middle)
    # print("middle", gear_adjacent_numbers)
    adjacent_numbers.extend(gear_adjacent_numbers)

    if line_number <= line_count:
        # under current line
        indexes_under = [x[1] for x in neighbours[2]]
        gear_adjacent_numbers = get_gear_adjacent_numbers_from_line(number_line_dict[line_number + 1], indexes_under)
        # print("bottom", gear_adjacent_numbers)
        adjacent_numbers.extend(gear_adjacent_numbers)

    return adjacent_numbers


def symbol_in_number_neighbours(neighbours: list[str]) -> bool:
    return bool([neighbour for neighbour in neighbours if neighbour not in SYMBOL_BLACKLIST])


def get_line_to_symbols_dict(texts: list[str], mode: str) -> dict[int, list[dict[str, str | None | int]]]:
    # get all numbers
    numbers = [get_symbol_and_borders_from_line(line, mode) for line in texts]

    # create a dict like {line_number: [number_dict]}
    numbers_dict = {number_line: numbers for number_line, numbers in enumerate(numbers)}
    return numbers_dict


def get_viable_part_numbers(texts: list[str]) -> list[int]:
    numbers_dict = get_line_to_symbols_dict(texts, "number")

    # premade list of viable numbers
    viable_numbers_list = []

    # for each line, find if number is viable and fill in dictionary
    for number_line, numbers in numbers_dict.items():
        for number in numbers:
            # get neighbours
            neighbours = generate_number_potential_neighbours(texts, number_line, number)
            # find if number is viable
            viable = symbol_in_number_neighbours(neighbours)
            number["valid"] = viable
            if viable:
                viable_numbers_list.append(int(number["symbol"]))
    #
    # import pprint
    #
    # pprint.pprint(numbers_dict)
    # print(viable_numbers_list)

    return viable_numbers_list


def get_viable_gears(texts: list[str]) -> list[dict]:
    gears_dict = get_line_to_symbols_dict(texts, "gear")
    numbers_dict = get_line_to_symbols_dict(texts, "number")

    possible_gears = []
    for line_number, gears in gears_dict.items():
        for gear in gears:
            neighbours = get_gear_adjacent_numbers(gear, numbers_dict, texts, line_number)
            if len(neighbours) == 2:
                gear["valid"] = True
                gear["neighbors"] = neighbours
                ratio = 1
                for neighbour in neighbours:
                    ratio *= int(neighbour["symbol"])
                gear["ratio"] = ratio
                possible_gears.append(gear)

    # print(possible_gears)

    return possible_gears


def get_viable_part_numbers_sum(texts: list[str]) -> int:
    return sum(get_viable_part_numbers(texts))


def get_gear_ratios(texts: list[str]) -> int:
    gears = get_viable_gears(texts)
    ratios = [gear["ratio"] for gear in gears]
    return sum(ratios)


# def get_viable_gear_numbers(texts: list[str]) -> list[]
