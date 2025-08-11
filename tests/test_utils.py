import pytest

import pandas as pd
from plotly import exceptions

from pepsi.utils import (
    sanitize_seq,
    get_column_name,
    get_distinct_seq,
    normalize_color,
    extract_related_kwargs,
)
from .constants import PEPTIDES


def test_sanitize_seq():
    assert "PEPTIDE" == sanitize_seq("pEPtiDe :)")


def test_get_column_name():
    assert "Intensity" == get_column_name(PEPTIDES, "intensity")
    normalized = PEPTIDES.rename(columns={"Intensity": "Normalized intensity"})
    assert "Normalized intensity" == get_column_name(normalized, "intensity")
    with pytest.raises(ValueError) as e:
        get_column_name(PEPTIDES, "test")
    assert "could not be found" in str(e.value)


def test_get_distinct_seq():
    assert pd.DataFrame(
        {
            "Sequence": [
                "SRVLNLGPITRK",
                "PPPPPLGAPPPPPP",
                "NDPFANKDDPFYYDWKNLQ",
                "EEGEFEEEAEEEVA",
                "GPPGPPGPPGHPGPQGPPG",
                "VEWESNGQPENNYKTTPPVL",
            ]
        }
    ).equals(get_distinct_seq(PEPTIDES))


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
