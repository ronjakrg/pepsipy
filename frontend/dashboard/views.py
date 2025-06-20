from django.shortcuts import render
import pandas as pd
import plotly.io as pio

from peptidefeatures.features import compute_features, FeatureParams
from peptidefeatures.plots import generate_plots, PlotsParams

from .forms import *
from .utils import load_data, get_params, get_features_for_seq


def overview(request):
    seq = ""
    feature_params = {}
    computed_features = pd.DataFrame()
    computed_peptide_features = {}

    plot_params = []
    html_plots = []

    # Get form data with prefixes
    feature_forms = []
    plot_forms = []
    for cls in FORM_TO_FEATURE_FUNCTION.keys():
        form = cls(
            data=request.POST or None,
            prefix=cls.__name__,
        )
        feature_forms.append(form)
    for cls in FORM_TO_PLOT_FUNCTION:
        form = cls(data=request.POST or None)
        plot_forms.append(form)
    if request.method == "POST":
        # Get data
        gen_form = GeneralForm(request.POST)
        if gen_form.is_valid():
            data = load_data(gen_form.cleaned_data["data_name"])
            seq = gen_form.cleaned_data["seq"]

        # Compute features
        feature_params = get_params(feature_forms, FORM_TO_FEATURE_FUNCTION)
        computed_features = compute_features(
            df=data, params=FeatureParams(**feature_params)
        )

        # Filter data for peptide of interest
        computed_peptide_features = get_features_for_seq(computed_features, seq)

        # Generate plots
        plot_params = get_params(plot_forms, FORM_TO_PLOT_FUNCTION)
        plots = generate_plots(
            df=computed_features, seq=seq, params=PlotsParams(**plot_params)
        )
        for plot in plots:
            # plot.update_layout(width=600, height=450)
            html_plots.append(plot.to_html(config={"responsive": True}))
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
            "plots": html_plots,
        },
    )
