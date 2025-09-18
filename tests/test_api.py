import pytest
import plotly.graph_objects as go

from pepsipy import Calculator
from pepsipy.features import FEATURES
from pepsipy.plots import PLOTS
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


def test_set_plot_params():
    calc = Calculator()
    calc.set_plot_params(hydropathy_profile=True)
    assert ("hydropathy_profile", True) in calc.plot_params.items()
    assert ("titration_curve", False) in calc.plot_params.items()
    assert "self" not in calc.plot_params.keys()


def test_ensure_attrs():
    calc = Calculator()
    with pytest.raises(ValueError) as e:
        calc.get_features()
    assert "not available" in str(e.value)
    calc.setup(dataset=PEPTIDES, seq="SVIDQSRVLNLGPITR")
    with pytest.raises(ValueError) as e:
        calc.get_plots()
    assert "not available" in str(e.value)


def test_get_features_with_params():
    calc = Calculator(dataset=PEPTIDES, feature_params={"gravy": True})
    res = calc.get_features()
    assert len(PEPTIDES.columns) + 1 == len(res.columns)
    assert -0.3 == res["GRAVY"][0]


def test_get_features_without_params():
    calc = Calculator(dataset=PEPTIDES)
    res = calc.get_features()
    assert len(FEATURES) + len(PEPTIDES.columns) == len(res.columns)


def test_get_peptide_features_with_params():
    calc = Calculator(seq="SVIDQSRVLNLGPITR", feature_params={"gravy": True})
    res = calc.get_peptide_features()
    assert 2 == len(res.columns)
    assert 0.075 == res["GRAVY"][0]


def test_get_peptide_features_without_params():
    calc = Calculator(seq="SVIDQSRVLNLGPITR")
    res = calc.get_peptide_features()
    assert len(FEATURES) + 1 == len(res.columns)


def test_get_plots_for_seq_with_params():
    calc = Calculator(
        seq="SVIDQSRVLNLGPITR",
        plot_params={"hydropathy_profile": True},
    )
    plots = calc.get_plots()
    assert 1 == len(plots)
    assert isinstance(plots[0], go.Figure)


def test_get_plots_for_dataset_with_params():
    calc = Calculator(
        dataset=PEPTIDES,
        metadata=METADATA,
        feature_params={"molecular_weight": True},
        plot_params={
            "raincloud": True,
            "raincloud_feature": "Molecular weight",
            "raincloud_group_by": "Group",
            "raincloud_log_scaled": True,
        },
    )
    calc.get_features()
    plots = calc.get_plots()
    assert 1 == len(plots)
    assert isinstance(plots[0], go.Figure)


def test_get_plots_without_params():
    calc = Calculator(dataset=PEPTIDES, metadata=METADATA, seq="SVIDQSRVLNLGPITR")
    calc.get_features()
    plots = calc.get_plots()
    assert len(PLOTS) == len(plots)


def test_get_plots_as_tuple():
    calc = Calculator(dataset=PEPTIDES, metadata=METADATA, seq="SVIDQSRVLNLGPITR")
    calc.get_features()
    plots = calc.get_plots(as_tuple=True)
    assert 2 == len(plots)
    assert len(PLOTS) == len(plots[0] + plots[1])
