from django.shortcuts import render
import plotly

from .forms import FeatureForm
from peptidefeatures.features import molecular_formula
from peptidefeatures.plots.other import aa_distribution


def overview(request):
    peptide_of_interest = ""
    peptide_results = {}
    peptide_plots = []
    if request.method == "POST":
        form = FeatureForm(request.POST)
        if form.is_valid():
            peptide_of_interest = form.cleaned_data["peptide_of_interest"]
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
        form = FeatureForm()

    return render(
        request,
        "overview.html",
        {
            "form": form,
            "peptide_of_interest": peptide_of_interest,
            "peptide_results": peptide_results,
            "peptide_plots": peptide_plots,
        },
    )
