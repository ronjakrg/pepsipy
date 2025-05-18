import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from peptidefeatures.constants import COLORS
from peptidefeatures.utils import get_group

def features(
    df: pd.DataFrame,
    plot_type: str,
    groups: list,
    feature_a: str,
    feature_b: str,
) -> go.Figure:
    """
    Creates a plot to compare two features across groups.
    """
    peptides = df.copy()
    peptides["Group"] = peptides["Sample"].apply(lambda x: get_group(x, groups))

    if plot_type == "scatter":
        fig = px.scatter(
            peptides,
            x=feature_a,
            y=feature_b,
            color="Group",
            color_discrete_sequence=COLORS,
            title="Comparison of peptide features across groups",
        )
    elif plot_type == "histogramm":
        print("Not implemented yet.")
    return fig
