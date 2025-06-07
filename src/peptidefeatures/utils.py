import pandas as pd

from peptidefeatures.constants import AA_LETTERS


def sanitize_seq(seq: str) -> str:
    """
    Converts all letters to upper case and removes any character that
    does not represent an amino acid according to IUPAC-IUB standard.
    """
    seq = seq.upper()
    return "".join(res for res in seq if res in AA_LETTERS)


def get_group(name: str, groups: list) -> str:
    """
    Returns the group that is found in the prefix of the sample name.
    If no group was found, "None" will be returned.
    """
    return next((g for g in groups if name.startswith(g)), "None")


def get_seq_column_name(df: pd.DataFrame) -> str:
    """
    Finds the first column of a dataframe that contains the substring "sequence".
    """
    seq_col_name = next((col for col in df.columns if "sequence" in col.lower()), None)
    if seq_col_name == None:
        raise ValueError(
            f"None of the containing columns are recognized as sequence column: {df.columns}"
        )
    return seq_col_name


def get_distinct_seq(df: pd.DataFrame) -> pd.DataFrame:
    """
    Finds the first column containing "sequence" in its header and
    returns a dataframe containing only unique sequences.
    """
    seq_col_name = get_seq_column_name(df)
    return df[[seq_col_name]].drop_duplicates(keep="first")
