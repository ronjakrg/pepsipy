import pytest

import pandas as pd
from plotly import exceptions

from constants import TEST_DATA, NORMALIZED_TEST_DATA
from pepsi.utils import (
    sanitize_seq,
    get_column_name,
    get_distinct_seq,
    normalize_color,
    extract_related_kwargs,
)


def test_sanitize_seq():
    assert "PEPTIDE" == sanitize_seq("pEPtiDe :)")


def test_get_column_name():
    assert "Intensity" == get_column_name(TEST_DATA, "intensity")
    assert "Normalized intensity" == get_column_name(NORMALIZED_TEST_DATA, "intensity")
    with pytest.raises(ValueError) as e:
        get_column_name(TEST_DATA, "test")
    assert "could not be found" in str(e.value)


def test_get_distinct_seq():
    assert get_distinct_seq(TEST_DATA).equals(
        pd.DataFrame({"Sequence": ["FSGVPDR", "VTISVDK"]})
    )


def test_normalize_color():
    assert "rgb(13, 8, 135)" == normalize_color(0.0, 0.0, 100.0, "Plasma")
    assert "rgb(182, 48, 139)" == normalize_color(42.0, 0.0, 100.0, "Plasma")
    with pytest.raises(exceptions.PlotlyError) as e:
        normalize_color(42.0, 0.0, 100.0, "Something")
    assert "not a built-in scale" in str(e.value)


def test_extract_related_kwargs():
    mapping = {
        "param_a": "param_1",
        "param_b": "param_2",
        "param_c": "param_3",
    }
    params = {
        "param_a": "foo",
        "param_c": "foo",
        "param_d": "foo",
    }
    expected = {
        "param_1": "foo",
        "param_3": "foo",
    }
    assert expected == extract_related_kwargs(mapping, params)
