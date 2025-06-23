import pytest
from django.conf import settings
import pandas as pd

from frontend.dashboard.utils import (
    load_data,
    get_params,
    get_features_for_seq,
)
from frontend.dashboard.views import overview


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
    pass


def test_get_features_for_seq():
    pass


def test_overview():
    pass
