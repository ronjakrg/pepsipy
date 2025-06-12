from functools import partial
import os
from pathlib import Path
import pickle
import string
import sys

from Bio.SeqUtils import IsoelectricPoint
import numpy as np
import pandas as pd

from peptidefeatures.constants import (
    AA_FORMULA,
    AA_LETTERS,
    AA_THREE_LETTER_CODE,
    AA_ONE_LETTER_CODE,
    AA_WEIGHTS,
    HYDROPATHY_INDICES,
    WATER,
)
from peptidefeatures.utils import sanitize_seq, get_distinct_seq, get_column_name


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes all selected features on a pd.DataFrame.
    The column containing the peptide sequence must contain the
    substring "sequence".
    """
    # TODO Accept parameters for choice of features and options
    seq_col_name = get_column_name(df, "sequence")
    sequences = get_distinct_seq(df)
    isoelectric_point_option = "bjellqvist"
    feature_to_func = {
        "Three Letter Code": three_letter_code,
        "Molecular formula": molecular_formula,
        "Molecular weight": molecular_weight,
        "Isoelectric point": partial(
            isoelectric_point, option=isoelectric_point_option
        ),
        "Sequence length": seq_length,
        "Frequency of AA": aa_frequency,
        "GRAVY": gravy,
        "Aromaticity": aromaticity,
    }
    for feature, func in feature_to_func.items():
        sequences[feature] = sequences[seq_col_name].apply(func)
    merged = pd.merge(
        df,
        sequences,
        on=seq_col_name,
        how="left",
    )
    return merged


def seq_length(seq: str) -> int:
    """
    Computes the length in a given sequence.
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
    num = seq_length(seq)
    weight = sum(AA_WEIGHTS[aa] for aa in seq) - (num - 1) * WATER
    return round(weight, 3)


def three_letter_code(seq: str) -> str:
    """
    Converts a sequence of amino acids into its representation in three letter code.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
    """
    try:
        return "".join(AA_THREE_LETTER_CODE[aa] for aa in seq)
    except KeyError as e:
        raise ValueError(f"Invalid amino acid symbol: '{e.args[0]}'") from None


def one_letter_code(codes: str) -> str:
    """
    Converts concatenated three-letter amino acid codes into their one-letter code representation.
    """
    separators = set(string.whitespace + string.punctuation)
    if any(ch in separators for ch in codes):
        raise ValueError(
            f"Invalid input: Separators between codes are not allowed."
        ) from None
    seq = []
    for i in range(0, len(codes), 3):
        code = codes[i : i + 3]
        try:
            seq.append(AA_ONE_LETTER_CODE[code])
        except KeyError as e:
            raise ValueError(f"Invalid three letter code: '{e.args[0]}'.") from None
    return "".join(seq)


def gravy(seq: str) -> float:
    """
    Computes the GRAVY (grand average of hydropathy) score of a given sequence.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
    """
    num = seq_length(seq)
    hydropathy_sum = sum(HYDROPATHY_INDICES[aa] for aa in seq)
    return round(hydropathy_sum / num, 3)


def molecular_formula(seq: str) -> str:
    """
    Computes the molecular formula of a given sequence.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
    """
    total_atoms = {}
    for aa in seq:
        for atom, count in AA_FORMULA[aa].items():
            total_atoms[atom] = total_atoms.get(atom, 0) + count

    num_bindings = seq_length(seq) - 1
    total_atoms["H"] -= 2 * num_bindings
    total_atoms["O"] -= num_bindings

    sorted_atoms = ["C", "H", "N", "O", "S"]
    formula_elems = [
        f"{atom}{total_atoms[atom]}" if total_atoms[atom] > 1 else atom
        for atom in sorted_atoms
        if atom in total_atoms
    ]
    return "".join(formula_elems)


def isoelectric_point(seq: str, option: str) -> float:
    """
    Computes the theoretical pI of a given sequence.
    Option "kozlowski" uses IPC 2.0 (Kozlowski, 2021) to predict the pI
    with the pretrained model IPC2.peptide.svr19.
    Option "bjellqvist" uses the biopython package (Bjellqvist, 1993).
    """
    clean_seq = sanitize_seq(seq)

    if option == "kozlowski":
        EXTERNAL_PATH = Path(__file__).resolve().parent / "external"
        ipc_path = EXTERNAL_PATH / "ipc-2.0.1"
        model_path = ipc_path / "models" / "IPC2_peptide_75_SVR_19.pickle"
        if os.path.exists(ipc_path):
            sys.path.append(str(ipc_path / "scripts"))
        else:
            raise RuntimeError("IPC 2.0 installation could not be found.")

        # Ignoring warning because this function is dynamically added at runtime
        from ipc2_lib.svr_functions import get_pI_features  # type: ignore

        X, _ = get_pI_features([[clean_seq, ""]])
        X = np.array(X)

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        return float(model.predict(X)[0])

    elif option == "bjellqvist":
        calc = IsoelectricPoint.IsoelectricPoint(clean_seq)
        return round(calc.pi(), 3)

    else:
        raise ValueError(f"Unknown option: {option}")


def aromaticity(seq: str) -> float:
    """
    Computes the aromaticity of a given sequence by calculating the relative
    frequency of amino acids F, Y, and W (Lobry and Gautier, 1994).
    """
    freq = aa_frequency(seq)
    seq_len = seq_length(seq)
    num_aromatic = freq["F"] + freq["Y"] + freq["W"]
    return round(num_aromatic / seq_len, 3)
