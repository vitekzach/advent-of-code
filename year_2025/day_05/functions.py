class IngredientDB:
    def __init__(self) -> None:
        self.fresh_id_ranges: list[list[int]] = []
        self.fresh_ingredients: list[int] = []
        self.spoiled_ingredients: list[int] = []

    def load_fresh_ranges(self, ranges: list[str]) -> None:
        for range in ranges:
            b, e = range.split("-")
            parsed_range = [int(b), int(e)]
            self.add_fresh_range(parsed_range)

    def add_fresh_range(self, parsed_range: list[int]):
        if len(self.fresh_id_ranges) == 0:
            # print("Empty DB, adding new")
            self.fresh_id_ranges.append(parsed_range)
            return

        i = 0
        while i < len(self.fresh_id_ranges):
            compare_with = self.fresh_id_ranges[i]
            ranges_comparison = self.compare_ranges(parsed_range, compare_with)
            # print(
            #     f"Range 1: {parsed_range}, Range 2: {compare_with}, Result: {ranges_comparison}, DB: {self.fresh_id_ranges}, i: {i}"
            # )
            # self.fresh_id_ranges.append(parsed_range)
            if ranges_comparison == "none_left":
                self.fresh_id_ranges.insert(i, parsed_range)
                break
            if ranges_comparison == "left":
                self.fresh_id_ranges[i] = [parsed_range[0], compare_with[1]]
                break
            if ranges_comparison == "inside":
                break
            if ranges_comparison == "right" or ranges_comparison == "full":
                if ranges_comparison == "right":
                    self.fresh_id_ranges[i] = [compare_with[0], parsed_range[1]]
                if ranges_comparison == "full":
                    self.fresh_id_ranges[i] = [parsed_range[0], parsed_range[1]]
                # print(f"After DB: {self.fresh_id_ranges}")
                if i < len(self.fresh_id_ranges) - 1:
                    current_range = self.fresh_id_ranges[i]
                    next_range = self.fresh_id_ranges[i + 1]
                    ranges_comparison_right = self.compare_ranges(current_range, next_range)

                    while ranges_comparison_right in (
                        "left",
                        "full",
                    ):
                        # print(
                        #     f"DB: {self.fresh_id_ranges}, current: {current_range}, next: {next_range}, comparison: {ranges_comparison_right}, walk index: {i}"
                        # )
                        if ranges_comparison_right == "left":
                            self.fresh_id_ranges[i] = [current_range[0], next_range[1]]
                            # print(f"Left: Before: {self.fresh_id_ranges}")
                            self.fresh_id_ranges.pop(i + 1)
                            # print(f"Left: After: {self.fresh_id_ranges}")
                            break
                        if ranges_comparison_right == "full":
                            # self.fresh_id_ranges[walk_index] = [current_range[0], current_range[1]]
                            # print(f"Full: Before: {self.fresh_id_ranges}")
                            self.fresh_id_ranges.pop(i + 1)
                            # print(f"Full: After: {self.fresh_id_ranges}")

                            if i + 1 == len(self.fresh_id_ranges):
                                # print(f"At the end of list. DB: {self.fresh_id_ranges}, i: {i}")
                                break

                            current_range = self.fresh_id_ranges[i]
                            next_range = self.fresh_id_ranges[i + 1]
                            ranges_comparison_right = self.compare_ranges(current_range, next_range)
                            # print(f"Next comparison: {current_range} {next_range} {ranges_comparison_right}")
                break
            i += 1

        if i == len(self.fresh_id_ranges):
            self.fresh_id_ranges.append(parsed_range)

    def check_ingredient(self, id: int) -> None:
        for range in self.fresh_id_ranges:
            if id >= range[0] and id <= range[1]:
                self.fresh_ingredients.append(id)
                return

        self.spoiled_ingredients.append(id)

    def get_fresh_ingredient_count(self) -> int:
        fresh_id_count = 0
        for id_range in self.fresh_id_ranges:
            range_id_count = id_range[1] - id_range[0] + 1
            fresh_id_count += range_id_count

            # print(f"Range: {id_range}, Range count: {range_id_count}, Overll count: {fresh_id_count}")

        return fresh_id_count

    @staticmethod
    def compare_ranges(range_1: list[int], range_2: list[int]) -> str:
        if range_1[1] < range_2[0] and range_1[1] < range_2[1]:
            return "none_left"
        if range_1[0] > range_2[0] and range_1[0] > range_2[1]:
            return "none_right"
        if range_1[0] >= range_2[0] and range_1[1] <= range_2[1]:
            return "inside"
        if range_1[0] <= range_2[0] and range_1[1] >= range_2[1]:
            return "full"
        if range_1[0] < range_2[0] and range_1[1] >= range_2[0]:
            return "left"
        if range_1[0] >= range_2[0] and range_1[1] > range_2[1]:
            return "right"

        raise NotImplementedError("Edge case? :o")


# i = IngredientDB()
# i.load_fresh_ranges(
#     [
#         "20-30",
#         "10-15",
#         "35-40",
#         "36-37",
#         "19-31",
#         "14-32",
#         "1-100",
#         "100-101",
#         "100-101",
#         "102-103",
#         "103-104",
#         "5-104",
#         "104-105",
#         "201-300",
#         "401-500",
#     ]
# )
# print(i.fresh_id_ranges)
# print(i.get_fresh_ingredient_count())
# i.check_ingredient(1)
# i.check_ingredient(5)
# i.check_ingredient(8)
# i.check_ingredient(11)
# i.check_ingredient(17)
# i.check_ingredient(32)
# print(i.fresh_ingredients)
# print(i.spoiled_ingredients)

# i.create_fresh_id_list()
# print(i.fresh_ids_list)
