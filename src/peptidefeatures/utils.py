from peptidefeatures.constants import AA_LETTERS


def sanitize_sequence(seq: str) -> str:
    """
    Converts all letters to upper case and removes any character that
    does not represent an amino acid according to IUPAC-IUB standard.
    """
    seq = seq.upper()
    return "".join(res for res in seq if res in AA_LETTERS)
