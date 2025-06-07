import pytest

import pandas as pd

from constants import TEST_DATA
from peptidefeatures.utils import (
    sanitize_seq,
    get_group,
    get_seq_column_name,
    get_distinct_seq,
)


def test_sanitize_seq():
    assert "PEPTIDE" == sanitize_seq("pEPtiDe :)")


def test_get_group():
    groups = ["AD", "CTR"]
    assert "AD" == get_group("AD01_C1_INSOLUBLE_01", groups)
    assert "None" == get_group(":)", groups)


def test_get_seq_column_name():
    assert "Sequence" == get_seq_column_name(TEST_DATA)
    with pytest.raises(ValueError) as e:
        get_seq_column_name(pd.DataFrame())
    assert "None of the containing columns are recognized" in str(e.value)


def test_get_distinct_seq():
    assert get_distinct_seq(TEST_DATA).equals(
        pd.DataFrame({"Sequence": ["FSGVPDR", "VTISVDK"]})
    )
