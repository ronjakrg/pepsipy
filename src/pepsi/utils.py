import pandas as pd
from plotly.colors import sample_colorscale

from pepsi.constants import AA_LETTERS


def sanitize_seq(seq: str) -> str:
    """
    Converts all letters to upper case and removes any character that
    does not represent an amino acid according to IUPAC-IUB standard.
    """
    seq = seq.upper()
    return "".join(res for res in seq if res in AA_LETTERS)


def get_column_name(df: pd.DataFrame, keyword: str) -> str:
    """
    Finds the first column of a DataFrame that contains a given keyword.
    """
    col_name = next((col for col in df.columns if keyword.lower() in col.lower()), None)
    if col_name is None:
        raise ValueError(
            f"Keyword {keyword.lower()} could not be found in containing columns: {df.columns}."
        )
    return col_name


def get_distinct_seq(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a pandas DataFrame containing only unique sequences.
    """
    return df[["Sequence"]].drop_duplicates(keep="first")


def normalize_color(
    val: float, min: float, max: float, colorscale: str = "Plasma"
) -> float:
    """
    Normalizes a feature value to [0,1] and maps it to a color from a given Plotly colorscale.
        val: Feature value to normalize
        min: Minimum feature value
        max: Maximum feature value
        colorscale: Name of a Plotly colorscale (see https://plotly.com/python/builtin-colorscales/ for more information)
    """
    norm = (val - min) / (max - min)
    return sample_colorscale(colorscale, norm)[0]


def extract_related_kwargs(mapping: dict, params: dict) -> dict:
    """
    Extracts entries whose external key appears in a given mapping from a dictionary. The found entries are returned with their internal key and values with None are ignored.
        mapping: Dictionary which maps external keys to internal keys
        params: Dictionary containing external keys and values
    """
    kwargs = {}
    for external_key, internal_key in mapping.items():
        val = params.get(external_key)
        if val is not None:
            kwargs[internal_key] = val
    return kwargs
