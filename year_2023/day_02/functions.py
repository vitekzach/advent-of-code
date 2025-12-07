def parse_line(game_records: str) -> dict[str, int | dict[str, list[int]]]:
    # prepare dictionary with amounts seen
    dict_colors = {"blue": [], "red": [], "green": []}

    # take game id and the games out of input
    game_name, game_outputs = game_records.split(":")
    game_id = int(game_name.split(" ")[1])
    game_outputs = game_outputs.strip()

    # split games into separate list of lists of "NUM COLOR"
    games = game_outputs.split(";")
    games = [game.split(", ") for game in games]
    games = [[x.strip() for x in game] for game in games]

    # fill the dict for given round - get amount and color, add it
    for game in games:
        for turn in game:
            amount, color = turn.split(" ")
            amount = int(amount)
            dict_colors[color].append(amount)

    # print(f" Game ID: {game_id}, games: {dict_colors}")
    return {"game_id": game_id, "amounts": dict_colors}


def game_possible(game_record: dict[str, list[int]], bag_contents: dict[str, int]) -> bool:
    # check each color
    for color_to_check, amount_to_check in bag_contents.items():
        # check each game
        # print(f"Color: {color_to_check}, Amount: {amount_to_check}, Record: {game_record[color_to_check]}")
        if not all([amount <= amount_to_check for amount in game_record[color_to_check]]):
            return False

    return True


def possible_game_sum(games_parsed: list[dict[str, int | dict[str, list[int]]]], bag_contents: dict[str, int]) -> int:
    # get IDs of possible games and sum them
    possible_ids = [
        one_game["game_id"] for one_game in games_parsed if game_possible(one_game["amounts"], bag_contents)
    ]
    return sum(possible_ids)


def minimal_amounts_for_possible_game(game_record: dict[str, list[int]]) -> dict[str, int]:
    # minimal amount is max amount of each colour we've seen
    return {key: max(value) for key, value in game_record.items()}


def minimal_amounts_game_power(game_record: dict[str, list[int]]) -> int:
    minimal_amounts = minimal_amounts_for_possible_game(game_record)
    # get amounts
    amounts = list(minimal_amounts.values())

    # get aproduct of amounts
    power = amounts[0]
    for amount in amounts[1:]:
        power *= amount
    return power


def minimal_power_game_sum(games_parsed: list[dict[str, int | dict[str, list[int]]]]) -> int:
    game_powers = [minimal_amounts_game_power(game["amounts"]) for game in games_parsed]
    return sum(game_powers)
