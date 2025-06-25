import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from django.conf import settings
from django.urls import reverse
from unittest.mock import patch, MagicMock

from frontend.dashboard.utils import (
    load_data,
    get_params,
    get_match_for_seq,
)
from frontend.dashboard.views import overview
from frontend.dashboard.forms import (
    ThreeLetterCodeForm,
    MolecularFormulaForm,
    IsoelectricPointForm,
)
from peptidefeatures.features import FeatureParams


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
        ThreeLetterCodeForm(data={"select": "on"}),
        MolecularFormulaForm(data={}),
        IsoelectricPointForm(
            data={
                "select": "on",
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
    # TODO Write test as soon as dynamic columns are implemented
    pass


@patch("frontend.dashboard.views.load_data")
@patch("frontend.dashboard.views.compute_features")
@patch("frontend.dashboard.views.get_match_for_seq")
@patch("frontend.dashboard.views.generate_plots")
@patch("frontend.dashboard.views.get_params")
def test_overview_valid_form(
    mock_get_params,
    mock_generate_plots,
    mock_get_match_for_seq,
    mock_compute_features,
    mock_load_data,
    client,
):
    # Setup
    peptides = pd.DataFrame({"Sequence": ["PEPTIDE"]})
    features = pd.DataFrame(
        {
            "Sequence": ["PEPTIDE"],
            "Feature": [0.5],
        }
    )
    mock_load_data.return_value = peptides
    params = FeatureParams()
    mock_compute_features.return_value = peptides
    mock_get_match_for_seq.return_value = (1, features)
    mock_get_params.side_effect = [{}, {}]
    plot_a = MagicMock()
    plot_a.to_html.return_value = "<div>plot_a</div>"
    plot_b = MagicMock()
    plot_b.to_html.return_value = "<div>plot_b</div>"
    mock_generate_plots.return_value = ([plot_a], [plot_b])

    # Execute
    url = reverse("overview")
    response = client.post(
        url,
        data={
            "data_name": "peptides.csv",
            "seq": "PEPTIDE",
        },
    )

    # Assert
    assert response.status_code == 200
    mock_load_data.assert_called_once_with("peptides.csv")
    mock_compute_features.assert_called_once_with(
        df=peptides,
        params=params,
    )
    mock_get_match_for_seq.assert_called_once_with(peptides, "PEPTIDE")
    mock_generate_plots.assert_called_once()
    assert "<div>plot_a</div>" in response.context["peptide_plots"][0]
    assert "<div>plot_b</div>" in response.context["data_plots"][0]
    assert "PEPTIDE" == response.context["seq"]
    assert False == response.context["computed_features"].empty
    assert_frame_equal(features, response.context["computed_peptide_features"])
