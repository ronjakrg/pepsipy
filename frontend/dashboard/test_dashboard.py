import pytest
import pandas as pd

from frontend.dashboard.utils import (
    load_data,
    get_params,
    get_match_for_seq,
)
from frontend.dashboard.views import index
from frontend.dashboard.forms import (
    ThreeLetterCodeForm,
    MolecularFormulaForm,
    IsoelectricPointForm,
)


def test_load_data(tmp_path, settings):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    csv_file = data_dir / "peptides.csv"
    csv_file.write_text(
        "Sample,Protein ID,Sequence,Intensity,PEP\nAD01_C1_INSOLUBLE_01,A0A075B6S2,FSGVPDR,936840.0,0.0068633"
    )
    settings.PROJECT_DIR = str(tmp_path)

    expected = pd.DataFrame(
        {
            "Sample": ["AD01_C1_INSOLUBLE_01"],
            "Protein ID": ["A0A075B6S2"],
            "Sequence": ["FSGVPDR"],
            "Intensity": [936840.0],
            "PEP": [0.0068633],
        }
    )
    pd.testing.assert_frame_equal(expected, load_data("peptides.csv"))


def test_load_data_wrong_name(tmp_path, settings):
    (tmp_path / "data").mkdir()
    settings.PROJECT_DIR = str(tmp_path)

    with pytest.raises(FileNotFoundError) as e:
        load_data("peptide")
    assert "could not be found" in str(e.value)


def test_get_params():
    forms = [
        ThreeLetterCodeForm(data={"selected": "on"}),
        MolecularFormulaForm(data={}),
        IsoelectricPointForm(
            data={
                "selected": "on",
                "isoelectric_point_option": "bjellqvist",
            }
        ),
    ]
    mapping = {
        ThreeLetterCodeForm: "three_letter_code",
        MolecularFormulaForm: "molecular_formula",
        IsoelectricPointForm: "isoelectric_point",
    }
    expected = {
        "three_letter_code": True,
        "molecular_formula": False,
        "isoelectric_point": True,
        "isoelectric_point_option": "bjellqvist",
    }
    assert expected == get_params(forms, mapping)


def test_get_match_for_seq():
    data = pd.DataFrame(
        {
            "Sample": ["AD01_C1_INSOLUBLE_01", "CTR01_C1_INSOLUBLE_01"],
            "Protein ID": ["A0A075B6S2", "A0A075B6S2"],
            "Sequence": ["FSGVPDR", "PEPTIDE"],
            "Intensity": [936840.0, "NaN"],
            "PEP": [0.0068633, 0.0056387],
            "GRAVY": [2.0, 1.0],
        }
    )
    seq = "PEPTIDE"
    expected_match = {
        "Sequence": "PEPTIDE",
        "GRAVY": 1.0,
    }
    assert (1, expected_match) == get_match_for_seq(data, "PEPTIDE")
    assert (0, {}) == get_match_for_seq(data, "PEP")
