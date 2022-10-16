from argparse import ArgumentParser
from textwrap import wrap
from typing import Iterator, List, Tuple


def get_filename() -> str:
    parser = ArgumentParser(
        description="Solution to https://www.facebook.com/codingcompetitions/hacker-cup/2022/qualification-round/problems/B1"
    )

    parser.add_argument("input_file", help="input data for problem")

    args = parser.parse_args()

    filename = args.input_file
    return filename


def get_number_of_test_cases(input: str) -> int:
    return int(input)


def get_row_and_column_count(input: str) -> Tuple[int, int]:
    dimensions = input.split(" ")
    row_count = int(dimensions[0])
    column_count = int(dimensions[1])
    return row_count, column_count


def convert_row_to_int(input: str) -> int:
    input = input.replace("\n", "")
    converted_row = ["1" if v == "^" else "0" for v in input]
    line = "".join(converted_row)
    output = int(line, 2)
    return output


def combine_lines_to_int(input: List[int], column_count: int) -> int:
    output = 0
    stop_val = len(input) - 1
    for i, v in enumerate(input):
        output |= v
        if i != stop_val:
            output <<= column_count

    return output


def produce_test_cases(input: Iterator[str]) -> Iterator[Tuple[int, int, int]]:
    number_of_test_cases = get_number_of_test_cases(next(input))

    for _ in range(number_of_test_cases):
        row_count, column_count = get_row_and_column_count(next(input))
        lines = [convert_row_to_int(next(input)) for _ in range(row_count)]
        test_case = combine_lines_to_int(lines, column_count)
        yield row_count, column_count, test_case


def is_friendly_painting(row_count: int, column_count: int, test_case: int) -> bool:
    match (row_count, column_count, test_case):  # type:ignore
        case (0, _, _):
            # 0 rows, therefore not friendly
            return False
        case (_, 0, _):
            # 0 columns, therefore not friendly
            return False
        case (_, _, 0):
            # no trees, therefore definitely friendly
            return True
        case (1, _, _):
            # only 1 row, cannot have 2 neighbours at ends, therefore not friendly
            return False
        case (_, 1, _):
            # only 1 column, cannot have 2 neighbours at ends, therefore not friendly
            return False

    return True


def paint(row_count: int, column_count: int, test_case: int) -> int:
    if test_case == 0:
        return 0

    final_painting = test_case
    for bit in decompose_bits(test_case):
        final_painting |= make_paint_block(row_count, column_count, bit)

    return final_painting


def make_paint_block(row_count: int, column_count: int, bit: int) -> int:
    row_of_bit = get_row_of_bit(row_count, column_count, bit)
    column_of_bit = get_column_of_bit(row_count, column_count, bit)

    block = bit
    if column_of_bit != column_count - 1:
        block |= block << 1
    if column_of_bit != 0:
        block |= block >> 1

    if row_of_bit != row_count - 1:
        block |= block << column_count
    if row_of_bit != 0:
        block |= block >> column_count

    return block


def decompose_bits(number: int) -> Iterator[int]:
    index = 1
    while index <= number:
        if index & number:
            yield index
        index <<= 1


def get_row_of_bit(row_count: int, column_count: int, bit: int) -> int:
    if bit <= 0:
        raise ValueError("Must be positive number that is a power of 2")

    row_mask = 0
    for column in range(column_count):
        row_mask |= 1 << column

    for row in range(row_count):
        if (row_mask << row * column_count) & bit:
            return row

    raise ValueError(
        f"unexpected error: row_count: {row_count}, column_count: {column_count}, bit {bin(bit)}, bit_length: {bit.bit_length()}"
    )


def get_column_of_bit(row_count: int, column_count: int, bit: int) -> int:
    if bit <= 0:
        raise ValueError("Must be positive number that is a power of 2")

    column_mask = 0
    for row in range(row_count):
        column_mask |= 1 << row * column_count

    for column in range(column_count):
        if (column_mask << column) & bit:
            return column

    raise ValueError("unexpected error")


def prepare_painting(row_count: int, column_count: int, painting: int) -> List[str]:
    stringed_painting = str(bin(painting))[2:].zfill(row_count * column_count)
    lines = []
    for line in wrap(stringed_painting, column_count):
        line = line.replace("0", ".")
        line = line.replace("1", "^")
        line += "\n"
        lines.append(line)
    return lines


def main():
    filename = get_filename()
    with open(filename, "r") as f, open("output.txt", "w") as o:
        for test_case_number, test_case_spec in enumerate(produce_test_cases(f)):
            test_case_number += 1
            row_count, column_count, test_case = test_case_spec
            if not is_friendly_painting(row_count, column_count, test_case):
                message = f"Case #{test_case_number}: Impossible\n"
                print(message)
                o.write(message)
                continue
            message = f"Case #{test_case_number}: Possible\n"
            o.write(message)
            print(message)
            painting = paint(row_count, column_count, test_case)
            final_painting = prepare_painting(row_count, column_count, painting)
            for line in final_painting:
                print(line)
                o.write(line)


if __name__ == "__main__":
    main()
