# <---- BIOCHEMICAL ---->

# Taken from "Nomenclature and Symbolism for Amino, Acids and Peptides Recommendations 1983"
# https://doi.org/10.1351/pac198456050595
AA_LETTERS = "ACDEFGHIKLMNPQRSTVWY"
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

# <---- MISCELLANEOUS ---->

# Contains a readable label for each function id
LABEL = {
    "aa_number": "Number of Amino Acids",
    "aa_frequency": "Frequency of Amino Acids",
    "molecular_weight": "Molecular Weight (Da)",
}