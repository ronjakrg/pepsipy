import pytest

from .forms import (
    GeneralForm,
    ThreeLetterCodeForm,
    MolecularFormulaForm,
    SeqLengthForm,
    MolecularWeightForm,
    GravyForm,
    IsoelectricPointForm,
    AromaticityForm,
    AaDistributionForm,
    HydropathyProfileForm,
    ClassificationForm,
    CompareFeaturesForm,
    CompareFeatureForm,
    FORM_TO_FEATURE_FUNCTION,
    FORM_TO_PLOT_FUNCTION,
)

@pytest.mark.parametrize("data", [
    {"data_name": "peptides.csv", "seq": "PEPTIDE"},
])
def test_forms_general(data):
    form = GeneralForm(data=data)
    assert form.is_valid()

@pytest.mark.parametrize("FormClass", [
    ThreeLetterCodeForm,
    MolecularFormulaForm,
    SeqLengthForm,
    MolecularWeightForm,
    GravyForm,
    AromaticityForm,
    HydropathyProfileForm,
])
def test_forms_checkboxes(FormClass):
    form = FormClass(data={})
    assert form.is_valid()
    assert form.cleaned_data["select"] is False
    form = FormClass(data={"select": "on"})
    assert form.is_valid()
    assert form.cleaned_data["select"] is True

def test_utils():
    pass


def test_views():
    pass