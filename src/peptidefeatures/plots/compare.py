import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Callable

from peptidefeatures.constants import LABEL


def features(
    df: pd.DataFrame,
    func_a: Callable,
    func_b: Callable,
) -> go.Figure:
    """
    Creates a scatter plot from two given methods that compute metrics.
    """
    peptides = df.copy()
    metric_a = func_a.__name__
    metric_b = func_b.__name__

    peptides[metric_a] = peptides["Sequence"].apply(func_a)
    peptides[metric_b] = peptides["Sequence"].apply(func_b)
    fig = px.scatter(
        peptides,
        x=metric_a,
        y=metric_b,
        labels={
            metric_a: LABEL[metric_a],
            metric_b: LABEL[metric_b],
        },
        title="Comparison of Peptide Metrics",
    )
    return fig
