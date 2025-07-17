import zipfile
import pandas as pd
from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from pathlib import Path

from frontend.project import settings
from pepsi.calculator import Calculator

from .forms import *  # TODO
from .utils import load_data, get_params, get_match_for_seq, clear_tmp, make_forms


def overview(request):
    # Setup
    computed_features = pd.DataFrame()
    computed_peptide_features = {}
    num_matches = 0
    html_peptide_plots = []
    html_data_plots = []
    feature_forms = []
    plot_forms = []
    selection_forms_bound = (
        True  # len(feature_forms) > 0 and feature_forms[0].is_valid()
    )

    calc = Calculator()
    config_form = ConfigForm(request.POST or None)

    if config_form.is_valid():
        metadata = load_data(config_form.cleaned_data["metadata_name"])
        metadata_choices = [(col, col) for col in metadata.columns]
        feature_forms = make_forms(request.POST, FORM_TO_FEATURE_FUNCTION.keys())
        plot_forms = make_forms(
            request.POST, FORM_TO_PLOT_FUNCTION.keys(), metadata_choices
        )

    elif request.method == "POST" and "calculate" in request.POST:
        # Clear tmp directory
        clear_tmp()

        # Get data
        if config_form.is_valid():
            calc.set_dataset(load_data(config_form.cleaned_data["data_name"]))
            calc.set_metadata(metadata)
            calc.set_seq(config_form.cleaned_data["seq"])

        # Compute features
        calc.set_feature_params(**get_params(feature_forms, FORM_TO_FEATURE_FUNCTION))
        computed_features = calc.get_features()
        computed_features.to_csv(settings.TMP_DIR / "features.csv", index=False)

        if calc.seq != "":
            # Filter data for peptide of interest
            num_matches, computed_peptide_features = get_match_for_seq(
                computed_features, calc.seq
            )
            # If peptide was not found in dataset
            if num_matches == 0:
                res = calc.get_peptide_features()
                res.to_csv(settings.TMP_DIR / "peptide_features.csv", index=False)
                computed_peptide_features = res.iloc[0].to_dict()

        # Generate plots
        calc.set_plot_params(**get_params(plot_forms, FORM_TO_PLOT_FUNCTION))
        peptide_plots, data_plots = calc.get_plots()
        i = 1
        for plot in peptide_plots:
            plot.write_image(
                settings.TMP_DIR / "plots" / f"plot_{i}.png", format="png", scale=3
            )
            html_peptide_plots.append(plot.to_html(config={"responsive": True}))
            i += 1
        for plot in data_plots:
            plot.write_image(
                settings.TMP_DIR / "plots" / f"plot_{i}.png", format="png", scale=3
            )
            html_data_plots.append(plot.to_html(config={"responsive": True}))
            i += 1
    else:
        config_form = ConfigForm()

    context = {
        "config_form": config_form,
        "seq": calc.seq,
        "feature_forms": feature_forms,
        "plot_forms": plot_forms,
        "selection_forms": [feature_forms, plot_forms],
        "selection_forms_bound": selection_forms_bound,
        "computed_features": computed_features,
        "computed_peptide_features": computed_peptide_features,
        "num_matches": num_matches,
        "peptide_plots": html_peptide_plots,
        "data_plots": html_data_plots,
    }
    return render(request, "index.html", context)


def download_data(request):
    filename = request.GET.get("filename")
    return FileResponse(
        open(settings.TMP_DIR / f"{filename}.csv", "rb"),
        content_type="text/csv",
        filename="features.csv",
    )


def download_plots(request):
    path = settings.TMP_DIR / "plots.zip"
    with zipfile.ZipFile(path, "w") as zipf:
        for file in Path(settings.TMP_DIR / "plots").glob("*"):
            zipf.write(file, arcname=file.name)
    return FileResponse(
        open(path, "rb"), content_type="application/zip", filename="plots.zip"
    )
