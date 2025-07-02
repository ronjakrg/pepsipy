from pathlib import Path

# <---- BIOCHEMICAL ---->

# Taken from "Nomenclature and Symbolism for Amino, Acids and Peptides Recommendations 1983"
# https://doi.org/10.1351/pac198456050595
AA_LETTERS = set("ACDEFGHIKLMNPQRSTVWY")
AA_THREE_LETTER_CODE = {
    "A": "Ala",
    "C": "Cys",
    "D": "Asp",
    "E": "Glu",
    "F": "Phe",
    "G": "Gly",
    "H": "His",
    "I": "Ile",
    "K": "Lys",
    "L": "Leu",
    "M": "Met",
    "N": "Asn",
    "P": "Pro",
    "Q": "Gln",
    "R": "Arg",
    "S": "Ser",
    "T": "Thr",
    "V": "Val",
    "W": "Trp",
    "Y": "Tyr",
}
AA_ONE_LETTER_CODE = {
    "Ala": "A",
    "Cys": "C",
    "Asp": "D",
    "Glu": "E",
    "Phe": "F",
    "Gly": "G",
    "His": "H",
    "Ile": "I",
    "Lys": "K",
    "Leu": "L",
    "Met": "M",
    "Asn": "N",
    "Pro": "P",
    "Gln": "Q",
    "Arg": "R",
    "Ser": "S",
    "Thr": "T",
    "Val": "V",
    "Trp": "W",
    "Tyr": "Y",
}
AA_FORMULA = {
    "A": {"C": 3, "H": 7, "N": 1, "O": 2},
    "C": {"C": 3, "H": 7, "N": 1, "O": 2, "S": 1},
    "D": {"C": 4, "H": 7, "N": 1, "O": 4},
    "E": {"C": 5, "H": 9, "N": 1, "O": 4},
    "F": {"C": 9, "H": 11, "N": 1, "O": 2},
    "G": {"C": 2, "H": 5, "N": 1, "O": 2},
    "H": {"C": 6, "H": 9, "N": 3, "O": 2},
    "I": {"C": 6, "H": 13, "N": 1, "O": 2},
    "K": {"C": 6, "H": 14, "N": 2, "O": 2},
    "L": {"C": 6, "H": 13, "N": 1, "O": 2},
    "M": {"C": 5, "H": 11, "N": 1, "O": 2, "S": 1},
    "N": {"C": 4, "H": 8, "N": 2, "O": 3},
    "P": {"C": 5, "H": 9, "N": 1, "O": 2},
    "Q": {"C": 5, "H": 10, "N": 2, "O": 3},
    "R": {"C": 6, "H": 14, "N": 4, "O": 2},
    "S": {"C": 3, "H": 7, "N": 1, "O": 3},
    "T": {"C": 4, "H": 9, "N": 1, "O": 3},
    "V": {"C": 5, "H": 11, "N": 1, "O": 2},
    "W": {"C": 11, "H": 12, "N": 2, "O": 2},
    "Y": {"C": 9, "H": 11, "N": 1, "O": 3},
}

# Taken from IUPAC Standards Online Database
# https://doi.org/10.1515/iupac
AA_WEIGHTS = {
    "A": 89.094,
    "C": 121.154,
    "D": 133.103,
    "E": 147.130,
    "F": 165.192,
    "G": 75.067,
    "H": 155.157,
    "I": 131.175,
    "K": 146.190,
    "L": 131.175,
    "M": 149.208,
    "N": 132.119,
    "P": 115.132,
    "Q": 146.146,
    "R": 174.204,
    "S": 105.093,
    "T": 119.12,
    "V": 117.148,
    "W": 204.229,
    "Y": 181.191,
}
WATER = 18.015

# Taken from Kyte and Doolittle, 1982
# https://doi.org/10.1016/0022-2836(82)90515-0
HYDROPATHY_INDICES = {
    "A": 1.8,
    "C": 2.5,
    "D": -3.5,
    "E": -3.5,
    "F": 2.8,
    "G": -0.4,
    "H": -3.2,
    "I": 4.5,
    "K": -3.9,
    "L": 3.8,
    "M": 1.9,
    "N": -3.5,
    "P": -1.6,
    "Q": -3.5,
    "R": -4.5,
    "S": -0.8,
    "T": -0.7,
    "V": 4.2,
    "W": -0.9,
    "Y": -1.3,
}

# Taken from Pommiè et al., 2004
# https://doi.org/10.1002/jmr.647
CHEMICAL_CLASS = {
    "Aliphatic": ["I", "L", "V", "A"],
    "Sulfur": ["M", "C"],
    "Hydroxyl": ["T", "S"],
    "Basic": ["K", "R", "H"],
    "Acidic": ["E", "D"],
    "Amide": ["Q", "N"],
    "Other": ["F", "W", "Y", "P", "G"],
}
CHEMICAL_CLASS_PER_AA = {
    "I": "Aliphatic",
    "L": "Aliphatic",
    "V": "Aliphatic",
    "A": "Aliphatic",
    "M": "Sulfur",
    "C": "Sulfur",
    "T": "Hydroxyl",
    "S": "Hydroxyl",
    "K": "Basic",
    "R": "Basic",
    "H": "Basic",
    "E": "Acidic",
    "D": "Acidic",
    "Q": "Amide",
    "N": "Amide",
    "F": "Other",
    "W": "Other",
    "Y": "Other",
    "P": "Other",
    "G": "Other",
}
CHARGE_CLASS = {
    "Non-polar": ["F", "W", "I", "L", "M", "V", "C", "P", "A", "G"],
    "Uncharged": ["Y", "T", "S", "Q", "N"],
    "Charged": ["K", "R", "H", "E", "D"],
}
CHARGE_CLASS_PER_AA = {
    "F": "Non-polar",
    "W": "Non-polar",
    "I": "Non-polar",
    "L": "Non-polar",
    "M": "Non-polar",
    "V": "Non-polar",
    "C": "Non-polar",
    "P": "Non-polar",
    "A": "Non-polar",
    "G": "Non-polar",
    "Y": "Uncharged",
    "T": "Uncharged",
    "S": "Uncharged",
    "Q": "Uncharged",
    "N": "Uncharged",
    "K": "Charged",
    "R": "Charged",
    "H": "Charged",
    "E": "Charged",
    "D": "Charged",
}

# <---- MISCELLANEOUS ---->

COLORS = [
    "#CE5A5A",
    "#4A536A",
    "#87A8B9",
    "#F1A765",
    "#A7A1B2",
    "#8E3F25",
    "#511D43",
]

PROJECT_PATH = Path(__file__).resolve().parent.parent.parent
EXTERNAL_PATH = PROJECT_PATH / "external"
