import pytest

import pandas as pd

from constants import TEST_DATA
from pepsi.utils import (
    sanitize_seq,
    get_column_name,
    get_distinct_seq,
    extract_related_kwargs,
)


def test_sanitize_seq():
    assert "PEPTIDE" == sanitize_seq("pEPtiDe :)")


def test_get_column_name():
    assert "Sequence" == get_column_name(TEST_DATA, "sequence")
    with pytest.raises(ValueError) as e:
        get_column_name(TEST_DATA, "test")
    assert "could not be found" in str(e.value)


def test_get_distinct_seq():
    assert get_distinct_seq(TEST_DATA).equals(
        pd.DataFrame({"Sequence": ["FSGVPDR", "VTISVDK"]})
    )


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
