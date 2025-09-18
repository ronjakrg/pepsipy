import pandas as pd
import plotly.io as pio

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
    _charge_at_ph,
    _charge_density,
    _boman_index,
    _aliphatic_index,
    _extinction_coefficient,
)
from pepsi.plots import (
    _generate_plots,
    _aa_distribution,
    _hydropathy_profile,
    _classification,
    _titration_curve,
    _compare_features,
    _compare_feature,
    _raincloud,
    _mann_whitney_u_test,
)
from pepsi.constants import PROJECT_PATH, DATA_PATH


class Calculator:
    """
    The central interface for using the PEPSI package. Computes peptide-specific of dataset-specific features and plots based on defined parameters.
        dataset: pandas DataFrame containing the peptidomic data. The column 'Sequence' must contain the amino acid sequences. Columns 'Protein ID', 'Intensity' and 'PEP' are optional. To link the metadata file, the first metadata column must be added to the dataset.
        metadata: pandas DataFrame containing the metadata. The first column must contain unique identifiers (used as the key). All other columns can provide additional information for each key (e.g., group, batch, ...).
        seq: Amino acid sequence of interest
        feature_params: Dictionary containing all available features and their associated parameters. Use set_feature_params() seperately to get an overview on all options.
        plot_params: Dictionary containing all available plots and their associated parameters. Use set_plot_params() seperately to get an overview on all options.
    """

    dataset: pd.DataFrame
    metadata: pd.DataFrame
    metadata_list: list[str]
    key_metadata: str
    seq: str
    feature_params: dict
    plot_params: dict
    computed_features: pd.DataFrame

    def __init__(
        self,
        dataset: pd.DataFrame = None,
        metadata: pd.DataFrame = None,
        seq: str = None,
        feature_params: dict = None,
        plot_params: dict = None,
    ):
        self.dataset = None
        self.metadata = None
        self.seq = None
        self.setup(
            dataset=dataset,
            metadata=metadata,
            seq=seq,
        )
        self.feature_params = feature_params
        self.plot_params = plot_params
        self.computed_features = None

    # Setup
    def setup(
        self,
        dataset: pd.DataFrame = None,
        metadata: pd.DataFrame = None,
        seq: str = None,
    ):
        """
        Sets up relevant input data for computing features or generating plots.
            dataset: pandas DataFrame containing the peptidomic data. The column 'Sequence' must contain the amino acid sequences. Columns 'Protein ID', 'Intensity' and 'PEP' are optional. To link the metadata file, the first metadata column must be added to the dataset.
            metadata: pandas DataFrame containing the metadata. The first column must contain unique identifiers (used as the key). All other columns can provide additional information for each key (e.g., group, batch, ...).
            seq: Amino acid sequence of interest
        """
        if dataset is not None:
            self.dataset = dataset
        if metadata is not None:
            self.metadata = metadata
            self.metadata_list = list(metadata.columns)
            self.key_metadata = metadata.columns[0]
        if seq is not None:
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
        charge_at_ph: bool = False,
        charge_at_ph_level: float = 7.0,
        charge_density: bool = False,
        charge_density_level: float = 7.0,
        boman_index: bool = False,
        aliphatic_index: bool = False,
        extinction_coefficient: bool = False,
        extinction_coefficient_oxidized: bool = False,
    ):
        """
        Selects peptide features and their related parameters.
        """
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
        titration_curve: bool = False,
        compare_features: bool = False,
        compare_features_a: str = "Sequence length",
        compare_features_b: str = "Molecular weight",
        compare_features_group_by: str = None,
        compare_features_intensity_threshold: float = None,
        compare_feature: bool = False,
        compare_feature_a: str = "GRAVY",
        compare_feature_group_by: str = None,
        compare_feature_intensity_threshold: float = None,
        raincloud: bool = False,
        raincloud_feature: str = "GRAVY",
        raincloud_group_by: str = None,
        raincloud_log_scaled: bool = True,
        mann_whitney: bool = False,
        mann_whitney_feature: str = "GRAVY",
        mann_whitney_group_by: str = None,
        mann_whitney_group_a: str = None,
        mann_whitney_group_b: str = None,
        mann_whitney_alternative: str = "two-sided",
    ):
        """
        Selects peptide and dataset plots and their related parameters.
        """
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
            if "computed_features" in missing:
                msg = "Computed features are not available. Feature visualisation requires that get_features() has been executed first."
            else:
                msg = f"The following information is not available: {missing}. Please execute the corresponding set or get methods first."
            raise ValueError(msg)

    # Features
    def get_features(self) -> pd.DataFrame:
        """
        Computes selected features on the current dataset. Requires a dataset set by setup().
        Note: If no features were explicitly selected, all available features are computed with their default options.
        """
        self._ensure_attrs("dataset")
        if self.feature_params:
            params = self.feature_params
        else:
            params = {"select_all": True}
        self.computed_features = _compute_features(
            params=params,
            df=self.dataset,
            seq=None,
        )
        return self.computed_features

    def get_peptide_features(self) -> pd.DataFrame:
        """
        Computes selected features on the current peptide sequence of interest. Requires a sequence set by setup().
        Note: If no features were explicitly selected, all available features are computed with their default options.
        """
        self._ensure_attrs("seq")
        if self.feature_params:
            params = self.feature_params
        else:
            params = {"select_all": True}
        return _compute_features(
            params=params,
            df=None,
            seq=self.seq,
        )

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
    charge_at_ph = staticmethod(_charge_at_ph)
    charge_density = staticmethod(_charge_density)
    boman_index = staticmethod(_boman_index)
    aliphatic_index = staticmethod(_aliphatic_index)
    extinction_coefficient = staticmethod(_extinction_coefficient)

    # Plots
    def get_plots(self, as_tuple: bool = False) -> list | tuple:
        """
        Generates selected plots. Requires a sequence or a dataset set by setup().
        Note: If no plots were explicitly selected, all available plots are computed with their default options.
            as_tuple: If set to True, the peptide and dataset plots are returned seperated as tuple.
        """
        if self.plot_params:
            params = self.plot_params
        else:
            params = {"select_all": True}

        # TODO 74: Rethink these if statements
        if any(
            p in params.keys()
            for p in [
                "aa_distribution",
                "hydropathy_profile",
                "classification",
                "titration_curve",
                "select_all",
            ]
        ):
            self._ensure_attrs("seq")
        if any(
            p in params.keys()
            for p in [
                "raincloud",
                "compare_feature",
                "compare_features",
                "mann_whitney",
                "select_all",
            ]
        ):
            self._ensure_attrs("computed_features", "metadata")
            current_features = pd.merge(
                self.computed_features, self.metadata, on=self.key_metadata, how="left"
            )
        else:
            current_features = self.dataset

        plot_tuple = _generate_plots(
            df=current_features,
            seq=self.seq,
            params=params,
        )
        if as_tuple:
            return plot_tuple
        else:
            plots = [plot for sublist in plot_tuple for plot in sublist]
            return plots

    aa_distribution = staticmethod(_aa_distribution)
    hydropathy_profile = staticmethod(_hydropathy_profile)
    classification = staticmethod(_classification)
    titration_curve = staticmethod(_titration_curve)
    compare_features = staticmethod(_compare_features)
    compare_feature = staticmethod(_compare_feature)
    raincloud = staticmethod(_raincloud)
    mann_whitney_u_test = staticmethod(_mann_whitney_u_test)

    # Demonstration: Hello PEPSI!
    @staticmethod
    def hello_pepsi():
        print("✨ Hello PEPSI! ✨")
        # Load data
        dataset = pd.read_csv(DATA_PATH / "peptides.csv")
        metadata = pd.read_csv(DATA_PATH / "metadata.csv")
        print("Loaded input data.")

        # Initialize Calculator instance
        calc = Calculator(
            dataset=dataset,
            metadata=metadata,
            seq="SVIDQSRVLNLGPITR",
        )
        print("Set up calculator.")

        # Select features and plots
        calc.set_feature_params(
            gravy=True,
            molecular_weight=True,
        )
        calc.set_plot_params(
            hydropathy_profile=True,
            classification=True,
            classification_classify_by="charge",
        )
        print("Set feature and plot parameters.")

        # Compute and output results
        print("Printing first five peptides with computed features ...")
        print(calc.get_features().head())
        plots = calc.get_plots()
        i = 1
        for plot in plots:
            pio.write_image(plot, PROJECT_PATH / "results" / f"plot{i}.png", scale=3)
            i += 1
        print(f"You can find all generated plots in '{PROJECT_PATH / "results"}'.")
        print("Successfully executed PEPSI demonstration. Happy coding! 💻🧬")
