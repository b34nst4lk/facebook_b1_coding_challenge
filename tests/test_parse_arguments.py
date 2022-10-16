import pytest

from ..main import (
    combine_lines_to_int,
    convert_row_to_int,
    decompose_bits,
    get_column_of_bit,
    get_number_of_test_cases,
    get_row_and_column_count,
    get_row_of_bit,
    is_friendly_painting,
    paint,
    produce_test_cases,
)

edge_case = "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

edge_case_in_int = 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111


@pytest.mark.parametrize("line", ["1", "2", "5000"])
def test_parse_number_of_test_cases(line):
    number_of_test_cases = get_number_of_test_cases(line)
    assert number_of_test_cases == int(line)


@pytest.mark.parametrize(
    "line,result",
    [
        ("1 3", (1, 3)),
        ("2 4", (2, 4)),
        ("3 3", (3, 3)),
    ],
)
def test_get_row_and_column_count(line, result):
    row_count, column_count = get_row_and_column_count(line)
    assert row_count == result[0]
    assert column_count == result[1]


@pytest.mark.parametrize(
    "line,result",
    [
        (".^.", 0b010),
        ("^....", 0b10000),
        (".^^.^^.", 0b0110110),
        ("^^^^^^^^^", 0b111111111),
        ("^^^^^^^^^\n", 0b111111111),
        (edge_case, edge_case_in_int),
    ],
)
def test_convert_row_to_int(line, result):
    row_int = convert_row_to_int(line)
    print(bin(row_int))
    print(bin(result))
    assert convert_row_to_int(line) == result


@pytest.mark.parametrize(
    "line,columns,result",
    [
        ([0b010, 0b010, 0b010], 3, 0b010010010),
        ([0b01000, 0b010, 0b010], 5, 0b010000001000010),
        ([0b1, 0b1, 0b0], 1, 0b110),
        ([edge_case_in_int for _ in range(100)], 92, 2**9200 - 1),
    ],
)
def test_combine_lines_to_int(line, columns, result):
    assert combine_lines_to_int(line, columns) == result


@pytest.fixture
def test_cases():
    return iter(
        f"""3
1 3
.^.
3 1
.
.
.
4 4
..^.
..^.
....
...^""".split(
            "\n"
        )
    )


def test_produce_test_cases(test_cases):
    producer = produce_test_cases(test_cases)
    assert next(producer) == (1, 3, 0b010)
    assert next(producer) == (3, 1, 0b000)
    assert next(producer) == (4, 4, 0b0010001000000001)


@pytest.mark.parametrize(
    "row_count,column_count,testcase,result",
    [
        (1, 0, 1, False),
        (0, 1, 1, False),
        (1, 1, 0, True),
        (1, 1, 1, False),
    ],
)
def test_is_friendly_painting(row_count, column_count, testcase, result):
    assert is_friendly_painting(row_count, column_count, testcase) == result


@pytest.mark.parametrize(
    "row_count,column_count,testcase,result",
    [
        (1, 1, 0, 0),
        (1, 3, 0, 0),
        (3, 1, 0, 0),
        (3, 3, 0b000010000, 0b111111111),
        (2, 2, 0b1000, 0b1111),
    ],
)
def test_paint(row_count, column_count, testcase, result):
    assert paint(row_count, column_count, testcase) == result


@pytest.mark.parametrize(
    "testcase,results",
    [
        (0b1, {0b1}),
        (0b11, {0b1, 0b10}),
        (0b0, set()),
        (0b10110, {0b10000, 0b100, 0b10}),
        (2**9200 - 1, {2**i for i in range(9200)}),
    ],
)
def test_decompose_bits(testcase, results):
    assert {bit for bit in decompose_bits(testcase)} == results


@pytest.mark.parametrize(
    "row_count,column_count,bit,result",
    [
        (3, 2, 0b010000, 2),
        (3, 3, 0b000000010, 0),
        (3, 3, 0b000010000, 1),
        (2, 2, 0b1000, 1),
        (3, 1, 0b100, 2),
    ],
)
def test_get_row_of_bit(row_count, column_count, bit, result):
    assert get_row_of_bit(row_count, column_count, bit) == result


@pytest.mark.parametrize(
    "row_count,column_count,bit,result",
    [
        (3, 2, 0b010000, 0),
        (3, 3, 0b000000010, 1),
        (3, 3, 0b000010000, 1),
        (2, 2, 0b1000, 1),
        (3, 1, 0b100, 0),
    ],
)
def test_get_column_of_bit(row_count, column_count, bit, result):
    assert get_column_of_bit(row_count, column_count, bit) == result
