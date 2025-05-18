import plotly.express as px
import plotly.graph_objects as go


def aa_freq_distribution(freq: dict[str, int]) -> go.Figure:
    """
    Creates a bar plot with amino acid frequency distribution.
    """
    fig = px.bar(
        x=list(freq.keys()),
        y=list(freq.values()),
        labels={
            "x": "Amino Acid",
            "y": "Frequency",
        },
        title="Amino Acid Frequency",
    )
    fig.update_yaxes(tickmode="linear", tick0=0, dtick=1)
    return fig
