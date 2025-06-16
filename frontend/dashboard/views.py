from django.shortcuts import render

from .forms import GeneralForm, PeptideForm
from peptidefeatures.features import molecular_formula
from peptidefeatures.plots.other import aa_distribution


def overview(request):
    peptide_of_interest = ""
    peptide_results = {}
    peptide_plots = []
    if request.method == "POST":
        general_form = GeneralForm(request.POST)
        peptide_form = PeptideForm(request.POST)
        if general_form.is_valid() and peptide_form.is_valid():
            peptide_of_interest = general_form.cleaned_data["peptide_of_interest"]
            formula = molecular_formula(peptide_of_interest)
            peptide_results = {
                "Three letter code": "",
                "Molecular formular": formula,
                "Sequence length": "",
                "Molecular weight": "",
                "GRAVY": "",
                "Isoelectric point": "",
                "Aromaticity": "",
            }
            plot = aa_distribution(peptide_of_interest, "classes chemical", True)
            peptide_plots.append(plot.to_html())
    else:
        general_form = GeneralForm()
        peptide_form = PeptideForm()

    return render(
        request,
        "overview.html",
        {
            "general_form": general_form,
            "peptide_form": peptide_form,
            "dataset_form": "",

            "peptide_of_interest": peptide_of_interest,
            "peptide_results": peptide_results,
            "peptide_plots": peptide_plots,

            "dataset_plots": "",
        },
    )
