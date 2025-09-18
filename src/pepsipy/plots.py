from dataclasses import dataclass
from typing import Callable
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import mannwhitneyu
import warnings

from pepsipy.constants import (
    AA_WEIGHTS,
    COLORS,
    COLORS_BY_NAME,
    HYDROPATHY_INDICES,
    CHEMICAL_CLASS,
    CHARGE_CLASS,
    CHEMICAL_CLASS_PER_AA,
    CHARGE_CLASS_PER_AA,
)
from pepsipy.features import (
    _aa_frequency,
    _aa_classification,
    _charge_at_ph,
    _seq_length,
)
from pepsipy.utils import (
    get_column_name,
    normalize_color,
    extract_related_kwargs,
    convert_exponential_to_suffix,
)


# Sequence-based
def _aa_distribution(
    seq: str,
    order_by: str = "frequency",
    show_all: bool = False,
) -> go.Figure:
    """
    Computes a bar plot showing the frequency distribution for a given sequence.
        seq: Given sequence
        order_by: Specification of how the amino acids should be sorted, can be any of "frequency", "alphabetical", "classes chemical", "classes charge", "hydropathy" or "weight".
        show_all: Specification if all amino acids should be listed, even when not found in the sequence
    """
    freq = _aa_frequency(seq)
    num = _seq_length(seq)
    df = pd.DataFrame({"Amino acid": freq.keys(), "Frequency": freq.values()})
    if not show_all:
        df = df[df["Frequency"] > 0]
    df["Proportion"] = (df["Frequency"] / num * 100).round(3)
    if order_by in ["frequency", "alphabetical", "hydropathy", "weight"]:
        fig = px.bar(
            df,
            x="Amino acid",
            y="Frequency",
            color_discrete_sequence=COLORS,
            custom_data=["Proportion"],
        )
        if order_by == "frequency":
            fig.update_xaxes(categoryorder="total ascending")
        elif order_by == "alphabetical":
            fig.update_xaxes(categoryorder="category ascending")
        elif order_by == "hydropathy":
            sorted_aa = sorted(df["Amino acid"], key=lambda aa: HYDROPATHY_INDICES[aa])
            fig.update_xaxes(categoryorder="array", categoryarray=sorted_aa)
        elif order_by == "weight":
            sorted_aa = sorted(df["Amino acid"], key=lambda aa: AA_WEIGHTS[aa])
            fig.update_xaxes(categoryorder="array", categoryarray=sorted_aa)
        fig.update_traces(
            hovertemplate="Amino acid=%{x}<br>Frequency=%{y} (%{customdata} %)<extra></extra>",
        )

    elif order_by in ["classes chemical", "classes charge"]:
        if order_by == "classes chemical":
            df["Class"] = df["Amino acid"].map(CHEMICAL_CLASS_PER_AA)
            classes = list(CHEMICAL_CLASS.keys())
        elif order_by == "classes charge":
            df["Class"] = df["Amino acid"].map(CHARGE_CLASS_PER_AA)
            classes = list(CHARGE_CLASS.keys())

        # Filter occuring classes
        classes = [cls for cls in classes if (df["Class"] == cls).any()]
        # Compute column widths by number of aa per class
        col_widths = [df[df["Class"] == cls].shape[0] for cls in classes]
        rel_column_widths = [w / sum(col_widths) for w in col_widths]

        # Create plot
        fig = make_subplots(
            cols=len(classes),
            rows=1,
            subplot_titles=classes,
            column_widths=rel_column_widths,
            horizontal_spacing=0.3 / len(classes),
            shared_yaxes=True,
        )
        # Create bar per class
        CLASS_TO_COLOR = dict(zip(classes, COLORS))
        for i, cls in enumerate(classes):
            class_df = df[df["Class"] == cls].sort_values("Amino acid")
            fig.add_trace(
                go.Bar(
                    x=class_df["Amino acid"],
                    y=class_df["Frequency"],
                    marker_color=CLASS_TO_COLOR[cls],
                    hovertemplate="Amino acid=%{x}<br>Frequency=%{y} (%{customdata} %)<extra></extra>",
                    showlegend=False,
                    customdata=class_df["Proportion"],
                ),
                row=1,
                col=i + 1,
            )
            fig.update_xaxes(title_text=None, row=1, col=i + 1, tickfont=dict(size=10))
        fig.update_layout(
            barmode="group",
            yaxis_title="Frequency",
            annotations=[dict(font=dict(size=12)) for _ in fig.layout.annotations],
        )

    else:
        raise ValueError(f"Unknown option for sorting amino acids: {order_by}.")
    fig.update_layout(title=f"Amino acid frequency of sequence {seq}")
    fig.update_yaxes(tickmode="linear", tick0=0, dtick=1)
    return fig


def _hydropathy_profile(seq: str) -> go.Figure:
    """
    Computes a hydropathy profile plot for a given sequence.
    Note: The input sequence must be pre-sanitized to compute only valid amino acids.
    """
    df = pd.DataFrame({"Amino acid": list(seq)})
    df["Hydropathy index"] = df["Amino acid"].map(HYDROPATHY_INDICES)
    df.index = df.index + 1
    baseline_df = pd.DataFrame(
        {"Amino acid": ["None"], "Hydropathy index": [0.0]}, index=[0]
    )
    df = pd.concat([baseline_df, df])
    df.index.name = "Residue number"

    fig = px.line(
        df,
        y="Hydropathy index",
        title=f"Hydropathy plot of sequence {seq}",
        hover_data={"Amino acid": True, "Hydropathy index": True},
    )
    fig.update_traces(line=dict(color=COLORS_BY_NAME["red"], width=3))
    fig.add_hline(
        y=0,
        line_dash="dash",
    )
    return fig


def _classification(seq: str, classify_by: str = "chemical") -> go.Figure:
    """
    Computes a bar plot showing the frequency of each amino acid class based on (Pommié et al., 2004).
        seq: Given sequence
        classify_by: Specification of how the amino acids should be classified, can be "chemical" or "charge".
    """
    classification = _aa_classification(seq, classify_by)
    num = _seq_length(seq)
    df = pd.DataFrame(
        {"Class": classification.keys(), "Frequency": classification.values()}
    )
    df["Proportion"] = (df["Frequency"] / num * 100).round(3)
    fig = px.bar(
        df,
        x="Class",
        y="Frequency",
        title=f"Classification ({classify_by}) of {seq}",
        color="Class",
        color_discrete_sequence=COLORS,
        custom_data=["Proportion"],
    )
    fig.update_yaxes(tickmode="linear", tick0=0, dtick=1)
    fig.update_traces(
        showlegend=False,
        hovertemplate="Class=%{x}<br>Frequency=%{y} (%{customdata} %)<extra></extra>",
    )
    return fig


# Dataset-wide
def _titration_curve(seq: str) -> go.Figure:
    """
    Computes a graph showing the net charge of a given sequence per pH level.
        seq: Given sequence
    """
    ph_vals = np.arange(0.0, 14.0 + 0.1, 0.1)
    df = pd.DataFrame({"pH": ph_vals})
    df["Charge"] = df["pH"].apply(lambda ph: _charge_at_ph(seq, ph))
    fig = px.line(
        df,
        x="pH",
        y="Charge",
        title="Titration curve (charge vs. pH)",
    )
    fig.update_traces(line=dict(color=COLORS_BY_NAME["red"], width=3))
    fig.add_hline(y=0, line_dash="dash")

    min_charge = int(np.floor(df["Charge"].min()))
    max_charge = int(np.ceil(df["Charge"].max()))
    int_charges = np.arange(min_charge, max_charge + 1)

    points = []
    for i in int_charges:
        matched_charges = df[np.isclose(df["Charge"], i, rtol=0.01)]
        if not matched_charges.empty:
            median_ph = matched_charges["pH"].median()
            points.append((median_ph, i))
    if points:
        ph, charge = zip(*points)
        fig.add_trace(
            go.Scatter(
                x=ph,
                y=charge,
                mode="markers",
                marker=dict(size=8, color=COLORS_BY_NAME["blue"]),
                hovertemplate="pH=%{x:.1f}<br>Charge=%{y:.0f}<extra></extra>",
                showlegend=False,
            )
        )
    return fig


def _compare_features(
    df: pd.DataFrame,
    feature_a: str = "Sequence length",
    feature_b: str = "Molecular weight",
    group_by: str = None,
    intensity_threshold: float = None,
) -> go.Figure:
    """
    Creates a scatter plot to compare two features across a metadata aspect.
        df: Dataframe that contains the features
        group_by: Metadata aspect (e.g. Group, Batch, ...) that peptides get grouped by
        feature_a: Feature shown on x-axis
        feature_b: Feature shown on y-axis
        intensity_threshold: Peptides with intensities below this threshold are not included
    """
    if feature_a not in df.columns:
        raise ValueError(
            f"Feature {feature_a} could not be found in dataset. Please make sure to compute it first."
        )
    if feature_b not in df.columns:
        raise ValueError(
            f"Feature {feature_b} could not be found in dataset. Please make sure to compute it first."
        )
    peptides = df.copy()
    intensity_col = get_column_name(peptides, "intensity")
    if intensity_threshold is not None:
        peptides = peptides[peptides[intensity_col] > intensity_threshold]

    fig = px.scatter(
        peptides,
        x=feature_a,
        y=feature_b,
        color=group_by,
        color_discrete_sequence=COLORS,
        symbol=group_by,
        symbol_sequence=["square", "circle", "arrow-up", "star"],
        title=f"Comparison of peptide features across each {group_by}",
        hover_name="Sequence",
    )
    if feature_b == "GRAVY":
        fig.add_hline(y=0)
    fig.update_traces(marker=dict(size=10))
    return fig


