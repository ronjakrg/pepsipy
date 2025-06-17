import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from peptidefeatures.constants import COLORS
from peptidefeatures.utils import find_group, get_column_name

# TODO Merge plot functions into one python file


def scatter_features(
    df: pd.DataFrame,
    feature_a: str,
    feature_b: str,
    groups: list = None,
    intensity_threshold: float = None,
) -> go.Figure:
    """
    Creates a scatter plot to compare two features across groups.
        df: Dataframe that contains the features
        groups: List of prefixes representing groups that can be found in column "Sample"
        feature_a: Feature shown on x-axis
        feature_b: Feature shown on y-axis
        intensity_threshold: Peptides with intensities below this threshold are not included
    """
    peptides = df.copy()
    intensity_col = get_column_name(peptides, "intensity")
    seq_col = get_column_name(peptides, "sequence")
    if intensity_threshold is not None:
        peptides = peptides[peptides[intensity_col] > intensity_threshold]
    # TODO Generalize sample column
    peptides["Group"] = peptides["Sample"].apply(lambda x: find_group(x, groups))

    fig = px.scatter(
        peptides,
        x=feature_a,
        y=feature_b,
        color="Group",
        color_discrete_sequence=COLORS,
        symbol="Group",
        symbol_sequence=["square", "circle", "arrow-up", "star"],
        title="Comparison of peptide features across groups",
        hover_name=seq_col,
    )
    fig.update_traces(marker=dict(size=10))
    return fig


def box_feature(
    df: pd.DataFrame,
    feature: str,
    groups: list = None,
    intensity_threshold: float = None,
) -> go.Figure:
    """
    Creates box plots for each group to compare a feature between groups.
        df: Dataframe that contains the features
        groups: List of prefixes representing groups that can be found in column "Sample"
        feature: Feature to be compared
        intensity_threshold: Peptides with intensities below this threshold are not included
    """
    peptides = df.copy()
    intensity_col = get_column_name(peptides, "intensity")
    seq_col = get_column_name(peptides, "sequence")
    if intensity_threshold is not None:
        peptides = peptides[peptides[intensity_col] > intensity_threshold]
    peptides["Group"] = peptides["Sample"].apply(lambda x: find_group(x, groups))

    fig = px.box(
        peptides,
        x="Group",
        y=feature,
        color="Group",
        color_discrete_sequence=COLORS,
        title=f"Distribution of {feature} across groups",
        hover_name=seq_col,
    )
    return fig
