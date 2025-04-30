# ────────────────────────────────────────────────
#                     PLAYGROUND
#   This file is just an experimental sandbox
#   and is not part of the implementation.
#
#   To run this code, execute python -m src.
# ────────────────────────────────────────────────

import pandas as pd

from src.features.sequence import aa_number

peptides = pd.read_csv("./data/peptides.csv")
peptides["aa_number"] = peptides["Sequence"].apply(aa_number)
print(peptides.head())