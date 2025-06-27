# TODO
# Set sample / group / batch as column names
# All features
# All plots
# Params

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
    """ """

    dataset: pd.DataFrame
    peptide: str

    feature_params: dict
    plot_params: dict

    def __init__(self, peptide):
        self.peptide = peptide

    def say_peptide(self):
        print(self.peptide)

    # Features
    def compute_features(self):
        return compute_features(
            params=self.feature_params,
            df=self.dataset,
            seq=self.peptide,
        )

    def seq_length(seq: str) -> int:
        return

    def aa_frequency(seq: str) -> dict[str, int]:
        return

    def molecular_weight(seq: str) -> float:
        return

    def three_letter_code(seq: str) -> str:
        return

    def one_letter_code(codes: str) -> str:
        return

    def gravy(seq: str) -> float:
        return

    def molecular_formula(seq: str) -> str:
        return

    def isoelectric_point(seq: str, option: str = "bjellqvist") -> float:
        return

    def aromaticity(seq: str) -> float:
        return

    def aa_classification(seq: str, classify_by: str = "chemical") -> dict:
        return

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
