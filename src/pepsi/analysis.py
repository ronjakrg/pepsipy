import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import mannwhitneyu

from pepsi.constants import COLORS


def _mann_whitney_u_test(
    df: pd.DataFrame,
    feature: str = "GRAVY",
    group_by: str = "Group",
    group_a: str = "CTR",
    group_b: str = "T1D",
    alternative: str = "two-sided",
) -> go.Figure:
    """
    Performs a Mann-Whitney U test on a feature between two groups and creates a box plot with a significance bracket and p-value.
        df: pandas DataFrame that contains the features
        feature: Feature to be compared
        group_by: Metadata aspect (e.g. Group, Batch, ...) that peptides get grouped by
        group_a: First comparison group
        group_b: Second comparison group
        alternative: Chosen test alternative (two-sided, greater, less)
    """
    # Prepare data
    sub = df.loc[
        df[group_by].isin([group_a, group_b]), [group_by, feature, "Sequence"]
    ].copy()
    sub = sub.dropna(subset=[feature])
    sub = sub.drop_duplicates([group_by, "Sequence"], keep="first")
    x = sub.loc[sub[group_by] == group_a, feature].to_numpy()
    y_pos = sub.loc[sub[group_by] == group_b, feature].to_numpy()
    num_x, num_y = len(x), len(y_pos)
    if num_x < 2 or num_y < 2:
        raise ValueError(
            f"Not enough values: {group_a}={num_x}, {group_b}={num_y} (at least 2 per group required)."
        )

    # Execute test
    mw = mannwhitneyu(x, y_pos, alternative=alternative, method="auto")

    # Process results
    p = float(mw.pvalue)

    print(f"{num_x} unique sequences in {group_a}, {num_y} in {group_b}")
    print(f"Median {group_a}: {round(np.median(x), 3)}")
    print(f"Median {group_b}: {round(np.median(y_pos), 3)}")
    print(f"p-value: {round(p, 3)}")

    # Boxplot
    fig = px.box(
        sub,
        x=group_by,
        y=feature,
        color=group_by,
        color_discrete_sequence=COLORS,
        title=f"Mann-Whitney U test of {feature}: {group_a} vs {group_b}",
        hover_name="Sequence",
    )

    # Significance bracket
    BOX_BRACKET_GAP = 0.05
    BRACKET_HEIGHT = 0.03

    feature_min = float(sub[feature].min())
    feature_max = float(sub[feature].max())
    span = max(feature_max - feature_min, 1.0)
    y_pos = feature_max + BOX_BRACKET_GAP * span
    y_height = BRACKET_HEIGHT * span
    x_group_a, x_group_b = group_a, group_b

    fig.add_shape(  # Left part
        type="line",
        xref="x",
        yref="y",
        x0=x_group_a,
        x1=x_group_a,
        y0=y_pos,
        y1=y_pos + y_height,
    )
    fig.add_shape(  # Middle part
        type="line",
        xref="x",
        yref="y",
        x0=x_group_a,
        x1=x_group_b,
        y0=y_pos + (y_height * 0.88),
        y1=y_pos + (y_height * 0.88),
    )
    fig.add_shape(  # Right part
        type="line",
        xref="x",
        yref="y",
        x0=x_group_b,
        x1=x_group_b,
        y0=y_pos + y_height,
        y1=y_pos,
    )
    fig.add_annotation(
        x=0.5,
        xref="paper",
        y=y_pos + y_height,
        yref="y",
        text=f"p = {round(p, 3)}",
        showarrow=False,
        align="center",
        yanchor="bottom",
    )

    fig.update_yaxes(
        range=[
            feature_min - BOX_BRACKET_GAP * span,
            y_pos + y_height + 2 * BOX_BRACKET_GAP * span,
        ]
    )
    return fig
