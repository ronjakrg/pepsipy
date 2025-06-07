import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from peptidefeatures.constants import COLORS
from peptidefeatures.utils import get_group


def scatter_features(
    df: pd.DataFrame,
    groups: list,
    feature_a: str,
    feature_b: str,
) -> go.Figure:
    """
    Creates a scatter plot to compare two features across groups.
    """
    peptides = df.copy()
    peptides["Group"] = peptides["Sample"].apply(lambda x: get_group(x, groups))
    fig = px.scatter(
        peptides,
        x=feature_a,
        y=feature_b,
        color="Group",
        color_discrete_sequence=COLORS,
        symbol="Group",
        symbol_sequence=["square", "circle"],
        title="Comparison of Peptide Features Across Groups",
    )
    fig.update_traces(marker=dict(size=10))
    return fig


def box_feature(
    df: pd.DataFrame,
    groups: list,
    feature: str,
) -> go.Figure:
    """
    Creates a box plot to compare a feature between groups.
    """
    peptides = df.copy()
    peptides["Group"] = peptides["Sample"].apply(lambda x: get_group(x, groups))

    fig = px.box(
        peptides,
        x="Group",
        y=feature,
        color="Group",
        color_discrete_sequence=COLORS,
        title=f"Distribution of {feature} Across Groups",
    )
    return fig
