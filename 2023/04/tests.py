import pytest

from src import Table, Card


def test_loading_file():
    file_input_path = "test_input.txt"
    output = [
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    ]

    table = Table(file_input_path)
    assert table.file_input_path == file_input_path
    assert table.table == output


@pytest.mark.parametrize(
    "card_input,winning,present",
    [
        ("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53", (41, 48, 83, 86, 17), (83, 86, 6, 31, 17, 9, 48, 53)),
        ("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19", (13, 32, 20, 16, 61), (61, 30, 68, 82, 17, 32, 24, 19)),
        ("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1", (1, 21, 53, 59, 44), (69, 82, 63, 72, 16, 21, 14, 1)),
        ("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83", (41, 92, 73, 84, 69), (59, 84, 76, 51, 58, 5, 54, 83)),
        ("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36", (87, 83, 26, 28, 32), (88, 30, 70, 12, 93, 22, 82, 36)),
        ("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11", (31, 18, 13, 56, 72), (74, 77, 10, 23, 35, 67, 36, 11)),
    ],
)
def test_card_parsing(card_input, winning, present):
    card = Card(card_input)
    assert card.winning_numbers_on_card == winning
    assert card.present_numbers_on_card == present


@pytest.mark.parametrize(
    "card_input,winning",
    [
        (
            "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
            tuple([83, 86, 17, 48]),
        ),
        ("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19", tuple([61, 32])),
        ("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1", tuple([21, 1])),
        ("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83", tuple([84])),
        ("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36", tuple([])),
        ("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11", tuple([])),
    ],
)
def test_winning_numbers(card_input, winning):
    card = Card(card_input)
    assert card.winning_numbers == winning


@pytest.mark.parametrize(
    "card_input,points",
    [
        (
            "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
            8,
        ),
        ("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19", 2),
        ("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1", 2),
        ("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83", 1),
        ("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36", 0),
        ("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11", 0),
    ],
)
def test_card_points(card_input, points):
    card = Card(card_input)
    assert card.card_points == points


def test_pile_worth():
    cards_input = "test_input.txt"
    pile_worth = 13

    table = Table(cards_input)

    assert table.pile_worth == pile_worth


@pytest.mark.parametrize(
    "card_input,copies",
    [
        (
            "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
            tuple([2, 3, 4, 5]),
        ),
        ("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19", tuple([3, 4])),
        ("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1", tuple([4, 5])),
        ("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83", tuple([5])),
        ("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36", tuple()),
        ("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11", tuple()),
    ],
)
def test_copy_winning(card_input, copies):
    card = Card(card_input)
    assert card.wins_copies == copies


@pytest.mark.parametrize(
    "card_number,copies",
    [
        (1, 1),
        (2, 2),
        (3, 4),
        (4, 8),
        (5, 14),
        (6, 1),
    ],
)
def test_copies_owned(card_number, copies):
    cards_input = "test_input.txt"

    table = Table(cards_input)
    assert table.cards[card_number].copies_owned == copies


def test_overall_copies_owned():
    cards_input = "test_input.txt"
    copies_owned = 30

    table = Table(cards_input)

    assert table.overall_copies_owned == copies_owned
