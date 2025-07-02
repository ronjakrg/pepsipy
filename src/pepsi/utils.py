import pandas as pd

from pepsi.constants import (
    AA_LETTERS,
    CHEMICAL_CLASS_PER_AA,
    CHARGE_CLASS_PER_AA,
)


def sanitize_seq(seq: str) -> str:
    """
    Converts all letters to upper case and removes any character that
    does not represent an amino acid according to IUPAC-IUB standard.
    """
    seq = seq.upper()
    return "".join(res for res in seq if res in AA_LETTERS)


def find_group(name: str, groups: list) -> str:
    """
    Returns the group that is found in the prefix of the sample name.
    If no group was found, "None" will be returned.
    """
    if groups is None:
        return "None"
    return next((g for g in groups if name.startswith(g)), "None")


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
    Finds the first column containing "sequence" in its header and
    returns a DataFrame containing only unique sequences.
    """
    seq_col_name = get_column_name(df, "sequence")
    return df[[seq_col_name]].drop_duplicates(keep="first")
