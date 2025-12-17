import io
import zipfile
import pandas as pd
from django.shortcuts import render
from django.http import FileResponse, JsonResponse, HttpResponse
from pathlib import Path
import yaml

from frontend.project import settings
from pepsipy import Calculator

from .forms import ConfigForm, FORM_TO_FEATURE_FUNCTION, FORM_TO_PLOT_FUNCTION
from .utils import (
    session_cache_clear,
    session_cache_get_all,
    session_cache_add,
    uploaded_csv_to_string,
    df_to_csv_string,
    csv_string_to_df,
    load_uploaded_csv,
    load_data,
    get_params,
    get_match_for_seq,
    clear_tmp,
    make_forms,
    get_paired_list,
    update_tuple_in_paired_list,
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
    uploaded_data_name = ""
    uploaded_metadata_name = ""

    calc = Calculator()
    config_form = ConfigForm(request.POST or None, request.FILES or None)

    if config_form.is_valid():

        # Store uploaded CSVs in session (only once per load)
        if "load" in request.POST:
            request.session["uploaded_data_name"] = config_form.cleaned_data[
                "data_file"
            ].name
            request.session["uploaded_metadata_name"] = config_form.cleaned_data[
                "metadata_file"
            ].name

            session_cache_add(
                request,
                "data_csv",
                uploaded_csv_to_string(config_form.cleaned_data["data_file"]),
            )
            session_cache_add(
                request,
                "metadata_csv",
                uploaded_csv_to_string(config_form.cleaned_data["metadata_file"]),
            )
            # request.session["metadata_csv"] = uploaded_csv_to_string(
            #     config_form.cleaned_data["metadata_file"]
            # )

            request.session["seq"] = config_form.cleaned_data["seq"]
            request.session.modified = True

        # Load metadata from session
        metadata = csv_string_to_df(session_cache_get_all(request, "metadata_csv")[0])
        # metadata = csv_string_to_df(request.session["metadata_csv"])
        metadata_choices = [(col, col) for col in metadata.columns]

        feature_forms = make_forms(request.POST, FORM_TO_FEATURE_FUNCTION.keys())
        plot_forms = make_forms(
            request.POST, FORM_TO_PLOT_FUNCTION.keys(), metadata_choices
        )

    if request.session.get("user_colors"):
        context_user_colors_dict, context_user_colors_list, selected_colors = (
            load_user_color_scheme(request)
        )
    else:
        context_user_colors_list = COLOR_SCHEME_1

    if request.method == "POST" and "calculate" in request.POST:
        # Get data
        # dataset = csv_string_to_df(request.session["data_csv"])
        dataset = csv_string_to_df(session_cache_get_all(request, "data_csv")[0])
        metadata = csv_string_to_df(session_cache_get_all(request, "metadata_csv")[0])
        metadata_choices = [(col, col) for col in metadata.columns]
        seq = request.session.get("seq", "")

        feature_forms = make_forms(request.POST, FORM_TO_FEATURE_FUNCTION.keys())
        plot_forms = make_forms(
            request.POST, FORM_TO_PLOT_FUNCTION.keys(), metadata_choices
        )

        # # Clear tmp directory
        # clear_tmp()
        # print(dataset)
        # print(metadata)

        calc.setup(dataset=dataset, metadata=metadata)
        calc.setup(seq=seq)

        # Compute features
        calc.set_feature_params(**get_params(feature_forms, FORM_TO_FEATURE_FUNCTION))
        computed_features = calc.get_features()

        session_cache_add(request, "features", df_to_csv_string(computed_features))
        # request.session["features_csv"] = df_to_csv_string(computed_features)

        if calc.seq != "":
            # Filter data for peptide of interest
            num_matches, computed_peptide_features = get_match_for_seq(
                computed_features, calc.seq
            )
            # If peptide was not found in dataset
            if num_matches == 0:
                res = calc.get_peptide_features()

                session_cache_add(request, "computed_features", df_to_csv_string(res))

                # request.session["peptide_features_csv"] = df_to_csv_string(res)
                computed_peptide_features = res.iloc[0].to_dict()

            paired_peptide_features = get_paired_list(computed_peptide_features)
            associated_protein_ids = computed_features.loc[
                computed_features["Sequence"] == seq, "Protein ID"
            ].unique()
            paired_peptide_features = update_tuple_in_paired_list(
                paired_peptide_features, "Protein ID", ", ".join(associated_protein_ids)
            )

        # Generate plots
        # print(get_params(plot_forms, FORM_TO_PLOT_FUNCTION))
        calc.set_plot_params(**get_params(plot_forms, FORM_TO_PLOT_FUNCTION))
        peptide_plots, data_plots = calc.get_plots(
            as_tuple=True, colors=selected_colors
        )

        for i, plot in enumerate(peptide_plots + data_plots, start=1):
            img_bytes = io.BytesIO()
            plot.write_image(img_bytes, format="png", scale=3)
            img_bytes.seek(0)

            session_cache_add(request, f"""plot_{i}""", img_bytes.getvalue())

            if i <= len(peptide_plots):
                html_peptide_plots.append(plot.to_html(config={"responsive": True}))
            else:
                # print(plot)
                html_data_plots.append(plot.to_html(config={"responsive": True}))

        # i = 1
        # for plot in peptide_plots:
        #     plot.write_image(
        #         settings.TMP_DIR / "plots" / f"plot_{i}.png", format="png", scale=3
        #     )
        #     html_peptide_plots.append(plot.to_html(config={"responsive": True}))
        #     i += 1
        # for plot in data_plots:
        #     plot.write_image(
        #         settings.TMP_DIR / "plots" / f"plot_{i}.png", format="png", scale=3
        #     )
        #     html_data_plots.append(plot.to_html(config={"responsive": True}))
        #     i += 1
        results_ready = True
        print("CALCULATION DONE")
        request.session.modified = True

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
        "uploaded_data_name": request.session.get("uploaded_data_name"),
        "uploaded_metadata_name": request.session.get("uploaded_metadata_name"),
    }
    return render(request, "index.html", context)


