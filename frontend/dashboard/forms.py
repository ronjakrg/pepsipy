from django import forms


class FeatureForm(forms.Form):
    dataset_name = forms.CharField(
        label="Name of dataset in /data (.csv)",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    peptide_of_interest = forms.CharField(
        label="Peptide of interest",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    # Features & Options
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
