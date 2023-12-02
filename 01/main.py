from functions import get_final_sum, replace_spelled_digits


# @profile
def final_sum_functions(inputs: list[str]) -> tuple[int, ...]:
    result_for = get_final_sum(inputs)
    result_crawl = get_final_sum(inputs)

    return result_for, result_crawl


# read input
with open("input.txt", "r") as file:
    jumbled_inputs_original = file.read()

jumbled_inputs_original = jumbled_inputs_original.replace("\n", " ")
# this added for part 2
jumbled_inputs = replace_spelled_digits(jumbled_inputs_original)
jumbled_inputs = jumbled_inputs.split(" ")

with open("input_formatted.txt", "w") as file:
    to_save = [f"{old}\t{new}\n" for old, new in zip(jumbled_inputs_original.split(" "), jumbled_inputs)]
    file.writelines(to_save)


result_with_for, result_with_crawl = final_sum_functions(jumbled_inputs)


print(f"Final sum in input is (using for)  : {result_with_for}")
print(f"Final sum in input is (using crawl): {result_with_crawl}")
