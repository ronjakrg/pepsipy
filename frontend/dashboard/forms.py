from django import forms

from pepsipy.features import FEATURES

# Numeric features available for comparison
numeric_feature_choices = tuple(
    (f.label, f.label) for f in FEATURES.values() if f.numeric
)


class ConfigForm(forms.Form):
    data_name = forms.CharField(
        label="Name of dataset in /data (.csv)",
        max_length=100,
        initial="peptides.csv",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    metadata_name = forms.CharField(
        label="Name of metadata file in /data (.csv)",
        max_length=100,
        initial="metadata.csv",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    seq = forms.CharField(
        label="Peptide sequence of interest",
        max_length=100,
        initial="SVIDQSRVLNLGPITR",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )


# Feature forms
class MolecularWeightForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["molecular_weight"].label,
        required=False,
    )


class ThreeLetterCodeForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["three_letter_code"].label,
        required=False,
    )


class MolecularFormulaForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["molecular_formula"].label,
        required=False,
    )


class SeqLengthForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["seq_length"].label,
        required=False,
    )


class AromaticityForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["aromaticity"].label,
        required=False,
    )


class AliphaticIndexForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["aliphatic_index"].label,
        required=False,
    )


class ChargeForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["charge_at_ph"].label,
        required=False,
    )
    charge_at_ph_level = forms.FloatField(
        label="pH level",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )


class ChargeDensityForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["charge_density"].label,
        required=False,
    )
    charge_density_level = forms.FloatField(
        label="pH level",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )


class IsoelectricPointForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["isoelectric_point"].label,
        required=False,
    )
    isoelectric_point_option = forms.ChoiceField(
        label="Option",
        choices=(
            ("bjellqvist", "Bjellqvist"),
            ("kozlowski", "IPC 2.0 by Kozlowski"),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class GravyForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["gravy"].label,
        required=False,
    )


class ExtinctionCoefficientForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["extinction_coefficient"].label,
        required=False,
    )
    extinction_coefficient_oxidized = forms.ChoiceField(
        label="Cysteine oxidation state",
        choices=(
            ("False", "Reduced"),
            ("True", "Oxidized"),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class BomanIndexForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["boman_index"].label,
        required=False,
    )


class InstabilityIndexForm(forms.Form):
    selected = forms.BooleanField(
        label=FEATURES["instability_index"].label,
        required=False,
    )


# Plot forms
class AaDistributionForm(forms.Form):
    selected = forms.BooleanField(
        label="Amino acid frequency",
        required=False,
    )
    aa_distribution_order_by = forms.ChoiceField(
        label="Order",
        choices=(
            ("frequency", "Frequency"),
            ("alphabetical", "Alphabetically"),
            ("classes chemical", "Chemical classes"),
            ("classes charge", "Charge classes"),
            ("hydropathy", "Hydropathy index"),
            ("weight", "Molecular weight"),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    aa_distribution_show_all = forms.ChoiceField(
        label="Show all amino acids",
        choices=((True, "Yes"), (False, "No")),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class ClassificationForm(forms.Form):
    selected = forms.BooleanField(
        label="Amino acid classification",
        required=False,
    )
    classification_classify_by = forms.ChoiceField(
        label="Class",
        choices=(
            ("chemical", "Chemical"),
            ("charge", "Charge"),
        ),
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class HydropathyProfileForm(forms.Form):
    selected = forms.BooleanField(
        label="Hydropathy profile",
        required=False,
    )


class TitrationCurveForm(forms.Form):
    selected = forms.BooleanField(
        label="Titration curve (charge vs. pH)",
        required=False,
    )


class CompareFeaturesForm(forms.Form):
    selected = forms.BooleanField(
        label="Compare two features",
        required=False,
    )
    compare_features_a = forms.ChoiceField(
        label="Feature on x-axis",
        choices=numeric_feature_choices,
        initial=("Sequence length", "Sequence length"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    compare_features_b = forms.ChoiceField(
        label="Feature on y-axis",
        choices=numeric_feature_choices,
        initial=("Molecular weight", "Molecular weight"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    compare_features_group_by = forms.ChoiceField(
        label="Group by metadata aspect",
        choices=(),  # Overridden by __init__
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    compare_features_intensity_threshold = forms.FloatField(
        label="Intensity threshold",
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, metadata_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        if metadata_choices is not None:
            self.fields["compare_features_group_by"].choices = metadata_choices


class CompareFeatureForm(forms.Form):
    selected = forms.BooleanField(
        label="Compare one feature",
        required=False,
    )
    compare_feature_a = forms.ChoiceField(
        label="Feature",
        choices=numeric_feature_choices,
        initial=("GRAVY", "GRAVY"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    compare_feature_group_by = forms.ChoiceField(
        label="Group by metadata aspect",
        choices=(),  # Overridden by __init__
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    compare_feature_intensity_threshold = forms.FloatField(
        label="Intensity threshold",
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, metadata_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        if metadata_choices is not None:
            self.fields["compare_feature_group_by"].choices = metadata_choices


class RaincloudForm(forms.Form):
    selected = forms.BooleanField(
        label="Raincloud plot",
        required=False,
    )
    raincloud_feature = forms.ChoiceField(
        label="Feature",
        choices=numeric_feature_choices,
        initial=("GRAVY", "GRAVY"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    raincloud_group_by = forms.ChoiceField(
        label="Group by metadata aspect",
        choices=(),  # Overridden by __init__
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    raincloud_log_scaled = forms.ChoiceField(
        label="Scale of x-axis",
        choices=(
            ("True", "Logarithmic (log10)"),
            ("False", "Linear"),
        ),
        initial=("True", "Logarithmic (log10)"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, metadata_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        if metadata_choices is not None:
            self.fields["raincloud_group_by"].choices = metadata_choices


class MannWhitneyForm(forms.Form):
    selected = forms.BooleanField(
        label="Mann-Whitney U test",
        required=False,
    )
    mann_whitney_feature = forms.ChoiceField(
        label="Feature",
        choices=numeric_feature_choices,
        initial=("GRAVY", "GRAVY"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    mann_whitney_group_by = forms.ChoiceField(
        label="Group by metadata aspect",
        choices=(),  # Overridden by __init__
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    mann_whitney_group_a = forms.CharField(
        label="First comparison group",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    mann_whitney_group_b = forms.CharField(
        label="Second comparison group",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    mann_whitney_alternative = forms.ChoiceField(
        label="Alternative hypothesis",
        choices=(
            ("two-sided", "Two-sided"),
            ("greater", "Greater"),
            ("less", "Less"),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, metadata_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        if metadata_choices is not None:
            self.fields["mann_whitney_group_by"].choices = metadata_choices


FORM_TO_FEATURE_FUNCTION = {
    MolecularWeightForm: "molecular_weight",
    ThreeLetterCodeForm: "three_letter_code",
    MolecularFormulaForm: "molecular_formula",
    SeqLengthForm: "seq_length",
    AromaticityForm: "aromaticity",
    AliphaticIndexForm: "aliphatic_index",
    ChargeForm: "charge_at_ph",
    ChargeDensityForm: "charge_density",
    IsoelectricPointForm: "isoelectric_point",
    GravyForm: "gravy",
    ExtinctionCoefficientForm: "extinction_coefficient",
    BomanIndexForm: "boman_index",
    InstabilityIndexForm: "instability_index",
}
FORM_TO_PLOT_FUNCTION = {
    AaDistributionForm: "aa_distribution",
    ClassificationForm: "classification",
    HydropathyProfileForm: "hydropathy_profile",
    TitrationCurveForm: "titration_curve",
    CompareFeaturesForm: "compare_features",
    CompareFeatureForm: "compare_feature",
    RaincloudForm: "raincloud",
    MannWhitneyForm: "mann_whitney",
}
