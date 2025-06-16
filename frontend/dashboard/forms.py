from django import forms

FEATURE_CHOICES = [
    ("three_letter_code", "Three letter code"),
    ("molecular_formula", "Molecular formula"),
    ("molecular_weight", "Molecular weight")
]

class FeatureForm(forms.Form):
    dataset_name = forms.CharField(
        label="Name of dataset in /data (.csv)",
        max_length = 100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    peptide_of_interest = forms.CharField(
        label="Peptide of interest",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )