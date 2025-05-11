import plotly.express as px
import plotly.graph_objects as go

from peptidefeatures.constants import LABEL


def metrics_compare_graph(peptides, func_a, func_b) -> go.Figure:
    """
    Creates a scatter plot from two given methods that compute metrics.
    """
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
