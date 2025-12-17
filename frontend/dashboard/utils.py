from collections.abc import Iterable
from django.http import QueryDict
from io import StringIO
import pandas as pd
from pathlib import Path
import os
from typing import Any
from django.conf import settings
import yaml
from .forms import (
    CompareFeatureForm,
    CompareFeaturesForm,
    ChargeForm,
    ChargeDensityForm,
    RaincloudForm,
    MannWhitneyForm,
)
from pepsipy.features import FEATURES
from .constants import COLOR_SCHEME_1, COLOR_SCHEME_2


from django.core.cache import cache
import uuid

CACHE_TIMEOUT = 60 * 60  # 1 hour


def yaml_to_string(data: Any) -> str:
    """
    Serialize a Python object (dict, list, etc.) to a YAML-formatted string.
    """
    return yaml.safe_dump(data, sort_keys=False)


def string_to_yaml(yaml_string: str) -> Any:
    """
    Parse a YAML-formatted string into a Python object (dict, list, etc.).
    """
    return yaml.safe_load(yaml_string)


def session_cache_add(request, namespace: str, value, timeout=CACHE_TIMEOUT):
    """
    Add an object to a session-scoped cache namespace.
    """
    if not request.session.session_key:
        request.session.save()

    cache_key = f"{request.session.session_key}:{namespace}:{uuid.uuid4()}"
    cache.set(cache_key, value, timeout=timeout)

    keys = request.session.get(namespace, [])
    keys.append(cache_key)
    request.session[namespace] = keys


def session_cache_get_all(request, namespace: str | None = None):
    """
    Retrieve all cached objects for a namespace.
    """
    if namespace:
        keys = request.session.get(namespace, [])
        return [cache.get(k) for k in keys if cache.get(k) is not None]

    all_values = {}
    for session_key, value in request.session.items():
        if isinstance(value, Iterable) and not isinstance(value, str):
            cached_list = [cache.get(k) for k in value if cache.get(k) is not None]
            if cached_list:
                all_values[session_key] = cached_list
    return all_values


def session_cache_clear(request, namespace: str):
    """
    Remove all cached objects for a namespace.
    """
    keys = request.session.pop(namespace, [])
    for k in keys:
        cache.delete(k)


def df_to_csv_string(df: pd.DataFrame) -> str:
    """
    Serialize DataFrame to CSV string for session storage.
    """
    buf = StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue()


def uploaded_csv_to_string(uploaded_file) -> str:
    """
    Read an uploaded CSV file and return its content as a string
    for session storage.
    """
    uploaded_file.seek(0)
    return uploaded_file.read().decode("utf-8")


def csv_string_to_df(csv_string: str) -> pd.DataFrame:
    """
    Reconstruct a DataFrame from a CSV string stored in session.
    """
    return pd.read_csv(StringIO(csv_string))


def load_uploaded_csv(uploaded_file) -> pd.DataFrame:
    """
    Load a CSV uploaded via Django FileField into a DataFrame.
    The file is never written to disk.
    """
    try:
        uploaded_file.seek(0)
        return pd.read_csv(uploaded_file)
    except Exception as e:
        raise ValueError(f"Could not read uploaded CSV: {e}")


