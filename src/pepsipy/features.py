from dataclasses import dataclass
from functools import partial
import os
from pathlib import Path
import pickle
import string
import sys
from typing import Callable

from modlamp.descriptors import GlobalDescriptor
import numpy as np
import pandas as pd

from pepsipy.constants import (
    AA_FORMULA,
    AA_LETTERS,
    AA_THREE_LETTER_CODE,
    AA_ONE_LETTER_CODE,
    AA_WEIGHTS,
    HYDROPATHY_INDICES,
    WATER,
    CHEMICAL_CLASS,
    CHARGE_CLASS,
)
from pepsipy.utils import (
    sanitize_seq,
    get_distinct_seq,
    extract_related_kwargs,
)


def _seq_length(seq: str) -> int:
    """
    Computes the length in a given sequence.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
        seq: Given sequence
    """
    invalid = set(seq) - AA_LETTERS
    if invalid:
        raise ValueError(f"Invalid amino acid symbol: {', '.join(sorted(invalid))}")
    return len(seq)


def _aa_frequency(seq: str) -> dict[str, int]:
    """
    Computes the frequency of each amino acid in a given sequence.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
        seq: Given sequence
    """
    try:
        freq = {val: 0 for val in AA_LETTERS}
        for aa in seq:
            freq[aa] += 1
        return freq
    except KeyError as e:
        raise ValueError(f"Invalid amino acid symbol: '{e.args[0]}'") from None


def _molecular_weight(seq: str) -> float:
    """
    Computes the average molecular weight of a given sequence in Da.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
        seq: Given sequence
    """
    num = _seq_length(seq)
    weight = sum(AA_WEIGHTS[aa] for aa in seq) - (num - 1) * WATER
    return round(weight, 2)


def _three_letter_code(seq: str) -> str:
    """
    Converts a sequence of amino acids into its representation in three letter code.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
        seq: Given sequence
    """
    try:
        return "".join(AA_THREE_LETTER_CODE[aa] for aa in seq)
    except KeyError as e:
        raise ValueError(f"Invalid amino acid symbol: '{e.args[0]}'") from None


def _one_letter_code(codes: str) -> str:
    """
    Converts concatenated three-letter amino acid codes into their one-letter code representation.
        codes: Sequence in three letter code
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


def _gravy(seq: str) -> float:
    """
    Computes the GRAVY (grand average of hydropathy) score of a given sequence.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
        seq: Given sequence
    """
    num = _seq_length(seq)
    hydropathy_sum = sum(HYDROPATHY_INDICES[aa] for aa in seq)
    return round(hydropathy_sum / num, 3)


def _molecular_formula(seq: str) -> str:
    """
    Computes the molecular formula of a given sequence.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
        seq: Given sequence
    """
    total_atoms = {}
    for aa in seq:
        for atom, count in AA_FORMULA[aa].items():
            total_atoms[atom] = total_atoms.get(atom, 0) + count

    num_bindings = _seq_length(seq) - 1
    total_atoms["H"] -= 2 * num_bindings
    total_atoms["O"] -= num_bindings

    sorted_atoms = ["C", "H", "N", "O", "S"]
    formula_elems = [
        f"{atom}{total_atoms[atom]}" if total_atoms[atom] > 1 else atom
        for atom in sorted_atoms
        if atom in total_atoms
    ]
    return "".join(formula_elems)


def _isoelectric_point(seq: str, option: str = "bjellqvist") -> float:
    """
    Computes the theoretical pI of a given sequence. One can choose between IPC 2.0 (Kozlowski, 2021) to predict
    the pI with the pretrained model IPC2.peptide.svr19 or biopython package based on (Bjellqvist, 1993)
        seq: Given sequence
        option: Specification of which approach to use, can be "bjellqvist" or "kozlowski"
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

        # Ignoring warning for import from local module
        from ipc2_lib.svr_functions import get_pI_features  # type: ignore

        X, _ = get_pI_features([[clean_seq, ""]])
        X = np.array(X)

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        return float(round(model.predict(X)[0], 2))

    elif option == "bjellqvist":
        desc = GlobalDescriptor(seq)
        desc.isoelectric_point(amide=False)
        return float(round(desc.descriptor[0][0], 2))

    else:
        raise ValueError(f"Unknown option: {option}")


def _aromaticity(seq: str) -> float:
    """
    Computes the aromaticity of a given sequence by calculating the relative
    frequency of amino acids F, Y, and W (Lobry and Gautier, 1994).
        seq: Given sequence
    """
    freq = _aa_frequency(seq)
    seq_len = _seq_length(seq)
    num_aromatic = sum(freq[aa] for aa in ["F", "Y", "W"])
    return round(num_aromatic / seq_len, 3)


def _aa_classification(seq: str, classify_by: str = "chemical") -> dict:
    """
    Computes the absolute frequency of each class (Pommié et al., 2004).
        seq: Given sequence
        classify_by: Specification of how the amino acids should be classified, can be "chemical" or "charge"
    """
    freq = _aa_frequency(seq)
    if classify_by == "chemical":
        return {
            _class: sum(freq[aa] for aa in aminos)
            for _class, aminos in CHEMICAL_CLASS.items()
        }
    elif classify_by == "charge":
        return {
            _class: sum(freq[aa] for aa in aminos)
            for _class, aminos in CHARGE_CLASS.items()
        }
    else:
        raise ValueError(f"Unknown option: {classify_by}")


