from peptidefeatures.constants import AA_LETTERS


def sanitize_sequence(seq: str) -> str:
    seq = seq.upper()
    return "".join(res for res in seq if res in AA_LETTERS)
