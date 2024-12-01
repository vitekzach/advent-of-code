import re

DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

DIGIT_REPLACEMENT = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_all_digits(jumbled: str) -> list[str]:
    return [x for x in jumbled if x.isnumeric()]


def get_first_digit(jumbled: str) -> str:
    return get_all_digits(jumbled)[0]


def get_last_digit(jumbled: str) -> str:
    return get_all_digits(jumbled)[-1]


def get_first_and_last_digit(jumbled: str) -> str:
    return f"{get_first_digit(jumbled)}{get_last_digit(jumbled)}"


def get_final_sum(inputs: list[str]) -> int:
    digits = [get_first_and_last_digit(x) for x in inputs]
    return sum([int(x) for x in digits])


def get_first_digit_crawl(jumbled: str) -> str:
    for i in jumbled:
        if i.isnumeric():
            return i


def get_last_digit_crawl(jumbled: str) -> str:
    for i in jumbled[::-1]:
        if i.isnumeric():
            return i


def get_first_and_last_digit_crawl(jumbled: str) -> str:
    return f"{get_first_digit_crawl(jumbled)}{get_last_digit_crawl(jumbled)}"


def get_final_sum_crawl(inputs: list[str]) -> int:
    digits = [get_first_and_last_digit_crawl(x) for x in inputs]
    return sum([int(x) for x in digits])


def replace_spelled_digits(string_to_replace: str) -> str:
    present_numbers = []
    for digit in DIGITS:
        present_numbers.extend([(digit, m.start()) for m in re.finditer(digit, string_to_replace)])

    # present_numbers = [(digit, string_to_replace.index(digit)) for digit in DIGITS if digit in string_to_replace]
    for present_number in present_numbers:
        # print(f"Before: {string_to_replace}, {present_number}")
        # print(f"  before: {string_to_replace[: present_number[1]]}")
        # print(f"  middle: {DIGIT_REPLACEMENT[present_number[0]]}")
        # print(f"  end: {string_to_replace[present_number[1] + 1 :]}")
        string_to_replace = (
            string_to_replace[: present_number[1]]
            + DIGIT_REPLACEMENT[present_number[0]]
            + string_to_replace[present_number[1] + 1 :]
        )
    # print(f"After: {string_to_replace}, {present_number}")
    return string_to_replace
