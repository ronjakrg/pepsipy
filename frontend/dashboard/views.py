from django.shortcuts import render

from .forms import FeatureForm

from peptidefeatures.features import molecular_formula

def overview(request):
    results = {}
    if request.method == "POST":
        form = FeatureForm(request.POST)
        if form.is_valid():
            peptide_of_interest = form.cleaned_data["peptide_of_interest"]
            formula = molecular_formula(peptide_of_interest)
            results = {
                "peptide_of_interest": peptide_of_interest,
                "formula": formula,
            }
    else:
        form = FeatureForm()
    return render(request, "overview.html", {
        "form": form,
        "results": results,
    })
