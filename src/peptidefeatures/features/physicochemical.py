from peptidefeatures.constants import AA_WEIGHTS, WATER
from peptidefeatures.features.sequence import aa_number


def molecular_weight(seq: str) -> float:
    """
    Computes the average molecular weight of a given sequence in Da.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
    """
    num = aa_number(seq)
    weight = sum(AA_WEIGHTS[aa] for aa in seq) - (num - 1) * WATER
    return round(weight, 3)