def _charge_at_ph(seq: str, ph: float = 7.0) -> float:
    """
    Computes the charge of a given sequence at a given pH level.
        seq: Given sequence
        ph: Given ph level
    """
    desc = GlobalDescriptor(seq)
    desc.calculate_charge(ph=ph, amide=False)
    return float(round(desc.descriptor[0][0], 2))


def _charge_density(seq: str, ph: float = 7.0) -> float:
    """
    Computes the charge density (charge / molecular weight) of a given sequence at a given pH level.
        seq: Given sequence
        ph: Given ph level
    """
    return round(_charge_at_ph(seq, ph) / _molecular_weight(seq), 5)


def _boman_index(seq: str) -> float:
    """
    Computes the boman index of a given sequence (Boman, 2003).
        seq: Given sequence
    """
    desc = GlobalDescriptor(seq)
    desc.boman_index()
    return float(round(desc.descriptor[0][0], 2))


def _aliphatic_index(seq: str) -> float:
    """
    Computes the aliphatic index of a given sequence (Ikai, 1980).
        seq: Given sequence
    """
    freq = _aa_frequency(seq)
    length = _seq_length(seq)
    nA = freq["A"]
    nV = freq["V"]
    nI = freq["I"]
    nL = freq["L"]
    return round((nA + 2.9 * nV + 3.9 * (nI + nL)) * 100.0 / length, 2)


def _extinction_coefficient(seq: str, oxidized: bool = False) -> int:
    """
    Computes the extinction coefficient of a given sequence. Formula is based on (Gill, von Hippel, 1989) and improved by (Pace et al., 1995).
        seq: Given sequence
        oxidized: True, if all pairs of Cysteine form cystines (disulfide bridges). False, if all Cysteine residues are reduced.
    """
    freq = _aa_frequency(seq)
    extinction = freq["W"] * 5500 + freq["Y"] * 1490
    if oxidized:
        extinction += (freq["C"] // 2) * 125
    return extinction


def _instability_index(seq: str) -> float:
    """
    Computes the instability index based on (Guruprasad et al., 1990) of a given sequence.
        seq: Given sequence
    """
    desc = GlobalDescriptor(seq)
    desc.instability_index()
    return float(round(desc.descriptor[0][0], 2))


@dataclass
class Feature:
    label: str
    numeric: bool
    method: Callable
    param_map: dict = None


FEATURES = {
    "molecular_weight": Feature("Molecular weight", True, _molecular_weight),
    "three_letter_code": Feature("Three letter code", False, _three_letter_code),
    "molecular_formula": Feature("Molecular formula", False, _molecular_formula),
    "seq_length": Feature("Sequence length", True, _seq_length),
    "aromaticity": Feature("Aromaticity", True, _aromaticity),
    "aliphatic_index": Feature("Aliphatic index", True, _aliphatic_index),
    "charge_at_ph": Feature(
        "Charge", True, _charge_at_ph, {"charge_at_ph_level": "ph"}
    ),
    "charge_density": Feature(
        "Charge density",
        True,
        _charge_density,
        {"charge_density_level": "ph"},
    ),
    "isoelectric_point": Feature(
        "Isoelectric point",
        True,
        _isoelectric_point,
        {"isoelectric_point_option": "option"},
    ),
    "gravy": Feature("GRAVY", True, _gravy),
    "extinction_coefficient": Feature(
        "Extinction coefficient",
        True,
        _extinction_coefficient,
        {"extinction_coefficient_oxidized": "oxidized"},
    ),
    "boman_index": Feature("Boman index", True, _boman_index),
    "instability_index": Feature("Instability index", True, _instability_index),
}


def _compute_features(
    params: dict,
    df: pd.DataFrame = None,
    seq: str = None,
) -> pd.DataFrame:
    """
    Computes all selected features on a pandas DataFrame. See API class 'Calculator' for more information.
    """
    select_all = params.get("select_all")
    # On single sequence or dataset
    if seq is not None:
        df = pd.DataFrame({"Sequence": [seq]})
        sequences = pd.DataFrame({"Sequence": [seq]})
    else:
        sequences = get_distinct_seq(df)

    # Feature mappings as (label, function call with optional params)
    mappings = {}
    for key, feature in FEATURES.items():
        kwargs = (
            extract_related_kwargs(feature.param_map, params)
            if feature.param_map
            else {}
        )
        func = feature.method if not kwargs else partial(feature.method, **kwargs)
        mappings[key] = (feature.label, func)
    # Filter selected features (feature = True)
    chosen_features = {
        col: func
        for feature, (col, func) in mappings.items()
        if params.get(feature) or select_all
    }

    # Compute features
    for feature, func in chosen_features.items():
        sequences[feature] = sequences["Sequence"].apply(func)

    merged = pd.merge(
        df,
        sequences,
        on="Sequence",
        how="left",
    )
    return merged
