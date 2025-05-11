from src.peptidefeatures.constants import AA_WEIGHTS, WATER
from src.peptidefeatures.features.sequence import aa_number


def molecular_weight(seq: str) -> int:
    """
    Computes the average molecular weight of a given sequence in Da.
    """
    num = aa_number(seq)
    weight = sum(AA_WEIGHTS[aa] for aa in seq) - (num - 1) * WATER
    return round(weight, 3)
