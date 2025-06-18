import pandas as pd
from pathlib import Path
from django.conf import settings

from .forms import FORM_TO_FUNCTION

def load_data(name: str) -> pd.DataFrame:
    data_path = (
        Path(settings.PROJECT_DIR) / "data" / name
    )
    return pd.read_csv(data_path)


def get_params(forms: list) -> dict:
    result = {}
    for form in forms:
        if form.is_valid():
            if form.cleaned_data["select"]:
                params = {
                    key: val
                    for key, val in form.cleaned_data.items()
                    if key != "select"
                }
                params.update({FORM_TO_FUNCTION[type(form)]: True})
                result.update(params)
    return result

def get_features_for_seq(data: pd.DataFrame, seq: str) -> dict:
    matched = data[data["Sequence"] == seq]
    matched = matched.drop(
        columns=[
            "Sample",
            "Protein ID",
            "Sequence",
            "Intensity",
            "PEP",
        ],
        errors="ignore",
    )
    if not matched.empty:
        return matched.iloc[0].to_dict()
    else:
        return {}