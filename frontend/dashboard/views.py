import zipfile
import pandas as pd
from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from pathlib import Path

from frontend.project import settings
from pepsi.calculator import Calculator

from .forms import *
from .utils import load_data, get_params, get_match_for_seq, clear_tmp


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
        # Clear tmp directory
        clear_tmp()

        # Get data
        gen_form = GeneralForm(request.POST)
        if gen_form.is_valid():
            calc.set_dataset(load_data(gen_form.cleaned_data["data_name"]))
            calc.set_seq(gen_form.cleaned_data["seq"])

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

def fill_aspects(request):
    if request.method == "POST":
        gen_form = GeneralForm(request.POST)
        if gen_form.is_valid():
            aspects = load_data(gen_form.cleaned_data["aspects_name"])
            aspects_list = list(aspects.columns)
            return JsonResponse({"aspects": aspects_list})
    return JsonResponse({"aspects": []})


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
