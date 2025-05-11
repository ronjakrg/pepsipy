from peptidefeatures.constants import AA_LETTERS


def aa_number(seq: str) -> int:
    """
    Computes the number of amino acids in a given sequence.
    """
    num = 0
    for aa in seq:
        if aa in AA_LETTERS:
            num += 1
    return num


def aa_frequency(seq: str) -> dict[str, int]:
    """
    Computes the frequency of each amino acid in a given sequence.
    """
    freq = {val: 0 for val in AA_LETTERS}
    for aa in seq:
        freq[aa] += 1
    return freq
