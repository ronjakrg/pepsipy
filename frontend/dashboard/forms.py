from django import forms


feature_choices = (
    ("Molecular weight", "Molecular weight"),
    ("Isoelectric point", "Isoelectric point"),
    ("Sequence length", "Sequence length"),
    ("GRAVY", "GRAVY"),
    ("Aromaticity", "Aromaticity"),
)


class GeneralForm(forms.Form):
    data_name = forms.CharField(
        label="Name of dataset in /data (.csv)",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    seq = forms.CharField(
        label="Peptide sequence of interest",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )


class ThreeLetterCodeForm(forms.Form):
    select = forms.BooleanField(
        label="Three letter code",
        required=False,
    )
    func = "three_letter_code"


class MolecularFormulaForm(forms.Form):
    select = forms.BooleanField(
        label="Molecular formula",
        required=False,
    )


class SeqLengthForm(forms.Form):
    select = forms.BooleanField(
        label="Sequence length",
        required=False,
    )


class MolecularWeightForm(forms.Form):
    select = forms.BooleanField(
        label="Molecular weight",
        required=False,
    )


class GravyForm(forms.Form):
    select = forms.BooleanField(
        label="GRAVY",
        required=False,
    )


class IsoelectricPointForm(forms.Form):
    select = forms.BooleanField(
        label="Isoelectric point",
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


class AromaticityForm(forms.Form):
    select = forms.BooleanField(
        label="Aromaticity",
        required=False,
    )


class AaDistributionForm(forms.Form):
    select = forms.BooleanField(
        label="📈 Frequency of amino acids",
        required=False,
    )
    order_by = forms.ChoiceField(
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
    show_all = forms.ChoiceField(
        label="Show all amino acids",
        choices=((True, "Yes"), (False, "No")),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class HydropathyPlotForm(forms.Form):
    select = forms.BooleanField(
        label="📈 Hydropathy profile",
        required=False,
    )


class ClassificationForm(forms.Form):
    select = forms.BooleanField(
        label="📈 Classification",
        required=False,
    )
    classify_by = forms.ChoiceField(
        label="Class",
        choices=(
            ("chemical", "Chemical"),
            ("charge", "Charge"),
        ),
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class ScatterFeaturesForm(forms.Form):
    select = forms.BooleanField(
        label="📈 Compare features across groups",
        required=False,
    )
    feature_a = forms.ChoiceField(
        label="Feature on x-axis",
        choices=feature_choices,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    feature_b = forms.ChoiceField(
        label="Feature on y-axis",
        choices=feature_choices,
        initial=("Sequence length", "Sequence length"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    groups = forms.CharField(
        label="Group prefixes, seperated by semicolons",
        max_length=100,
        required=False,
        initial="AD; CTR",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    intensity_threshold = forms.FloatField(
        label="Intensity threshold",
        required=False,
        initial=0.01,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )


class BoxFeatureForm(forms.Form):
    select = forms.BooleanField(
        label="📈 Compare a feature across groups",
        required=False,
    )
    feature = forms.ChoiceField(
        label="Feature",
        choices=feature_choices,
        initial=("GRAVY", "GRAVY"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    groups = forms.CharField(
        label="Group prefixes, seperated by semicolons",
        max_length=100,
        required=False,
        initial="AD; CTR",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    intensity_threshold = forms.FloatField(
        label="Intensity threshold",
        required=False,
        initial=0.01,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )


FORM_TO_FUNCTION = {
    ThreeLetterCodeForm: "three_letter_code",
    MolecularFormulaForm: "seq_length",
    MolecularWeightForm: "molecular_weight",
    GravyForm: "gravy",
    IsoelectricPointForm: "isoelectric_point",
    AromaticityForm: "aromaticity",
}
PLOT_FORM_CLASSES = [
    AaDistributionForm,
    HydropathyPlotForm,
    ClassificationForm,
    ScatterFeaturesForm,
    BoxFeatureForm,
]
