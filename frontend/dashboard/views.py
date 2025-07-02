from django.shortcuts import render
import pandas as pd
import plotly.io as pio

from pepsi.calculator import Calculator

from .forms import *
from .utils import load_data, get_params, get_match_for_seq


def overview(request):
    calc = Calculator()
    computed_features = pd.DataFrame()
    computed_peptide_features = {}
    num_matches = 0
    html_peptide_plots = []
    html_data_plots = []

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
            calc.set_dataset(load_data(gen_form.cleaned_data["data_name"]))
            calc.set_seq(gen_form.cleaned_data["seq"])

        # Compute features
        calc.set_feature_params(**get_params(feature_forms, FORM_TO_FEATURE_FUNCTION))
        computed_features = calc.get_features()

        # Filter data for peptide of interest
        num_matches, computed_peptide_features = get_match_for_seq(
            computed_features, calc.seq
        )
        # If peptide was not found in dataset
        if num_matches == 0:
            computed_peptide_features = calc.get_peptide_features().iloc[0].to_dict()

        # Generate plots
        calc.set_plot_params(**get_params(plot_forms, FORM_TO_PLOT_FUNCTION))
        peptide_plots, data_plots = calc.get_plots()
        for plot in peptide_plots:
            html_peptide_plots.append(plot.to_html(config={"responsive": True}))
        for plot in data_plots:
            html_data_plots.append(plot.to_html(config={"responsive": True}))
    else:
        gen_form = GeneralForm()

    return render(
        request,
        "overview.html",
        {
            "gen_form": gen_form,
            "seq": calc.seq,
            "forms_list": [feature_forms, plot_forms],
            "feature_forms": feature_forms,
            "plot_forms": plot_forms,
            "computed_features": computed_features,
            "computed_peptide_features": computed_peptide_features,
            "num_matches": num_matches,
            "peptide_plots": html_peptide_plots,
            "data_plots": html_data_plots,
        },
    )
