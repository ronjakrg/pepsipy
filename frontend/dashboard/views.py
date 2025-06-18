from django.shortcuts import render
from django.conf import settings
import pandas as pd
from pathlib import Path

from .forms import *
from peptidefeatures.features import compute_features, FeatureOptions
from peptidefeatures.plots import generate_plots


def overview(request):
    seq = ""
    feature_params = {}
    computed_features = pd.DataFrame
    computed_peptide_features = {}
    plot_forms = []
    plot_params = []
    plots = []

    feature_forms = []
    for cls in FORM_TO_FUNCTION.keys():
        form = cls(
            data=request.POST,
            prefix=cls.__name__,
        )
        feature_forms.append(form)
    if request.method == "POST":
        # Get data
        gen_form = GeneralForm(request.POST)
        if gen_form.is_valid():
            data_path = (
                Path(settings.PROJECT_DIR) / "data" / gen_form.cleaned_data["data_name"]
            )
            data = pd.read_csv(data_path)
            seq = gen_form.cleaned_data["seq"]
        # Compute features
        for form in feature_forms:
            if form.is_valid():
                print("Form:", form.cleaned_data)
                if form.cleaned_data["select"]:
                    params = {
                        key: val
                        for key, val in form.cleaned_data.items()
                        if key != "select"
                    }
                    params.update({FORM_TO_FUNCTION[type(form)]: True})
                    feature_params.update(params)
        print("###", feature_params)
        computed_features = compute_features(
            df=data, params=FeatureOptions(**feature_params)
        )
        print(computed_features)
        # Filter data for peptide of interest
        matched = computed_features[computed_features["Sequence"] == seq]
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
            computed_peptide_features = matched.iloc[0].to_dict()
        else:
            computed_peptide_features = {}
        # Generate plots
        # for cls in PLOT_FORM_CLASSES:
        #     form = cls(data=request.POST or None)
        #     plot_forms.append(form)
        # for form in plot_forms:
        #     if form.is_valid() and form.cleaned_data["select"]:
        #         params = {key: val for key, val in form.cleaned_data.items() if key != "select"}
        #         plot_params.append(params)
        # plots = generate_plots(df=computed_features, seq=seq) # TODO Add params
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
