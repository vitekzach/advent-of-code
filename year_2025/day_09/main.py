from collections import Counter
from year_2025.day_09.functions import Floor

with open("year_2025/day_09/input.txt", "r") as file:
    t = file.read()

f = Floor()
f.load_floor(t)
s = f.get_biggest_square()

print(f"Part 1: Largest square: {s.area}")

s2 = f.get_largest_inside_square()
print(s2)

# floor = f.tiles

# floor_xs = sorted([x.x for x in floor])
# floor_ys = sorted([x.y for x in floor])


# x_counter = Counter(floor_xs)
# y_counter = Counter(floor_ys)
# print(x_counter.most_common(5))
# print(y_counter.most_common(5))

