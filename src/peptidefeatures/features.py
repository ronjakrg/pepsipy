from peptidefeatures.constants import AA_LETTERS, AA_THREE_LETTERS, AA_WEIGHTS, WATER


def aa_number(seq: str) -> int:
    """
    Computes the number of amino acids in a given sequence.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
    """
    invalid = set(seq) - AA_LETTERS
    if invalid:
        raise ValueError(f"Invalid amino acid symbol: {', '.join(sorted(invalid))}")
    return len(seq)


def aa_frequency(seq: str) -> dict[str, int]:
    """
    Computes the frequency of each amino acid in a given sequence.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
    """
    try:
        freq = {val: 0 for val in AA_LETTERS}
        for aa in seq:
            freq[aa] += 1
        return freq
    except KeyError as e:
        raise ValueError(f"Invalid amino acid symbol: '{e.args[0]}'") from None


def molecular_weight(seq: str) -> float:
    """
    Computes the average molecular weight of a given sequence in Da.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
    """
    num = aa_number(seq)
    try:
        weight = sum(AA_WEIGHTS[aa] for aa in seq) - (num - 1) * WATER
        return round(weight, 3)
    except KeyError as e:
        raise ValueError(f"Invalid amino acid symbol: '{e.args[0]}'") from None


def three_letter_code(seq: str) -> str:
    """
    Converts a sequence of amino acids into its representation in three letter code.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
    """
    try:
        return "".join(AA_THREE_LETTERS[aa] for aa in seq)
    except KeyError as e:
        raise ValueError(f"Invalid amino acid symbol: '{e.args[0]}'") from None
