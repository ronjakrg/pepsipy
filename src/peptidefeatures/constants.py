# <---- BIOCHEMICAL ---->

# Taken from "Nomenclature and Symbolism for Amino, Acids and Peptides Recommendations 1983"
# https://doi.org/10.1351/pac198456050595
AA_LETTERS = set("ACDEFGHIKLMNPQRSTVWY")
AA_THREE_LETTERS = {
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

# <---- MISCELLANEOUS ---->

# Contains a readable label for each function id
LABEL = {
    "aa_number": "Number of Amino Acids",
    "aa_frequency": "Frequency of Amino Acids",
    "molecular_weight": "Molecular Weight (Da)",
}

# Color selection for plots
COLORS = ["#CE5A5A", "#4A536A"]
