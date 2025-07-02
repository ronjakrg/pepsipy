import pandas as pd
import plotly.graph_objects as go


from pepsi.features import (
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
from pepsi.plots import (
    _generate_plots,
    _aa_distribution,
    _hydropathy_profile,
    _classification,
    _compare_features,
    _compare_feature,
)


class Calculator:
    """
    The central interface for using the PEPSI package.
    Computes peptide-specific of dataset-specific features and plots based on defined parameters.
    """

    dataset: pd.DataFrame
    seq: str
    feature_params: dict
    plot_params: dict
    computed_features: pd.DataFrame

    def __init__(
        self,
        dataset=None,
        seq=None,
        feature_params=None,
        plot_params=None,
        computed_features=None,
    ):
        self.dataset = dataset
        self.seq = seq
        self.feature_params = feature_params
        self.plot_params = plot_params
        self.computed_features = computed_features

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

    # Utils
    def _ensure_attrs(self, *attrs):
        """
        Raises an error if a given attribute wasn't defined before.
        """
        missing = [a for a in attrs if getattr(self, a) is None]
        if missing:
            msg = f"The following information is not available: {missing}. Please execute the corresponding set or get methods first."
            raise ValueError(msg)

    # Features
    def get_features(self) -> pd.DataFrame:
        """
        Computes a pandas DataFrame with selected features for the entire dataset.
        """
        self._ensure_attrs("feature_params", "dataset")
        self.computed_features = _compute_features(
            params=self.feature_params, df=self.dataset
        )
        return self.computed_features

    def get_peptide_features(self) -> pd.DataFrame:
        """
        Computes a pandas DataFrame with selected features for a given peptide sequence.
        """
        self._ensure_attrs("feature_params", "seq")
        return _compute_features(params=self.feature_params, seq=self.seq)

    seq_length = staticmethod(_seq_length)
    aa_frequency = staticmethod(_aa_frequency)
    molecular_weight = staticmethod(_molecular_weight)
    three_letter_code = staticmethod(_three_letter_code)
    one_letter_code = staticmethod(_one_letter_code)
    gravy = staticmethod(_gravy)
    molecular_formula = staticmethod(_molecular_formula)
    isoelectric_point = staticmethod(_isoelectric_point)
    aromaticity = staticmethod(_aromaticity)
    aa_classification = staticmethod(_aa_classification)

    # Plots
    def get_peptide_plots(self) -> list[go.Figure]:
        """
        Generates plots for the given peptide sequence.
        """
        self._ensure_attrs("plot_params", "seq")
        return _generate_plots(
            seq=self.seq,
            params=self.plot_params,
        )

    def get_dataset_plots(self) -> list[go.Figure]:
        """
        Generates plots for the entire dataset.
        """
        self._ensure_attrs("plot_params", "computed_features")
        return _generate_plots(
            df=self.computed_features,
            params=self.plot_params,
        )

    def get_plots(self):
        """
        Generates plots for the given peptide sequence and the entire dataset,
        seperated into two lists of plots.
        """
        self._ensure_attrs("plot_params", "computed_features", "seq")
        return _generate_plots(
            df=self.computed_features,
            seq=self.seq,
            params=self.plot_params,
        )

    aa_distribution = staticmethod(_aa_distribution)
    hydropathy_profile = staticmethod(_hydropathy_profile)
    classification = staticmethod(_classification)
    compare_features = staticmethod(_compare_features)
    compare_feature = staticmethod(_compare_feature)
