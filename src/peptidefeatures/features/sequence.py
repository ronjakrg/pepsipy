from src.peptidefeatures.constants import AA_LETTERS


def aa_number(seq: str) -> int:
    """
    Computes the number of amino acids in a given sequence.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
    """
    return len(seq)


def aa_frequency(seq: str) -> dict[str, int]:
    """
    Computes the frequency of each amino acid in a given sequence.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
    """
    freq = {val: 0 for val in AA_LETTERS}
    for aa in seq:
        freq[aa] += 1
    return freq