# def download_data(request):
#     filename = request.GET.get("filename")
#     return FileResponse(
#         open(settings.TMP_DIR / f"{filename}.csv", "rb"),
#         content_type="text/csv",
#         filename="features.csv",
#     )


def download_data(request):
    # csv_string = request.session.get("features_csv")
    csv_string = session_cache_get_all(request, "features")[0]
    if csv_string is None:
        return HttpResponse("No data available", status=404)

    response = HttpResponse(csv_string, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="features.csv"'
    return response


def download_plots(request):
    path = settings.TMP_DIR / "plots.zip"
    plot_keys = [
        key for key in session_cache_get_all(request) if key.startswith("plot_")
    ]

    # with zipfile.ZipFile(path, "w") as zipf:
    #     for file in Path(settings.TMP_DIR / "plots").glob("*"):
    #         zipf.write(file, arcname=file.name)
    # return FileResponse(
    #     open(path, "rb"), content_type="application/zip", filename="plots.zip"
    # )
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for key in plot_keys:
            plot_bytes = session_cache_get_all(request, key)[
                0
            ]  # returns list of values
            zipf.writestr(f"{key}.png", plot_bytes)

    zip_buffer.seek(0)
    return FileResponse(
        zip_buffer, content_type="application/zip", filename="plots.zip"
    )


# Called via AJAX from color modal
def save_colors_from_modal(request):
    if request.method == "POST":
        colors = {k: v for k, v in request.POST.items() if k != "csrfmiddlewaretoken"}
        request.session["user_colors"] = colors
        request.session.modified = True

        return JsonResponse({"status": "ok", "colors": colors})
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)


def privacy(request):
    return render(request, "privacy.html")


def imprint(request):
    return render(request, "imprint.html")
