import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from peptidefeatures.constants import AA_WEIGHTS, COLORS, HYDROPATHY_INDICES
from peptidefeatures.features import aa_frequency, aa_classification


def aa_distribution(
    seq: str,
    order_by: str = "category ascending",
    show_all: bool = False,
) -> go.Figure:
    """
    Computes a bar plot showing the frequency distribution for a given sequence.
        seq: Given sequence
        order: Specification of how the amino acids should be sorted, can be any of "frequency", "alphabetical", "classification", "hydropathy" or "weight".
        show_all: Specification if all amino acids should be listed, even when not found in the sequence
    """
    freq = aa_frequency(seq)
    if not show_all:
        freq = {key: val for key, val in freq.items() if val > 0}
    fig = px.bar(
        x=list(freq.keys()),
        y=list(freq.values()),
        labels={
            "x": "Amino Acid",
            "y": "Frequency",
        },
        title=f"Amino Acid Frequency of Sequence {seq}",
        color_discrete_sequence=COLORS,
    )
    fig.update_yaxes(tickmode="linear", tick0=0, dtick=1)

    # Sort amino acids by given order specification
    if order_by == "frequency":
        fig.update_xaxes(categoryorder="total ascending")
    elif order_by == "alphabetical":
        fig.update_xaxes(categoryorder="category ascending")
    elif order_by == "classification":
        # TODO Add when aa classification is implemented
        raise NotImplementedError
    elif order_by == "hydropathy":
        sorted_aa = sorted(list(freq.keys()), key=lambda aa: HYDROPATHY_INDICES[aa])
        fig.update_xaxes(categoryorder="array", categoryarray=sorted_aa)
    elif order_by == "weight":
        sorted_aa = sorted(list(freq.keys()), key=lambda aa: AA_WEIGHTS[aa])
        fig.update_xaxes(categoryorder="array", categoryarray=sorted_aa)
    else:
        raise ValueError(f"Unknown option for sorting amino acids: {order_by}.")
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


def classification_plot(seq: str, classify_by: str = "chemical") -> go.Figure:
    """
    Computes a bar plot showing the frequency of each amino acid class based on (Pommié et al., 2004).
        seq: Given sequence
        classify_by: Specification of how the amino acids should be classified, can be "chemical" or "charge".
    """
    classification = aa_classification(seq, classify_by)
    df = pd.DataFrame(
        {"Class": classification.keys(), "Frequency": classification.values()}
    )
    fig = px.bar(
        df,
        x="Class",
        y="Frequency",
        title=f"Classification ({classify_by}) of {seq}",
        color="Class",
        color_discrete_sequence=COLORS,
    )
    fig.update_yaxes(tickmode="linear", tick0=0, dtick=1)
    return fig
