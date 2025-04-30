from src.utils import AA

def aa_number(seq: str) -> int:
    """
    Computes the number of amino acids in a given sequence.
    """
    return len(seq)

def aa_frequency(seq: str) -> dict[str, int]:
    """
    Computes the frequency of each amino acid in a given sequence.
    """
    freq = {val: 0 for val in AA}
    for aa in seq:
        freq[aa] += 1
    return freq