def _compare_feature(
    df: pd.DataFrame,
    feature: str = "Sequence length",
    group_by: str = None,
    intensity_threshold: float = None,
) -> go.Figure:
    """
    Creates box plots for each group to compare a feature between metadata aspect.
        df: Dataframe that contains the features
        group_by: Metadata aspect (e.g. Group, Batch, ...) that peptides get grouped by
        feature: Feature to be compared
        intensity_threshold: Peptides with intensities below this threshold are not included
    """
    if feature not in df.columns:
        raise ValueError(
            f"Feature {feature} could not be found in dataset. Please make sure to compute it first."
        )
    peptides = df.copy()
    intensity_col = get_column_name(peptides, "intensity")
    if intensity_threshold is not None:
        peptides = peptides[peptides[intensity_col] > intensity_threshold]

    fig = px.box(
        peptides,
        x=group_by,
        y=feature,
        color=group_by,
        color_discrete_sequence=COLORS,
        title=f"Distribution of {feature} across each {group_by}",
        hover_name="Sequence",
    )
    return fig


def _raincloud(
    df: pd.DataFrame,
    group_by: str = "Group",
    feature: str = "Sequence length",
    log_scaled: bool = True,
) -> go.Figure:
    """
    Creates a raincloud plot (containing half violin, box and scatter) for displaying
    the intensity distribution as well as a chosen feature value.
        df: Dataframe that contains the features
        group_by: Metadata aspect (e.g. Group, Batch, ...) that peptides get grouped by
        feature: Feature to be shown in scatter plot
        log_scaled: If True, the x-axis uses a logarithmic (log10) transformation of the intensity data.
    """
    intensity_col = get_column_name(df, "intensity")
    if group_by == "Group" and group_by not in df.columns:
        df["Group"] = "None"

    groups = df[group_by].unique()

    # Sizes & spacings
    violin_width = 0.5
    violin_margin_bottom = -0.8
    violin_margin_top = 0.7
    box_width = 0.075
    violin_box_spacing = -0.043
    scatter_min = -0.3
    scatter_max = -0.1

    # Min & max used for unified color scaling
    min_feature_val = df[feature].min()
    max_feature_val = df[feature].max()
    colorscale = "Plasma"

    fig = make_subplots(
        rows=len(groups),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.025,
    )

    for i, group in enumerate(groups):
        peptides = df[(df[group_by] == group) & (df[intensity_col].notna())].copy()
        if log_scaled:
            intensities = np.log10(peptides[intensity_col])
        else:
            intensities = peptides[intensity_col]

        peptides["Color"] = peptides[feature].apply(
            lambda x: normalize_color(x, min_feature_val, max_feature_val, colorscale)
        )

        violin_y = np.zeros(len(intensities))
        box_y = np.full(len(intensities), violin_box_spacing)
        scatter_y = np.random.uniform(
            low=scatter_min, high=scatter_max, size=len(intensities)
        )

        violin = go.Violin(
            x=intensities,
            y=violin_y,
            orientation="h",
            side="positive",
            width=violin_width,
            box_visible=False,
            points=False,
            showlegend=False,
            fillcolor=COLORS_BY_NAME["lightgray"],
            line=dict(color=COLORS_BY_NAME["lightgray"]),
            hoverinfo="skip",
        )
        scatter = go.Scatter(
            x=intensities,
            y=scatter_y,
            mode="markers",
            marker=dict(size=5, color=peptides["Color"]),
            showlegend=False,
            text=peptides[feature],
            customdata=np.stack(
                [peptides[intensity_col], peptides["Sequence"]], axis=-1
            ),
            hovertemplate=(
                "Intensity=%{customdata[0]}<br>"
                f"{feature}=%{{text}}<br>"
                "Sequence=%{customdata[1]}<br>"
                f"{group_by}={group}<extra></extra>"
            ),
        )
        box = go.Box(
            x=intensities,
            y=box_y,
            orientation="h",
            whiskerwidth=0.5,
            width=box_width,
            boxpoints=False,
            showlegend=False,
            fillcolor=COLORS_BY_NAME["transparent"],
            line=dict(color=COLORS_BY_NAME["darkgray"]),
            hoverinfo="skip",
        )
        fig.add_trace(violin, row=i + 1, col=1)
        fig.add_trace(scatter, row=i + 1, col=1)
        fig.add_trace(box, row=i + 1, col=1)

        # Add title & set margins by y-range
        fig.update_yaxes(
            row=i + 1,
            col=1,
            title_text=group,
            range=[
                violin_width * violin_margin_bottom,
                violin_width * violin_margin_top,
            ],
            showticklabels=False,
            zeroline=False,
        )

    # Add invisible trace to show shared colorscale
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(
                colorscale=colorscale,
                cmin=min_feature_val,
                cmax=max_feature_val,
                showscale=True,
                size=0,
                color=[min_feature_val, max_feature_val],
                colorbar=dict(
                    title=feature,
                    outlinewidth=0,
                ),
            ),
            hoverinfo="none",
            showlegend=False,
        )
    )
    # Adjust x-axis ticks to log10
    if log_scaled:
        valid_logscaled = np.log10(df[intensity_col].dropna())
        min = int(np.floor(valid_logscaled.min()))
        max = int(np.ceil(valid_logscaled.max()))
        tickvals = list(range(min, max + 1))
        ticktext = [convert_exponential_to_suffix(t) for t in tickvals]
        fig.update_xaxes(
            row=len(groups),
            col=1,
            tickvals=tickvals,
            ticktext=ticktext,
        )

    # Show y-axis title only on last subplot
    fig.update_xaxes(
        row=len(groups),
        col=1,
        title_text="Intensity (log10)" if log_scaled else "Intensity",
    )
    fig.update_layout(title=f"Raincloud: Intensity and {feature} distribution")
    return fig


