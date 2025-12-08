from year_2025.day_02.functions import IdInvalidator

id_invalidator = IdInvalidator()

with open("year_2025/day_02/input.txt", "r") as file:
    input = file.read().split(",")

split_ranges = [x.split("-") for x in input]

for split_range in split_ranges:
    id_invalidator.crack_duplicated_id(split_range[0], split_range[1])
    id_invalidator.crack_duplicated_ids_any_length(split_range[0], split_range[1])

# print(id_invalidator.invalid_ids)
print(sum(id_invalidator.invalid_ids))
print(sum(id_invalidator.invalid_ids_any))
