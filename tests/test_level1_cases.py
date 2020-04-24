from math import nan

import pytest

from lesson3 import Series


@pytest.mark.parametrize(
    ["values", "index"], [([10, 20], [1, 1]), ([10, 20, 30], ["a", "b", "a"])]
)
def test_init_with_duplicate_index_raises_value_error(values, index):
    with pytest.raises(ValueError):
        Series(values, index=index)


@pytest.mark.parametrize(["index"], [([10, 20, 30],), (["a", "b", "c"],)])
def test_init_with_index_but_no_values_sets_values_to_nan(index):
    series = Series(index=index)

    assert all(value is nan for value in series)


@pytest.mark.parametrize(
    ["series", "expected_min"],
    [
        (Series([10, 20, 30]), 10),
        (Series([0, 0, 0]), 0),
        (Series([10, 50, -100, 7]), -100),
    ],
)
def test_min(series, expected_min):
    """
    Series.min is NOT a function
    """
    assert series.min == expected_min


@pytest.mark.parametrize(
    ["series", "expected_max"],
    [
        (Series([10, 20, 30]), 30),
        (Series([0, 0, 0]), 0),
        (Series([10, 50, -100, 7]), 50),
    ],
)
def test_max(series, expected_max):
    """
    Series.max is NOT a function
    """
    assert series.max == expected_max


@pytest.mark.parametrize(
    ["series", "expected_index"],
    [
        (Series([10, 20, 30]), 0),
        (Series([0, 0, 0]), 0),
        (Series([10, 50, -100, 7], index=[31, 23, 11, 10]), 11),
        (Series([30, 10, 5, 100], index=["a", "b", "c", "d"]), "c"),
    ],
)
def test_idxmin(series, expected_index):
    """
    Series.idxmin is NOT a function.
    """
    assert series.idxmin == expected_index


@pytest.mark.parametrize(
    ["series", "expected_index"],
    [
        (Series([10, 20, 30]), 2),
        (Series([0, 0, 0]), 0),
        (Series([10, 50, -100, 7], index=[31, 23, 11, 10]), 23),
        (Series([30, 10, 5, 100], index=["a", "b", "c", "d"]), "d"),
    ],
)
def test_idxmax(series, expected_index):
    """
    Series.idxmax is NOT a function.
    """
    assert series.idxmax == expected_index


@pytest.mark.parametrize(
    ["series", "expected_series"],
    [
        (Series([10, 20, 30]), Series([nan, 10, 10])),
        (Series(20, nan, 30, 40), Series([nan, nan, nan, 10])),
        (
            Series(2, 4, 8, 16, index=["a", "b", "c", "d"]),
            Series([nan, 2, 4, 8], index=["a", "b", "c", "d"]),
        ),
    ],
)
def test_diff(series, expected_series):
    """
    Should only do 1st order difference
    """
    assert series.diff().eq(expected_series)


@pytest.mark.parametrize(
    ["series", "index", "value", "expected_series"],
    [
        (Series([10, 20]), 0, 100, Series([100, 20])),
        (
            Series([10, 20, 30], index=["a", "b", "c"]),
            "b",
            0,
            Series([10, 0, 30], index=["a", "b", "c"]),
        ),
    ],
)
def test_in_place_assignment_by_index(series, index, value, expected_series):
    series.loc[index] = value

    assert series.equals(expected_series)


@pytest.mark.parametrize(
    ["series", "location", "value", "expected_series"],
    [
        (Series([10, 20]), 0, 100, Series([100, 20])),
        (
            Series([10, 20, 30], index=["a", "b", "c"]),
            1,
            0,
            Series([10, 0, 30], index=["a", "b", "c"]),
        ),
    ],
)
def test_in_place_assignment_by_iloc(series, location, value, expected_series):
    series.iloc[location] = value

    assert series.equals(expected_series)
