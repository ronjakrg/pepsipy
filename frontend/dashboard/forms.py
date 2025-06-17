from django import forms

# TODO Rethink mapping feature field -> parameter fields (to collapse them if feature is unchecked)

feature_choices = (
    ("Molecular weight", "Molecular weight"),
    ("Isoelectric point", "Isoelectric point"),
    ("Sequence length", "Sequence length"),
    ("GRAVY", "GRAVY"),
    ("Aromaticity", "Aromaticity"),
)
feature_fields = [
    "three_letter_code",
    "molecular_formula",
    "seq_length",
    "molecular_weight",
    "gravy",
    "isoelectric_point",
    "aromaticity",
    "aa_distribution",
    "hydropathy_profile",
    "classification",
    "scatter_features",
    "box_feature",
]


class GeneralForm(forms.Form):
    data_name = forms.CharField(
        label="Name of dataset in /data (.csv)",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    peptide_of_interest = forms.CharField(
        label="Peptide sequence of interest",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )


class PeptideForm(forms.Form):
    three_letter_code = forms.BooleanField(
        label="Three letter code",
        required=False,
    )
    molecular_formula = forms.BooleanField(
        label="Molecular formula",
        required=False,
    )
    seq_length = forms.BooleanField(
        label="Sequence length",
        required=False,
    )
    molecular_weight = forms.BooleanField(
        label="Molecular weight",
        required=False,
    )
    gravy = forms.BooleanField(
        label="GRAVY",
        required=False,
    )
    isoelectric_point = forms.BooleanField(
        label="Isoelectric point",
        required=False,
    )
    isoelectric_point_method = forms.ChoiceField(
        label="Method",
        choices=(
            ("bjellqvist", "Bjellqvist"),
            ("kozlowski", "IPC 2.0 by Kozlowski"),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    aromaticity = forms.BooleanField(
        label="Aromaticity",
        required=False,
    )
    aa_distribution = forms.BooleanField(
        label="📈 Frequency of amino acids",
        required=False,
    )
    aa_distribution_order = forms.ChoiceField(
        label="Order of amino acids",
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
    aa_distribution_showall = forms.ChoiceField(
        label="Show all amino acids",
        choices=((True, "Yes"), (False, "No")),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    hydropathy_profile = forms.BooleanField(
        label="📈 Hydropathy profile",
        required=False,
    )
    classification = forms.BooleanField(
        label="📈 Classification",
        required=False,
    )
    classification_class = forms.ChoiceField(
        label="Class",
        choices=(
            ("chemical", "Chemical"),
            ("charge", "Charge"),
        ),
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class DatasetForm(forms.Form):
    scatter_features = forms.BooleanField(
        label="📈 Compare features across groups",
        required=False,
    )
    scatter_features_a = forms.ChoiceField(
        label="Feature on x-axis",
        choices=feature_choices,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    scatter_features_b = forms.ChoiceField(
        label="Feature on y-axis",
        choices=feature_choices,
        initial=("Sequence length", "Sequence length"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    scatter_features_groups = forms.CharField(
        label="Group prefixes, seperated by semicolons",
        max_length=100,
        required=False,
        initial="AD; CTR",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    scatter_features_intensity = forms.FloatField(
        label="Intensity threshold",
        required=False,
        initial=0.01,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    box_feature = forms.BooleanField(
        label="📈 Compare a feature across groups",
        required=False,
    )
    box_feature_a = forms.ChoiceField(
        label="Feature",
        choices=feature_choices,
        initial=("GRAVY", "GRAVY"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    box_feature_groups = forms.CharField(
        label="Group prefixes, seperated by semicolons",
        max_length=100,
        required=False,
        initial="AD; CTR",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    box_feature_intensity = forms.FloatField(
        label="Intensity threshold",
        required=False,
        initial=0.01,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
