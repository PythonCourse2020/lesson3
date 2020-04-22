from math import inf, nan
import operator

import pytest

from lesson3 import Series


def test_series_creation_without_index_creates_default_index():
    s = Series([10, 20, 30])

    assert s.index == [0, 1, 2]


def test_series_creation_with_index_sets_index_correctly():
    index = [1, 2, 3]
    s = Series([10, 20, 30], index=index)

    assert s.index == index


def test_series_creation_with_length_mismatched_index_raises_value_error():
    with pytest.raises(ValueError):
        Series([10, 20, 30], index=[0, 1])


def test_series_creation_with_non_iterable_value_creates_one_element_series():
    s = Series(100)

    assert list(s) == [100]


@pytest.mark.parametrize(["values"], [[[100, 200, 300]], [[]]])
def test_series_correctly_casts_to_list(values):
    assert list(Series(values)) == values


@pytest.mark.parametrize(["values"], [[[100, 200, 300]], [[]]])
def test_series_len_is_correct(values):
    assert len(Series(values)) == len(values)


@pytest.mark.parametrize(
    ["values", "op", "scalar", "expected_values"],
    [
        ([100, 200], operator.add, 1, [101, 201]),
        ([100, 200], operator.sub, 10, [90, 190]),
        ([100, 200], operator.mul, 5, [500, 1000]),
        ([100, 200], operator.truediv, 2, [50, 100]),
        ([100, 200], operator.truediv, 0, [inf, inf]),
        ([100, 200], operator.floordiv, 3, [33, 66]),
        ([100, 200], operator.floordiv, 0, [inf, inf]),
        ([100, 200], operator.mod, 9, [1, 2]),
        ([100, 200], operator.mod, 0, [nan, nan]),
        ([100, 200], operator.pow, 2, [10000, 40000]),
        ([100, 10000], operator.pow, 0.5, [10, 100]),
    ],
)
def test_binary_arithmetic_operations_with_scalars(values, op, scalar, expected_values):
    s = Series(values)

    assert (
        list(op(s, scalar)) == expected_values
        and list(op(scalar, s)) == expected_values
    )


@pytest.mark.parametrize(
    ["left_values", "op", "right_values", "expected_values"],
    [
        ([100, 200], operator.add, [2, 5], [102, 205]),
        ([100, 200], operator.sub, [10, -2], [90, 202]),
        ([100, 200], operator.mul, [0.5, 7], [50, 1400]),
        ([100, 200], operator.truediv, [8, 4], [12.5, 50]),
        ([100, 200], operator.truediv, [1, 0], [100, inf]),
        ([100, 200], operator.floordiv, [8, 3], [12, 66]),
        ([100, 200], operator.floordiv, [0, 0], [inf, inf]),
        ([100, 200], operator.mod, [11, -15], [1, -10]),
        ([100, 200], operator.mod, [0, 0], [nan, nan]),
        ([100, 200], operator.pow, [2, 0], [10000, 1]),
        ([100, 10000], operator.pow, [0.5, -1], [10, 0.0001]),
    ],
)
def test_binary_arithmetic_operations_between_series_of_same_index(
    left_values, op, right_values, expected_values
):
    left = Series(left_values)
    right = Series(right_values)

    assert list(op(left, right)) == expected_values


@pytest.mark.parametrize(
    ["left_series", "op", "right_series", "expected_series"],
    [
        (
            Series([100], index=[0]),
            operator.add,
            Series([1, 2], index=[0, 3]),
            Series([101, nan], index=[0, 3]),
        )
    ],
)
def test_binary_arithmetic_operations_between_series_of_mismatched_index(
    left_series, op, right_series, expected_series
):
    result = op(left_series, right_series)

    assert result == expected_series


@pytest.mark.parametrize(
    ["values", "op", "expected_values"],
    [
        ([100, 200], operator.neg, [-100, -200]),
        ([-100, 200], operator.neg, [100, -200]),
        ([0], operator.neg, [0]),
        ([100, 200], operator.pos, [100, 200]),
        ([-100, 200], operator.pos, [-100, 200]),
        ([0], operator.pos, [0]),
    ],
)
def test_unary_arithmetic_operations(values, op, expected_values):
    s = Series(values)

    assert list(op(s)) == expected_values


@pytest.mark.parametrize(
    ["values", "op", "scalar", "expected_values"],
    [
        ([100, 200], operator.lt, 150, [True, False]),
        ([50, 70], operator.lt, 50, [False, False]),
        ([100, 200], operator.le, 200, [True, True]),
        ([1000], operator.eq, 1000, [True]),
        ([1000.1], operator.eq, 1000, [False]),
        ([250, 251], operator.ne, 250, [False, True]),
        ([100, 200], operator.gt, 101, [False, True]),
        ([50, 70], operator.ge, 50, [True, True]),
    ],
)
def test_comparator_operation_with_scalar(values, op, scalar, expected_values):
    """
    The resulting series also needs to have an identical index.
    """
    s = Series(values)
    result = op(s, scalar)

    assert list(result) == expected_values and result.index == s.index


