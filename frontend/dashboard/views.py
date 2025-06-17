from django.shortcuts import render
from django.conf import settings
import pandas as pd
from pathlib import Path

from .forms import GeneralForm, PeptideForm
from peptidefeatures.features import compute_features, FeatureOptions
from peptidefeatures.plots.other import (
    aa_distribution,
    hydropathy_plot,
    classification_plot,
)


def overview(request):
    seq = ""
    peptide_results = {}
    peptide_plots = []
    if request.method == "POST":
        general_form = GeneralForm(request.POST)  # For general information
        peptide_form = PeptideForm(request.POST)  # Relevant for peptide features
        if general_form.is_valid() and peptide_form.is_valid():
            # Get data
            data_path = (
                Path(settings.PROJECT_DIR)
                / "data"
                / general_form.cleaned_data["data_name"]
            )
            df = pd.read_csv(data_path)
            seq = general_form.cleaned_data["peptide_of_interest"]
            # Compute feature data
            params = peptide_form.cleaned_data
            options = FeatureOptions(**params)
            results = compute_features(df=df, options=options)
            # Filter data for peptide of interest
            matched = results[results["Sequence"] == seq]
            # TODO Try not to hardcode this
            matched = matched.drop(
                columns=[
                    "Sample",
                    "Protein ID",
                    "Sequence",
                    "Intensity",
                    "PEP",
                    "Frequency of AA",
                    "Classification",
                ],
                errors="ignore",
            )
            if not matched.empty:
                peptide_results = matched.iloc[0].to_dict()
            else:
                peptide_results = {}
            # Generate plots
            if params["aa_distribution"]:
                plot = aa_distribution(
                    seq=seq,
                    order_by=params["aa_distribution_order"],
                    show_all=(params["aa_distribution_showall"] == "True"),
                )
                peptide_plots.append(plot.to_html())
            if params["hydropathy_profile"]:
                plot = hydropathy_plot(seq)
                peptide_plots.append(plot.to_html())
            if params["classification"]:
                plot = classification_plot(
                    seq=seq,
                    classify_by=params["classification_class"],
                )
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
            "peptide_of_interest": seq,
            "peptide_results": peptide_results,
            "peptide_plots": peptide_plots,
            "dataset_plots": "",
        },
    )
