# ────────────────────────────────────────────────
#                     PLAYGROUND
#   This file is just an experimental sandbox
#   and is not part of the implementation.
#
#   To run this code, execute python -m src.
# ────────────────────────────────────────────────

import pandas as pd

from src.features.sequence import aa_number, aa_frequency
from src.plots.sequence import aa_freq_distribution

peptides = pd.read_csv("./data/peptides.csv")
peptides["aa_number"] = peptides["Sequence"].apply(aa_number)
peptides["aa_frequency"] = peptides["Sequence"].apply(aa_frequency)
#print(peptides.head())

fig = aa_freq_distribution(aa_frequency("PEPTIDE"))
fig.show()