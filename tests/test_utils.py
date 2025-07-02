import pytest

import pandas as pd

from constants import TEST_DATA
from pepsi.utils import (
    sanitize_seq,
    find_group,
    get_column_name,
    get_distinct_seq,
)


def test_sanitize_seq():
    assert "PEPTIDE" == sanitize_seq("pEPtiDe :)")


def test_find_group():
    groups = ["AD", "CTR"]
    assert "AD" == find_group("AD01_C1_INSOLUBLE_01", groups)
    assert "None" == find_group("AD01_C1_INSOLUBLE_01", None)
    assert "None" == find_group(":)", groups)


def test_get_column_name():
    assert "Sequence" == get_column_name(TEST_DATA, "sequence")
    with pytest.raises(ValueError) as e:
        get_column_name(TEST_DATA, "test")
    assert "could not be found" in str(e.value)


def test_get_distinct_seq():
    assert get_distinct_seq(TEST_DATA).equals(
        pd.DataFrame({"Sequence": ["FSGVPDR", "VTISVDK"]})
    )
