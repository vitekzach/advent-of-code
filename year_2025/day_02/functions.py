class IdInvalidator:
    def __init__(self) -> None:
        self.invalid_ids: list[int] = []
        self.invalid_ids_any: list[int] = []

    def generate_duplicated_ids_of_length_duplicated(
        self, length: int, starting_half: int | None = None
    ):  # -> Generator[Any, Any, list[Any]]:
        if length % 2 != 0:
            raise ValueError("Length must be divisible by 2")

        if starting_half is None:
            starting_half_final: int = 10 ** ((length // 2) - 1)
        else:
            if len(str(starting_half)) != length:
                raise ValueError("Length of starting half must be same as length")
            starting_half_final = starting_half

        end_half = (10 ** (length // 2)) - 1

        current_half: int = starting_half_final

        # print(f"Starting half: {starting_half_final}, current half: {current_half}, end half {end_half}")

        while current_half <= end_half:
            full_number = current_half * 10 ** (length // 2) + current_half
            # print(full_number)
            yield full_number

            current_half += 1

    def generate_duplicated_ids_of_length(self, start: int, end: int, multiplication: int) -> list[int]:
        ids = [int(str(x) * multiplication) for x in range(start, end + 1)]
        return ids

    def generate_duplicated_ids_of_any_length(self, length: int) -> list[int]:
        duplicated_ids = []
        for i in range(1, (length // 2) + 2):
            modulo = length % i
            multiplication = length // i
            print(f"Trying length: {length}, i: {i}, modulo: {modulo}, multi: {multiplication}")
            if modulo == 0 and multiplication > 1:
                start = int(10 ** ((length / multiplication) - 1))
                end = int(10 ** (length / multiplication) - 1)
                print(f"Start: {start}, end: {end}")
                ids = self.generate_duplicated_ids_of_length(start, end, multiplication)
                # print(f"IDs: {ids}")
                duplicated_ids.extend(ids)

        return duplicated_ids

    def crack_duplicated_id(self, start: str, end: str):
        start_length = len(start)
        end_length = len(end)

        start_int = int(start)
        end_int = int(end)

        lengths_to_check = [x for x in range(start_length, end_length + 1) if x % 2 == 0]
        for length_to_check in lengths_to_check:
            print(f"Length to check: {length_to_check}")
            duplicated_ids = self.generate_duplicated_ids_of_length_duplicated(length_to_check)
            try:
                duplicated_id = next(duplicated_ids)
                while duplicated_id <= end_int:
                    # print(f"Duplicated id: {duplicated_id}")
                    if duplicated_id >= start_int:
                        self.invalid_ids.append(duplicated_id)
                    duplicated_id = next(duplicated_ids)
                print(f"End of length")
            except StopIteration:
                pass

    def crack_duplicated_ids_any_length(self, start: str, end: str):
        start_length = len(start)
        end_length = len(end)

        start_int = int(start)
        end_int = int(end)

        for length_to_check in range(start_length, end_length + 1):
            print(f"Length to check: {length_to_check}")
            duplicated_ids = self.generate_duplicated_ids_of_any_length(length_to_check)
            for duplicated_id in duplicated_ids:
                if duplicated_id <= end_int and duplicated_id >= start_int:
                    self.invalid_ids_any.append(duplicated_id)
            print(f"End of length {length_to_check}")

        self.invalid_ids_any = sorted(list(set(self.invalid_ids_any)))


i = IdInvalidator()
# # x = list(i.generate_duplicated_ids_of_length(6))
# print(i.generate_duplicated_ids_of_length(10, 99, 3))
# i.generate_duplicated_ids_of_any_length(6)
i.crack_duplicated_ids_any_length("11", "22")
print(i.invalid_ids_any)
# print(i.invalid_ids_any)

# i.generate_duplicated_id("12", "1111")