def _mann_whitney_u_test(
    df: pd.DataFrame,
    feature: str = "GRAVY",
    group_by: str = "Group",
    group_a: str = "",
    group_b: str = "",
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
    if not group_a or not group_b:
        all_groups = df[group_by].unique()
        if len(all_groups) < 2:
            raise ValueError(
                f"Not enough options for {group_by} in metadata, but 2 are required."
            )
        group_a, group_b = all_groups[:2]
        warnings.warn(
            f"{group_a} and {group_b} were selected for performing Mann-Whitney U test because at least one input was empty."
        )
        sub = df[[group_by, feature, "Sequence"]].copy()
    else:
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
    p = float(mw.pvalue)

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


@dataclass
class Plot:
    seq_based: bool
    method: Callable
    param_map: dict = None


PLOTS = {
    # Sequence-based
    "aa_distribution": Plot(
        True,
        _aa_distribution,
        {
            "aa_distribution_order_by": "order_by",
            "aa_distribution_show_all": "show_all",
        },
    ),
    "classification": Plot(
        True,
        _classification,
        {"classification_classify_by": "classify_by"},
    ),
    "hydropathy_profile": Plot(True, _hydropathy_profile),
    "titration_curve": Plot(True, _titration_curve),
    # Dataset-wide
    "compare_features": Plot(
        False,
        _compare_features,
        {
            "compare_features_a": "feature_a",
            "compare_features_b": "feature_b",
            "compare_features_group_by": "group_by",
            "compare_features_intensity_threshold": "intensity_threshold",
        },
    ),
    "compare_feature": Plot(
        False,
        _compare_feature,
        {
            "compare_feature_group_by": "group_by",
            "compare_feature_a": "feature",
            "compare_feature_intensity_threshold": "intensity_threshold",
        },
    ),
    "raincloud": Plot(
        False,
        _raincloud,
        {
            "raincloud_feature": "feature",
            "raincloud_group_by": "group_by",
        },
    ),
    "mann_whitney": Plot(
        False,
        _mann_whitney_u_test,
        {
            "mann_whitney_feature": "feature",
            "mann_whitney_group_by": "group_by",
            "mann_whitney_group_a": "group_a",
            "mann_whitney_group_b": "group_b",
            "mann_whitney_alternative": "alternative",
        },
    ),
}


def _generate_plots(seq: str, df: pd.DataFrame, params: dict) -> list:
    """
    Computes all selected plots on a given pandas DataFrame. Returns a tuple of lists, containing the peptide-specific plots and the plots describing the whole dataset.
    """
    seq_plots = []
    data_plots = []
    select_all = params.get("select_all")
    for key, plot in PLOTS.items():
        if params.get(key) or select_all:
            kwargs = (
                extract_related_kwargs(plot.param_map, params) if plot.param_map else {}
            )
            if plot.seq_based and seq is not None:
                kwargs["seq"] = seq
                seq_plots.append(plot.method(**kwargs))
            if not plot.seq_based and df is not None:
                kwargs["df"] = df
                data_plots.append(plot.method(**kwargs))
    return seq_plots, data_plots
