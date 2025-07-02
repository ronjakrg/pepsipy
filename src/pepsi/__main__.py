# ─────────────────────────────────────────────────────
#                     PLAYGROUND
#   This file is just an experimental sandbox and is
#   not part of the implementation.
#
#   To run this code, execute python -m peptidefeatures.
# ──────────────────────────────────────────────────────

import pandas as pd
from pepsi.calculator import Calculator

print("# Executing main code from peptidefeatures ... #")

calc = Calculator()
calc.set_dataset(
    pd.read_csv("/home/ronja/git/thesis-peptide-features/data/peptides.csv")
)
calc.set_feature_params(
    gravy=True,
)
calc.set_plot_params(
    aa_distribution=True,
    aa_distribution_show_all=True,
)
calc.set_seq("NVHWYQQKPGQAPVLVIYR")
result = calc.get_features()
plots = calc.get_plots()

plot = calc.aa_distribution("PEPTIDE", "classes chemical", True)
plot.show()
