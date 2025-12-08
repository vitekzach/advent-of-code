from dataclasses import dataclass


@dataclass
class BatteryBank:
    original_representation: str
    max_joltage_values: list[int]
    max_joltage_indices: list[int]

    @property
    def max_joltage_value(self) -> int:
        return int("".join([str(x) for x in self.max_joltage_values]))


class JoltMaximizer:
    def __init__(self) -> None:
        self.banks: list[BatteryBank] = []

    def get_bank_max_joltage_og(self, bank: str) -> BatteryBank:
        battery_bank_list = [int(x) for x in bank]

        viable_bank = battery_bank_list[:-1]
        max_first = max(viable_bank)
        idx_first = viable_bank.index(max_first)

        viable_bank = battery_bank_list[idx_first + 1 :]
        max_second = max(viable_bank)
        idx_second = viable_bank.index(max_second)

        bank_solved = BatteryBank(
            bank,
            [max_first, max_second],
            [idx_first, idx_second],
        )
        self.banks.append(bank_solved)

        print(bank_solved)
        return bank_solved

    def get_bank_max_joltage(self, bank: str, cells_available: int) -> BatteryBank:
        max_joltage_values: list[int] = []
        max_joltage_indices: list[int] = []
        battery_bank_list = [int(x) for x in bank]
        viable_beginning = 0

        for digit in range(-cells_available + 1, 1):
            if digit == 0:
                viable_bank = battery_bank_list[viable_beginning:]
            else:
                viable_bank = battery_bank_list[viable_beginning:digit]

            max_from_viable = max(viable_bank)
            idx_from_viable = viable_bank.index(max_from_viable)
            idx_overall = viable_beginning + idx_from_viable
            max_joltage_values.append(max_from_viable)
            max_joltage_indices.append(idx_overall)

            # print(
            #     f"viable bank: {viable_bank}, digit: {digit}, max: {max_from_viable}, idx: {idx_overall}, viable beginning: {viable_beginning}"
            # )

            viable_beginning = viable_beginning + idx_from_viable + 1

        bank_solved = BatteryBank(bank, max_joltage_values, max_joltage_indices)
        self.banks.append(bank_solved)
        return bank_solved

    def get_overall_joltage(self) -> int:
        bank_joltages = [x.max_joltage_value for x in self.banks]
        overall_joltage = sum(bank_joltages)
        return overall_joltage


# j = JoltMaximizer()
# b = j.get_bank_max_joltage("123456789012345", 12)
# print("\n\n")
# b = j.get_bank_max_joltage("9876987698769876", 6)
# print(b.max_joltage_value)
