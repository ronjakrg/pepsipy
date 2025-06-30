import pandas as pd
import plotly.graph_objects as go


from peptidefeatures.features import (
    _compute_features,
    _seq_length,
    _aa_frequency,
    _molecular_weight,
    _three_letter_code,
    _one_letter_code,
    _gravy,
    _molecular_formula,
    _isoelectric_point,
    _aromaticity,
    _aa_classification,
)
from peptidefeatures.plots import (
    _generate_plots,
    _aa_distribution,
    _hydropathy_profile,
    _classification,
    _compare_features,
    _compare_feature,
)


class Calculator:
    """TODO"""

    dataset: pd.DataFrame
    seq: str
    feature_params: dict
    plot_params: dict

    def __init__(
        self,
        dataset=None,
        seq=None,
    ):
        self.dataset = dataset
        self.seq = seq

    # Setter
    def set_dataset(self, dataset: pd.DataFrame):
        self.dataset = dataset

    def set_seq(self, seq: str):
        self.seq = seq

    def set_feature_params(
        self,
        three_letter_code: bool = False,
        molecular_formula: bool = False,
        seq_length: bool = False,
        molecular_weight: bool = False,
        gravy: bool = False,
        isoelectric_point: bool = False,
        isoelectric_point_option: str = "bjellqvist",
        aromaticity: bool = False,
    ):
        params = locals().copy()
        params.pop("self")
        self.feature_params = params

    def set_plot_params(
        self,
        aa_distribution: bool = False,
        aa_distribution_order_by: str = "frequency",
        aa_distribution_show_all: bool = False,
        hydropathy_profile: bool = False,
        classification: bool = False,
        classification_classify_by: str = "chemical",
        compare_features: bool = False,
        compare_features_a: str = "Sequence length",
        compare_features_b: str = "Molecular weight",
        compare_features_groups: list = None,
        compare_features_intensity_threshold: float = None,
        compare_feature: bool = False,
        compare_feature_a: str = "GRAVY",
        compare_feature_groups: list = None,
        compare_feature_intensity_threshold: float = None,
    ):
        params = locals().copy()
        params.pop("self")
        self.plot_params = params

    # Features
    def get_features(self) -> pd.DataFrame:
        """TODO"""
        if self.dataset is None:
            raise ValueError(
                "No dataset loaded. Please choose a pd.DataFrame by using set_dataset() first."
            )
        return _compute_features(params=self.feature_params, df=self.dataset)

    def get_peptide_features(self) -> pd.DataFrame:
        """TODO"""
        if self.seq is None:
            raise ValueError(
                "No sequence chosen. Please enter a sequence by using set_seq() first."
            )
        return _compute_features(params=self.feature_params, seq=self.seq)

    seq_length = _seq_length
    aa_frequency = _aa_frequency
    molecular_weight = _molecular_weight
    three_letter_code = _three_letter_code
    one_letter_code = _one_letter_code
    gravy = _gravy
    molecular_formula = _molecular_formula
    isoelectric_point = _isoelectric_point
    aromaticity = _aromaticity
    aa_classification = _aa_classification

    # Plots
    def get_peptide_plots(self) -> list[go.Figure]:
        """TODO"""
        if self.seq is None:
            raise ValueError(
                "No sequence chosen. Please enter a sequence by using set_seq() first."
            )
        return _generate_plots(
            seq=self.seq,
            params=self.plot_params,
        )

    def get_dataset_plots(self) -> list[go.Figure]:
        """TODO"""
        if self.dataset is None:
            raise ValueError(
                "No dataset loaded. Please choose a pd.DataFrame by using set_dataset() first."
            )
        return _generate_plots(
            df=self.dataset,
            params=self.plot_params,
        )

    def get_plots(self) -> list[go.Figure]:
        """TODO"""
        if self.dataset is None:
            raise ValueError(
                "No dataset loaded. Please choose a pd.DataFrame by using set_dataset() first."
            )
        if self.seq is None:
            raise ValueError(
                "No sequence chosen. Please enter a sequence by using set_seq() first."
            )
        return _generate_plots(
            df=self.set_dataset,
            seq=self.seq,
            params=self.plot_params,
        )

    aa_distribution = _aa_distribution
    hydropathy_profile = _hydropathy_profile
    classification = _classification
    compare_features = _compare_features
    compare_feature = _compare_feature