@pytest.mark.parametrize(
    ["left_values", "op", "right_values", "expected_values"],
    [
        ([100, 200], operator.lt, [200, 100], [True, False]),
        ([100, 200], operator.le, [100, 50], [True, False]),
        ([100, 200], operator.eq, [100, 100], [True, False]),
        ([100, 200], operator.ne, [200, 200], [True, False]),
        ([1, 2], operator.gt, [-1, 7], [True, False]),
        ([5, 10], operator.ge, [6, 10], [False, True]),
    ],
)
def test_comparator_operation_with_series(
    left_values, op, right_values, expected_values
):
    left = Series(left_values)
    right = Series(right_values)
    result = op(left, right)

    assert list(result) == expected_values and len(result) == len(left) == len(right)


@pytest.mark.parametrize(
    ["left_series", "op", "right_series"],
    [
        (Series([10, 20, 30]), operator.lt, Series([20, 30])),
        (Series([10], index=[0]), operator.eq, Series([50], index=[1])),
    ],
)
def test_comparator_operation_with_mismatched_series_raises_value_error(
    left_series, op, right_series
):
    with pytest.raises(ValueError):
        op(left_series, right_series)


@pytest.mark.parametrize(
    ["series", "expected_str"],
    [
        (Series([10, 20, 30]), "0\t10\n1\t20\n2\t30"),
        (Series([0, 0, 0], index=["L", "B", "G"]), "L\t0\nB\t0\nG\t0"),
        (Series([7, 5, 1], index=[10, 100, 1000]), "10\t7\n100\t5\n1000\t1"),
        (Series(), "Series([])"),
    ],
)
def test_str_is_correct(series, expected_str):
    assert str(series) == expected_str


@pytest.mark.parametrize(
    ["series", "expected_repr"],
    [
        (Series([10, 20, 30]), "Series([10, 20, 30], index=[0, 1, 2])"),
        (
            Series([0, 0, 0], index=["L", "B", "G"]),
            """Series([0, 0, 0], index=["L", "B", "G"])""",
        ),
        (
            Series([7, 5, 1], index=[10, 100, 1000]),
            "Series([7, 5, 1], index=[10, 100, 1000])",
        ),
        (Series(), "Series([])"),
    ],
)
def test_repr_is_correct(series, expected_repr):
    assert repr(series) == expected_repr


@pytest.mark.parametrize(
    ["series", "index", "expected_result"],
    [
        (Series([100, 200]), 0, 100),
        (Series([100, 200]), 1, 200),
        (Series([100, 200], index=[100, 1000]), 100, 100),
        (Series([100, 200], index=[100, 1000]), 1000, 200),
        (Series([100, 200], index=["a", "b"]), "a", 100),
    ],
)
def test_index_access(series, index, expected_result):
    assert series[index] == series.loc[index] == expected_result


@pytest.mark.parametrize(
    ["series", "index"],
    [(Series([10, 20]), 2), (Series([]), 0), (Series([10, 20], index=["a", "b"]), "c")],
)
def test_index_access_raises_index_error_if_index_does_not_exist(series, index):
    with pytest.raises(IndexError):
        series.loc[index]


@pytest.mark.parametrize(
    ["series", "i", "expected_result"],
    [
        (Series([10, 20], index=[3, 4]), 0, 10),
        (Series([10, 20], index=[1, 2]), 1, 20),
        (Series([10, 20, 30], index=[6, 7, 8]), -1, 30),
    ],
)
def test_iloc_access(series, i, expected_result):
    assert series.iloc[i] == expected_result


@pytest.mark.parametrize(
    ["series", "expected_values"],
    [
        (Series([10, 20]), [10, 20]),
        (Series([100, 200, 300], index=[6, 7, -1]), [100, 200, 300]),
        (Series(), []),
    ],
)
def test_iterator_loops_over_values(series, expected_values):
    results = list(iter(series))

    assert results == expected_values


@pytest.mark.parametrize(
    ["series", "expected_values"],
    [
        (Series([10, 20]), [(0, 10), (1, 20)]),
        (Series([10, 20], index=["a", "e"]), [("a", 10), ("e", 20)]),
        (Series(), []),
    ],
)
def test_iteritems_loops_over_key_value_tuples(series, expected_values):
    results = list(series.iteritems())

    assert results == expected_values


@pytest.mark.parametrize(
    ["series", "index", "expected_result"],
    [
        (Series([10, 20]), 10, False),
        (Series([10, 20]), 0, True),
        (Series(), 0, False),
        (Series([10], index=["a"]), "a", True),
    ],
)
def test_contains_checks_index(series, index, expected_result):
    assert index in series is expected_result


@pytest.mark.parametrize(
    ["series", "expected_len"],
    [(Series(), 0), (Series([10, 100]), 2), (Series([1]), 1)],
)
def test_len_is_correct(series, expected_len):
    assert len(series) == expected_len


@pytest.mark.parametrize(
    ["series", "selector", "expected_result"],
    [
        (Series([10, 100]), Series([False, True]), Series([100], index=[1])),
        (
            Series([5, 7, 9], index=["a", "b", "c"]),
            Series([True, False, True], index=["a", "b", "c"]),
            Series([5, 9], index=["a", "c"]),
        ),
    ],
)
def test_slicing_by_boolean_series(series, selector, expected_result):
    result = series[selector]

    assert result == expected_result
