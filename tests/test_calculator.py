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
