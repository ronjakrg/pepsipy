from peptidefeatures.constants import AA_LETTERS


def sanitize_sequence(seq: str) -> str:
    """
    Converts all letters to upper case and removes any character that
    does not represent an amino acid according to IUPAC-IUB standard.
    """
    seq = seq.upper()
    return "".join(res for res in seq if res in AA_LETTERS)


def get_group(name: str, groups: list) -> str:
    """
    Returns the group that is found in the prefix of the sample name.
    If no group was found, "UNKNOWN" will be returned.
    """
    return next((g for g in groups if name.startswith(g)), "UNKNOWN")
