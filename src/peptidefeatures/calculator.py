import pandas as pd
import plotly.graph_objects as go


from peptidefeatures.features import (
    compute_features,
    seq_length,
    aa_frequency,
    molecular_weight,
    three_letter_code,
    one_letter_code,
    gravy,
    molecular_formula,
    isoelectric_point,
    aromaticity,
    aa_classification,
)
from peptidefeatures.plots import (
    generate_plots,
    aa_distribution,
    hydropathy_profile,
    classification,
    compare_features,
    compare_feature,
)


class Calculator:
    """ TODO """
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
        if self.dataset is None:
            raise ValueError("No dataset loaded. Please choose a pd.DataFrame by using set_dataset() first.")
        return compute_features(params=self.feature_params, df=self.dataset)

    def get_pep_features(self) -> pd.DataFrame:
        if self.seq is None:
            raise ValueError("No sequence chosen. Please enter a sequence by using set_seq() first.")
        return compute_features(params=self.feature_params, seq=self.seq)

    def seq_length(seq: str) -> int:
        return seq_length(seq)

    def aa_frequency(seq: str) -> dict[str, int]:
        return aa_frequency(seq)

    def molecular_weight(seq: str) -> float:
        return molecular_weight(seq)

    def three_letter_code(seq: str) -> str:
        return three_letter_code(seq)

    def one_letter_code(codes: str) -> str:
        return one_letter_code(codes)

    def gravy(seq: str) -> float:
        return gravy(seq)

    def molecular_formula(seq: str) -> str:
        return molecular_formula(seq)

    def isoelectric_point(seq: str, option: str = "bjellqvist") -> float:
        return isoelectric_point(seq, option)

    def aromaticity(seq: str) -> float:
        return aromaticity(seq)

    def aa_classification(seq: str, classify_by: str = "chemical") -> dict:
        return aa_classification(seq, classify_by)

    def generate_plots() -> list:
        return

    # Plots
    def aa_distribution(
        seq: str,
        order_by: str = "frequency",
        show_all: bool = False,
    ) -> go.Figure:
        return

    def hydropathy_profile(seq: str) -> go.Figure:
        return

    def classification(seq: str, classify_by: str = "chemical") -> go.Figure:
        return

    def compare_features(
        df: pd.DataFrame,
        feature_a: str,
        feature_b: str,
        groups: list = None,
        intensity_threshold: float = None,
    ) -> go.Figure:
        return

    def compare_feature(
        df: pd.DataFrame,
        feature: str,
        groups: list = None,
        intensity_threshold: float = None,
    ) -> go.Figure:
        return
