import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from django.urls import reverse
from unittest.mock import call, patch, MagicMock

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


@patch("frontend.dashboard.views.load_data")
@patch("frontend.dashboard.views.get_match_for_seq")
@patch("frontend.dashboard.views.get_params")
@patch("frontend.dashboard.views.Calculator")
@patch("frontend.dashboard.views.Path.mkdir")
@patch("frontend.dashboard.views.pd.DataFrame.to_csv")
@patch("frontend.dashboard.views.Path.write_bytes")
def test_index_valid_form(
    mock_write_bytes,
    mock_to_csv,
    mock_mkdir,
    mock_calculator,
    mock_get_params,
    mock_get_match_for_seq,
    mock_load_data,
    client,
):
    # Setup
    mock_calc = MagicMock()
    mock_calculator.return_value = mock_calc
    mock_calc.seq = "PEPTIDE"
    peptides = pd.DataFrame({"Sequence": ["PEPTIDE"]})
    features = pd.DataFrame(
        {
            "Sequence": ["PEPTIDE"],
            "Feature": [0.5],
        }
    )
    mock_load_data.return_value = peptides
    mock_calc.get_features.return_value = peptides
    mock_calc.get_peptide_features.return_value = features
    mock_get_match_for_seq.return_value = (1, features)
    mock_get_params.side_effect = [{}, {}]
    plot_a = MagicMock()
    plot_a.to_html.return_value = "<div>plot_a</div>"
    plot_b = MagicMock()
    plot_b.to_html.return_value = "<div>plot_b</div>"
    mock_calc.get_plots.return_value = ([plot_a], [plot_b])

    # Execute
    url = reverse("index")
    response = client.post(
        url,
        data={
            "data_name": "peptides.csv",
            "metadata_name": "metadata.csv",
            "seq": "PEPTIDE",
            "calculate": "1",
        },
    )

    # Assert
    assert response.status_code == 200
    assert "<div>plot_a</div>" in response.context["peptide_plots"][0]
    assert "<div>plot_b</div>" in response.context["data_plots"][0]
    assert "PEPTIDE" == response.context["seq"]

    mock_load_data.assert_has_calls(
        [
            call("metadata.csv"),
            call("peptides.csv"),
        ]
    )
    mock_get_match_for_seq.assert_called_once_with(peptides, "PEPTIDE")

    mock_calc.set_dataset.assert_called_once_with(peptides)
    mock_calc.set_seq.assert_called_once_with("PEPTIDE")
    mock_calc.set_feature_params.assert_called_once()
    mock_calc.get_features.assert_called_once()
    mock_calc.set_plot_params.assert_called_once()
    mock_calc.get_plots.assert_called_once()
    mock_to_csv.assert_called()
