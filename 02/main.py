from functions import parse_line, possible_game_sum, minimal_power_game_sum

with open("input.txt", "r") as file:
    games = file.readlines()

games = [parse_line(game) for game in games]
bag_contents = {"blue": 14, "red": 12, "green": 13}
possible_sum = possible_game_sum(games, bag_contents)
print("Part 1:")
print(f"    Possible game ID sum is: {possible_sum}")

power_game_sum = minimal_power_game_sum(games)

print("\nPart 2:")
print(f"    Sum of power of minimal possible games: {power_game_sum}")