def load_data(name: str) -> pd.DataFrame:
    """
    Loads a CSV file from the project's data folder and
    returns its content as a pandas DataFrame.
    """
    data_path = Path(settings.PROJECT_DIR) / "data" / name
    try:
        return pd.read_csv(data_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {name} could not be found at {data_path}.")


def get_params(forms: list, mapping: dict) -> dict:
    """
    Extracts parameters from a list of forms.
    If a feature was selected, a parameter mapping the
    function name to True is added.
    """
    result = {}
    for form in forms:
        if form.is_valid():
            if form.cleaned_data["selected"]:
                # Get params from form
                params = {
                    key: eval_input(val)
                    for key, val in form.cleaned_data.items()
                    if key != "selected"
                }
                # Add function name as param for (un)selecting
                params.update({mapping[type(form)]: True})
                result.update(params)
            else:
                result.update({mapping[type(form)]: False})
    return result


def get_match_for_seq(data: pd.DataFrame, seq: str) -> dict:
    """
    Matches the given sequence to a row of computed sequences and removes all columns that do not correspond to a feature.
    Returns the number of matches and the found features as dict.
    """
    ALLOWED = {f.label for f in FEATURES.values()} | {"Sequence", "Protein ID"}
    matched = data[data["Sequence"] == seq]
    num_matches = len(matched)
    matched = matched.loc[:, matched.columns.isin(ALLOWED)]
    if not matched.empty:
        return (num_matches, matched.iloc[0].to_dict())
    else:
        return (0, {})


def clear_tmp():
    """
    Deletes all files from temporary directory /tmp, except the .gitkeep file.
    """
    path = settings.TMP_DIR
    if os.path.exists(path):
        for item in path.iterdir():
            if item.name == "plots":
                continue
            else:
                item.unlink()
        if os.path.exists(path / "plots"):
            for item in (path / "plots").iterdir():
                if item.name == ".gitkeep":
                    continue
                item.unlink()


def make_forms(post_data: QueryDict, classes: list, metadata_choices: dict = None):
    """
    Returns a list of feature or plot forms based on the provided classes and POST data.
    Includes metadata options and other initial values at run time.
        post_data: POST data of request
        classes: List of feature or plot form classes
        metadata_choices: Dict containing dropdown options from loaded metadata file
    """
    forms = []
    for cls in classes:
        prefix = cls.__name__
        kwargs = {"prefix": prefix}
        is_bound = any(key.startswith(f"{prefix}-") for key in post_data.keys())
        # Include initial values at run time
        if cls in (
            CompareFeatureForm,
            CompareFeaturesForm,
            RaincloudForm,
            MannWhitneyForm,
        ):
            kwargs["metadata_choices"] = metadata_choices
            group_option = ("Group", "Group")
            if group_option in metadata_choices:
                kwargs["initial"] = {
                    "compare_feature_group_by": group_option,
                    "compare_features_group_by": group_option,
                    "raincloud_group_by": group_option,
                    "mann_whitney_group_by": group_option,
                }
        if not is_bound:
            if cls == ChargeForm:
                kwargs["initial"] = {"charge_at_ph_level": 7.0}
            if cls == ChargeDensityForm:
                kwargs["initial"] = {"charge_density_level": 7.0}
        else:
            kwargs["data"] = post_data
        forms.append(cls(**kwargs))
    return forms


def eval_input(input: Any) -> bool | Any:
    """
    Evaluation that converts str 'True' to bool True.
        input: Input of any type
    """
    if isinstance(input, str):
        if input.lower() == "true":
            return True
        elif input.lower() == "false":
            return False
    return input


def get_paired_list(dict: dict) -> list:
    """
    Creates a list of paired items from a dictionary.
        dict: Dictionary of items
    """
    items = list(dict.items())
    return [items[i : i + 2] for i in range(0, len(items), 2)]


def update_tuple_in_paired_list(
    paired_list: list,
    target_label: str,
    value: Any,
) -> list:
    """
    Finds the target label in paired list and updates its value.
        paired_list: Paired list of tuples
        target_label: Label of tuple that gets updated
        value: New value
    """
    for i, pair in enumerate(paired_list):
        for j, (label, _) in enumerate(pair):
            if label == target_label:
                paired_list[i][j] = (label, value)
    return paired_list


def load_user_color_scheme(request):
    """
    Loads the colors.yaml config and returns
        context_dict: Contains all entries as dict
        context_list: Contains a list of all custom colors
        selected_colors: Contains a list of selected colors, either from a scheme or custom colors
    """
    context_dict = request.session.get("user_colors", {})
    context_list = [context_dict.get(f"customColor{i}", "#000000") for i in range(1, 8)]
    scheme = context_dict.get("colorScheme")

    if scheme == "custom":
        selected_colors = context_list
    elif scheme == "1":
        selected_colors = COLOR_SCHEME_1
    elif scheme == "2":
        selected_colors = COLOR_SCHEME_2
    else:
        selected_colors = None

    return context_dict, context_list, selected_colors

    # with open(path, "r") as f:
    #     context_dict = yaml.safe_load(f)
    # context_list = [context_dict.get(f"customColor{i}", "#000000") for i in range(1, 8)]
    # scheme = context_dict.get("colorScheme")
    # if scheme == "custom":
    #     selected_colors = context_list
    # elif scheme == "1":
    #     selected_colors = COLOR_SCHEME_1
    # elif scheme == "2":
    #     selected_colors = COLOR_SCHEME_2
    # else:
    #     selected_colors = None

    # return context_dict, context_list, selected_colors
