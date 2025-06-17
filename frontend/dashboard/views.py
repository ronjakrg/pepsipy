from django.shortcuts import render
from django.conf import settings
import pandas as pd
from pathlib import Path

from .forms import GeneralForm, PeptideForm, DatasetForm, feature_fields
from peptidefeatures.features import compute_features, FeatureOptions
from peptidefeatures.plots.other import (
    aa_distribution,
    hydropathy_plot,
    classification_plot,
)
from peptidefeatures.plots.compare import scatter_features, box_feature


def overview(request):
    """
    gen - General information
    pep - Information / features on a specific peptide sequence of interest
    data - Information / features on the whole dataset
    """
    seq = ""
    pep_results = {}
    pep_plots = []
    data_plots = []
    if request.method == "POST":
        gen_form = GeneralForm(request.POST)
        pep_form = PeptideForm(request.POST)
        data_form = DatasetForm(request.POST)
        if gen_form.is_valid() and pep_form.is_valid() and data_form.is_valid():
            # Get data
            data_path = (
                Path(settings.PROJECT_DIR) / "data" / gen_form.cleaned_data["data_name"]
            )
            df = pd.read_csv(data_path)
            seq = gen_form.cleaned_data["peptide_of_interest"]
            pep_params = pep_form.cleaned_data
            data_params = data_form.cleaned_data

            # Compute feature data
            options = FeatureOptions(**pep_params)
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
                pep_results = matched.iloc[0].to_dict()
            else:
                pep_results = {}

            # TODO Rethink plot function calls
            # Generate plots
            if pep_params["aa_distribution"]:
                plot = aa_distribution(
                    seq=seq,
                    order_by=pep_params["aa_distribution_order"],
                    show_all=(pep_params["aa_distribution_showall"] == "True"),
                )
                pep_plots.append(plot.to_html())
            if pep_params["hydropathy_profile"]:
                plot = hydropathy_plot(seq)
                pep_plots.append(plot.to_html())
            if pep_params["classification"]:
                plot = classification_plot(
                    seq=seq,
                    classify_by=pep_params["classification_class"],
                )
                pep_plots.append(plot.to_html())
            if data_params["scatter_features"]:
                plot = scatter_features(
                    df=results,
                    groups=[
                        grp.strip()
                        for grp in data_params["scatter_features_groups"].split(";")
                    ],
                    feature_a=data_params["scatter_features_a"],
                    feature_b=data_params["scatter_features_b"],
                    intensity_threshold=data_params["scatter_features_intensity"],
                )
                data_plots.append(plot.to_html())
            if data_params["box_feature"]:
                plot = box_feature(
                    df=results,
                    groups=[
                        grp.strip()
                        for grp in data_params["box_feature_groups"].split(";")
                    ],
                    feature=data_params["box_feature_a"],
                    intensity_threshold=data_params["box_feature_intensity"],
                )
                data_plots.append(plot.to_html())
    else:
        gen_form = GeneralForm()
        pep_form = PeptideForm()
        data_form = DatasetForm()

    fields = list(pep_form) + list(data_form)
    return render(
        request,
        "overview.html",
        {
            "gen_form": gen_form,
            "fields": fields,
            "seq": seq,
            "peptide_results": pep_results,
            "peptide_plots": pep_plots,
            "dataset_plots": data_plots,
            "feature_fields": feature_fields,
        },
    )
