import re


CARD_REGEX = re.compile(
    r"Card\s+(?P<card_number>\d+):\s+(?P<winning_numbers>((\d)+\s+)+)\|\s+(?P<present_numbers>((\d)+\s*)+)"
)
# line = "Card   1: 29 21 67 44  6 13 68 15 60 79 | 75 44 60 30 10 68 40 70 36 79  3 13 64 15  4 46 21 22 67 47 73 86 29 53  6"
#
LINE_REGEX = re.compile(r"\d+")
#
# [
#     {
#         "winning": m.group("winning"),
#         "present_numbers": m.group("present_numbers"),
#     }
#     for m in re.finditer(CARD_REGEX, line)
# ]
#
# re.findall(LINE_REGEX, line)


class Table:
    def __init__(self, file_input_path: str) -> None:
        self.file_input_path: str = file_input_path
        self.table: list[str] = self.__read__input__(file_input_path)

        cards = [Card(line) for line in self.table]
        self.cards = {card.card_number: card for card in cards}
        self.__calculate_pile_worth__()
        self.__calculate_card_copies_owned__()
        self.__calculate_overall_copies_owned__()

    @staticmethod
    def __read__input__(path: str) -> list[str]:
        """Read input and return list of lines"""

        with open(path, "r") as file:
            file_input = file.read()

        file_lines = file_input.split("\n")
        return file_lines

    def __calculate_pile_worth__(self) -> None:
        worth = 0
        for card in self.cards.values():
            worth += card.card_points

        self.pile_worth = worth

    def __calculate_card_copies_owned__(self) -> None:
        for card_number, card in self.cards.items():
            for winning_copy in card.wins_copies:
                self.cards[winning_copy].copies_owned += card.copies_owned

    def __calculate_overall_copies_owned__(self) -> None:
        cards = 0
        for card in self.cards.values():
            cards += card.copies_owned

        self.overall_copies_owned = cards


class Card:
    def __init__(self, card_line: str) -> None:
        card_line: str = card_line
        self.__parse_card_line__(card_line)
        self.__parse_winning_numbers__()
        self.__parse_card_value__()
        self.__parse_winning_copies__()
        self.copies_owned = 1

    def __parse_card_line__(self, card_line: str) -> None:
        match_numbers = re.search(CARD_REGEX, card_line)
        self.card_number = int(match_numbers.group("card_number"))
        winning_numbers = match_numbers.group("winning_numbers")
        present_numbers = match_numbers.group("present_numbers")

        self.winning_numbers_on_card = tuple(int(x) for x in re.findall(LINE_REGEX, winning_numbers))
        self.present_numbers_on_card = tuple(int(x) for x in re.findall(LINE_REGEX, present_numbers))

    def __parse_winning_numbers__(self) -> None:
        self.winning_numbers = tuple(x for x in self.present_numbers_on_card if x in self.winning_numbers_on_card)

    def __parse_card_value__(self) -> None:
        if len(self.winning_numbers) == 0:
            self.card_points = 0
        else:
            self.card_points = 2 ** (len(self.winning_numbers) - 1)

    def __parse_winning_copies__(self) -> None:
        indexes_to_add = list(range(1, len(self.winning_numbers) + 1))
        self.wins_copies = tuple([self.card_number + x for x in indexes_to_add])
