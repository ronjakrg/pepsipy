import pytest

from frontend.dashboard.forms import (
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


@pytest.mark.parametrize(
    "data",
    [
        {"data_name": "peptides.csv", "seq": "PEPTIDE"},
    ],
)
def test_forms_general(data):
    form = GeneralForm(data=data)
    assert form.is_valid()


# Testing forms that only contain checkboxes
@pytest.mark.parametrize(
    "FormClass",
    [
        ThreeLetterCodeForm,
        MolecularFormulaForm,
        SeqLengthForm,
        MolecularWeightForm,
        GravyForm,
        AromaticityForm,
        HydropathyProfileForm,
    ],
)
def test_forms_checkboxes(FormClass):
    form = FormClass(data={})
    assert form.is_valid()
    assert form.cleaned_data["select"] is False
    form = FormClass(data={"select": "on"})
    assert form.is_valid()
    assert form.cleaned_data["select"] is True


@pytest.mark.parametrize(
    "data",
    [
        {
            "select": "on",
            "isoelectric_point_option": "bjellqvist",
        }
    ],
)
def test_isoelectric_point_form(data):
    form = IsoelectricPointForm(data=data)
    assert form.is_valid()
    assert form.cleaned_data["select"] is True
    assert form.cleaned_data["isoelectric_point_option"] == "bjellqvist"


def test_utils():
    pass


def test_views():
    pass
