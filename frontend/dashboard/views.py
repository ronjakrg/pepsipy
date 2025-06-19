from django.shortcuts import render
from django.conf import settings
import pandas as pd
from pathlib import Path

from peptidefeatures.features import compute_features, FeatureParams
from peptidefeatures.plots import generate_plots

from .forms import *
from .utils import load_data, get_params, get_features_for_seq


def overview(request):
    seq = ""
    feature_params = {}
    computed_features = pd.DataFrame()
    computed_peptide_features = {}
    plot_forms = []
    plot_params = []
    plots = []

    # Get form data with prefixes
    feature_forms = []
    for cls in FORM_TO_FUNCTION.keys():
        form = cls(
            data=request.POST or None,
            prefix=cls.__name__,
        )
        feature_forms.append(form)

    if request.method == "POST":
        # Get data
        gen_form = GeneralForm(request.POST)
        if gen_form.is_valid():
            data = load_data(gen_form.cleaned_data["data_name"])
            seq = gen_form.cleaned_data["seq"]

        # Compute features
        feature_params = get_params(feature_forms)
        computed_features = compute_features(
            df=data, params=FeatureParams(**feature_params)
        )

        # Filter data for peptide of interest
        computed_peptide_features = get_features_for_seq(computed_features, seq)

        # TODO Generate plots
        # for cls in PLOT_FORM_CLASSES:
        #     form = cls(data=request.POST or None)
        #     plot_forms.append(form)
        # for form in plot_forms:
        #     if form.is_valid() and form.cleaned_data["select"]:
        #         params = {key: val for key, val in form.cleaned_data.items() if key != "select"}
        #         plot_params.append(params)
        # plots = generate_plots(df=computed_features, seq=seq)
    else:
        gen_form = GeneralForm()

    return render(
        request,
        "overview.html",
        {
            "gen_form": gen_form,
            "seq": seq,
            "forms_list": [feature_forms, plot_forms],
            "feature_forms": feature_forms,
            "plot_forms": plot_forms,
            "computed_features": computed_features,
            "computed_peptide_features": computed_peptide_features,
            "plots": plots,
        },
    )
