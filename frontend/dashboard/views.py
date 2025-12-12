import zipfile
import pandas as pd
from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from pathlib import Path
import yaml

from frontend.project import settings
from pepsipy import Calculator

from .forms import ConfigForm, FORM_TO_FEATURE_FUNCTION, FORM_TO_PLOT_FUNCTION
from .utils import (
    load_data,
    get_params,
    get_match_for_seq,
    clear_tmp,
    make_forms,
    get_paired_list,
    load_user_color_scheme,
)
from .constants import USER_COLORS_PATH, COLOR_SCHEME_1


def index(request):
    # Setup
    seq = ""
    computed_features = pd.DataFrame()
    computed_peptide_features = {}
    paired_peptide_features = list()
    num_matches = 0
    html_peptide_plots = []
    html_data_plots = []
    feature_forms = []
    plot_forms = []
    results_ready = False
    # For HTML color input fields
    context_user_colors_dict = {}
    context_user_colors_list = []
    # For using colors in plots
    selected_colors = None

    calc = Calculator()
    config_form = ConfigForm(request.POST or None)

    if config_form.is_valid():
        metadata = load_data(config_form.cleaned_data["metadata_name"])
        metadata_choices = [(col, col) for col in metadata.columns]
        seq = config_form.cleaned_data["seq"]
        calc.setup(seq=seq)
        feature_forms = make_forms(request.POST, FORM_TO_FEATURE_FUNCTION.keys())
        plot_forms = make_forms(
            request.POST, FORM_TO_PLOT_FUNCTION.keys(), metadata_choices
        )

    if USER_COLORS_PATH.exists():
        context_user_colors_dict, context_user_colors_list, selected_colors = (
            load_user_color_scheme(USER_COLORS_PATH)
        )
    else:
        context_user_colors_list = COLOR_SCHEME_1

    if request.method == "POST" and "calculate" in request.POST:
        # Clear tmp directory
        clear_tmp()

        # Get data
        calc.setup(
            dataset=load_data(config_form.cleaned_data["data_name"]), metadata=metadata
        )

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
            paired_peptide_features = get_paired_list(computed_peptide_features)

        # Generate plots
        calc.set_plot_params(**get_params(plot_forms, FORM_TO_PLOT_FUNCTION))
        peptide_plots, data_plots = calc.get_plots(
            as_tuple=True, colors=selected_colors
        )
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
        results_ready = True

    context = {
        "config_form": config_form,
        "feature_forms": feature_forms,
        "plot_forms": plot_forms,
        "selection_forms": [feature_forms, plot_forms],
        "results_ready": results_ready,
        "seq": seq,
        "paired_peptide_features": paired_peptide_features,
        "num_matches": num_matches,
        "peptide_plots": html_peptide_plots,
        "data_plots": html_data_plots,
        "context_user_colors_dict": context_user_colors_dict,
        "context_user_colors_list": context_user_colors_list,
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


# Called via AJAX from color modal
def save_colors_from_modal(request):
    if request.method == "POST":
        colors = {k: v for k, v in request.POST.items() if k != "csrfmiddlewaretoken"}

        USER_COLORS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(USER_COLORS_PATH, "w") as f:
            yaml.dump(colors, f)
        try:
            request.session["saved_colors"] = colors
        except Exception:
            pass
        return JsonResponse({"status": "ok", "colors": colors})
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)
