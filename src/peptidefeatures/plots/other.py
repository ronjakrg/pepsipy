import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from peptidefeatures.constants import COLORS, HYDROPATHY_INDICES
from peptidefeatures.features import aa_frequency


def aa_distribution(seq: str) -> go.Figure:
    """
    Computes a bar plot showing the frequency distribution for a given sequence.
    """
    freq = aa_frequency(seq)
    fig = px.bar(
        x=list(freq.keys()),
        y=list(freq.values()),
        labels={
            "x": "Amino Acid",
            "y": "Frequency",
        },
        title="Amino Acid Frequency",
        color_discrete_sequence=COLORS,
    )
    fig.update_xaxes(categoryorder="category ascending")
    fig.update_yaxes(tickmode="linear", tick0=0, dtick=1)
    return fig


def hydropathy_plot(seq: str) -> go.Figure:
    """
    Computes a hydropathy profile plot for a given sequence.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
    """
    df = pd.DataFrame({"Amino Acid": list(seq)})
    df["Hydropathy Index"] = df["Amino Acid"].map(HYDROPATHY_INDICES)
    df.index = df.index + 1
    baseline_df = pd.DataFrame(
        {"Amino Acid": ["None"], "Hydropathy Index": [0.0]}, index=[0]
    )
    df = pd.concat([baseline_df, df])
    df.index.name = "Residue Number"

    fig = px.line(
        df,
        y="Hydropathy Index",
        title=f"Hydropathy Plot of Sequence {seq}",
        color_discrete_sequence=COLORS,
        hover_data={"Amino Acid": True, "Hydropathy Index": True},
    )
    fig.add_hline(
        y=0,
        line_dash="dash",
    )
    return fig
