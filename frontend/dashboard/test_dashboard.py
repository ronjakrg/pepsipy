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
    HydropathyProfileForm,
    AaDistributionForm,
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
    assert not form.cleaned_data["select"]
    form = FormClass(data={"select": "on"})
    assert form.is_valid()
    assert form.cleaned_data["select"]


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
    assert form.cleaned_data["select"]
    assert form.cleaned_data["isoelectric_point_option"] == "bjellqvist"


@pytest.mark.parametrize(
    "data",
    [
        {
            "select": "on",
            "aa_distribution_order_by": "frequency",
            "aa_distribution_show_all": True,
        }
    ],
)
def test_aa_distribution_form(data):
    form = AaDistributionForm(data=data)
    assert form.is_valid()
    assert form.cleaned_data["select"]
    assert form.cleaned_data["aa_distribution_order_by"] == "frequency"
    assert form.cleaned_data["aa_distribution_show_all"]


def test_utils():
    pass


def test_views():
    pass
