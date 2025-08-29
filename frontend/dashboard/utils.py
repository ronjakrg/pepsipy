from django.http import QueryDict
import pandas as pd
from pathlib import Path
import os
from typing import Any
from django.conf import settings
from .forms import (
    CompareFeatureForm,
    CompareFeaturesForm,
    ChargeForm,
    ChargeDensityForm,
    RaincloudForm,
    MannWhitneyForm,
)


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
    Matches the given sequence to a row of computed sequences.
    Returns the number of matches and the found features as dict.
    """
    matched = data[data["Sequence"] == seq]
    num_matches = len(matched)
    matched = matched.drop(
        columns=[
            "Sample",
            "Protein ID",
            "Intensity",
            "PEP",
        ],
        errors="ignore",
    )
    if not matched.empty:
        return (num_matches, matched.iloc[0].to_dict())
    else:
        return (0, {})


def clear_tmp():
    """
    Deletes all files from temporary directory /tmp.
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
