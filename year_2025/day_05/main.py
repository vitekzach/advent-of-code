from year_2025.day_05.functions import IngredientDB

i = IngredientDB()

with open("year_2025/day_05/input.txt", "r") as file:
    input = file.read()

ranges, ingredients = input.split("\n\n")

ranges_split = ranges.split("\n")
i.load_fresh_ranges(ranges_split)

ingredients_split = ingredients.split("\n")
for ingredient in ingredients_split:
    i.check_ingredient(int(ingredient))

print(f"Day 1: There are {len(i.fresh_ingredients)} fresh ingredients.")
print(f"Day 2: There are {i.get_fresh_ingredient_count()} fresh IDs.")
