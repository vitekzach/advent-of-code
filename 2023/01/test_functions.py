from functions import (
    get_first_digit,
    get_last_digit,
    get_first_and_last_digit,
    get_final_sum,
    get_first_digit_crawl,
    get_last_digit_crawl,
    get_first_and_last_digit_crawl,
    get_final_sum_crawl,
    replace_spelled_digits,
)


def test_get_first_digit():
    assert get_first_digit("1abc2") == "1"
    assert get_first_digit("pqr3stu8vwx") == "3"
    assert get_first_digit("a1b2c3d4e5f") == "1"
    assert get_first_digit("treb7uchet") == "7"
    assert get_first_digit_crawl("1abc2") == "1"
    assert get_first_digit_crawl("pqr3stu8vwx") == "3"
    assert get_first_digit_crawl("a1b2c3d4e5f") == "1"
    assert get_first_digit_crawl("treb7uchet") == "7"


def test_get_last_digit():
    assert get_last_digit("1abc2") == "2"
    assert get_last_digit("pqr3stu8vwx") == "8"
    assert get_last_digit("a1b2c3d4e5f") == "5"
    assert get_last_digit("treb7uchet") == "7"
    assert get_last_digit_crawl("1abc2") == "2"
    assert get_last_digit_crawl("pqr3stu8vwx") == "8"
    assert get_last_digit_crawl("a1b2c3d4e5f") == "5"
    assert get_last_digit_crawl("treb7uchet") == "7"


def test_get_first_and_last_digit():
    assert get_first_and_last_digit("1abc2") == "12"
    assert get_first_and_last_digit("pqr3stu8vwx") == "38"
    assert get_first_and_last_digit("a1b2c3d4e5f") == "15"
    assert get_first_and_last_digit("treb7uchet") == "77"
    assert get_first_and_last_digit_crawl("1abc2") == "12"
    assert get_first_and_last_digit_crawl("pqr3stu8vwx") == "38"
    assert get_first_and_last_digit_crawl("a1b2c3d4e5f") == "15"
    assert get_first_and_last_digit_crawl("treb7uchet") == "77"


def test_get_final_sum():
    inputs = [
        "1abc2",
        "pqr3stu8vwx",
        "a1b2c3d4e5f",
        "treb7uchet",
    ]
    assert get_final_sum(inputs) == 142
    assert get_final_sum_crawl(inputs) == 142


def test_digit_replacement():
    assert replace_spelled_digits("two1nine") == "2wo19ine"
    assert replace_spelled_digits("eightwothree") == "8igh2wo3hree"
    assert replace_spelled_digits("abcone2threexyz") == "abc1ne23hreexyz"
    assert replace_spelled_digits("xtwone3four") == "x2w1ne34our"
    assert replace_spelled_digits("4nineeightseven2") == "49ine8ight7even2"
    assert replace_spelled_digits("zoneight234") == "z1n8ight234"
    assert replace_spelled_digits("7pqrstsixteen") == "7pqrst6ixteen"
    assert replace_spelled_digits("six8threepvlxttc85two") == "6ix83hreepvlxttc852wo"
    assert (
        replace_spelled_digits("two1nine eightwothree six8threepvlxttc85two")
        == "2wo19ine 8igh2wo3hree 6ix83hreepvlxttc852wo"
    )


def test_digit_replacement_end_to_end():
    inputs_with_digits = [
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen",
    ]

    inputs_with_digits = [replace_spelled_digits(x) for x in inputs_with_digits]
    results = ["29", "83", "13", "24", "42", "14", "76"]
    for text, result in zip(inputs_with_digits, results):
        assert get_first_and_last_digit_crawl(text) == result

    assert get_final_sum(inputs_with_digits) == 281
