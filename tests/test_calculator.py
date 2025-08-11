import pandas as pd

from pepsi import Calculator
from tests.constants import PEPTIDES, METADATA


def test_init():
    calc = Calculator(
        dataset=PEPTIDES,
        metadata=METADATA,
        seq="SVIDQSRVLNLGPITR",
    )
    assert PEPTIDES.equals(calc.dataset)
    assert METADATA.equals(calc.metadata)
    assert list(METADATA.columns) == calc.metadata_list
    assert METADATA.columns[0] == calc.key_metadata


def test_set_feature_params():
    calc = Calculator()
    calc.set_feature_params(gravy=True)
    assert ("gravy", True) in calc.feature_params.items()
    assert ("molecular_weight", False) in calc.feature_params.items()
    assert "self" not in calc.feature_params.keys()


def test_set_feature_params():
    calc = Calculator()
    calc.set_plot_params(hydropathy_profile=True)
    assert ("hydropathy_profile", True) in calc.plot_params.items()
    assert ("titration_curve", False) in calc.plot_params.items()
    assert "self" not in calc.plot_params.keys()
