import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import sample_colorscale

from pepsi.constants import (
    AA_WEIGHTS,
    COLORS,
    HYDROPATHY_INDICES,
    CHEMICAL_CLASS,
    CHARGE_CLASS,
    CHEMICAL_CLASS_PER_AA,
    CHARGE_CLASS_PER_AA,
)
from pepsi.features import _aa_frequency, _aa_classification, _charge_at_ph
from pepsi.utils import get_column_name


def _generate_plots(df: pd.DataFrame, seq: str, params: dict) -> list:
    """
    Computes all selected plots on a given pandas DataFrame.
    Returns a tuple of lists, containing the peptide-specific plots and the
    plots describing the whole dataset.
    """
    peptide_plots = []
    data_plots = []
    if seq is not None:
        if params["aa_distribution"]:
            plot = _aa_distribution(
                seq=seq,
                order_by=params["aa_distribution_order_by"],
                # Comparison with string necessary because form.cleaned_data only offers strings
                show_all=(params["aa_distribution_show_all"] == "True"),
            )
            peptide_plots.append(plot)
        if params["hydropathy_profile"]:
            plot = _hydropathy_profile(seq)
            peptide_plots.append(plot)
        if params["classification"]:
            plot = _classification(
                seq=seq,
                classify_by=params["classification_classify_by"],
            )
            peptide_plots.append(plot)
        if params["titration_curve"]:
            plot = _titration_curve(seq)
            peptide_plots.append(plot)
    if df is not None:
        if params["compare_features"]:
            plot = _compare_features(
                df=df,
                metadata=params["compare_features_metadata"],
                feature_a=params["compare_features_a"],
                feature_b=params["compare_features_b"],
                intensity_threshold=params["compare_features_intensity_threshold"],
            )
            data_plots.append(plot)
        if params["compare_feature"]:
            plot = _compare_feature(
                df=df,
                metadata=params["compare_feature_metadata"],
                feature=params["compare_feature_a"],
                intensity_threshold=params["compare_feature_intensity_threshold"],
            )
            data_plots.append(plot)
        if params["raincloud"]:
            plot = _raincloud(
                df=df,
                feature=params["raincloud_feature"],
                group_by=params["raincloud_group_by"],
            )
            data_plots.append(plot)
    return peptide_plots, data_plots


# Peptide-specific plots
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
    if not show_all:
        freq = {key: val for key, val in freq.items() if val > 0}
    if order_by in ["frequency", "alphabetical", "hydropathy", "weight"]:
        fig = px.bar(
            x=list(freq.keys()),
            y=list(freq.values()),
            labels={
                "x": "Amino Acid",
                "y": "Frequency",
            },
            color_discrete_sequence=COLORS,
        )
        if order_by == "frequency":
            fig.update_xaxes(categoryorder="total ascending")
        elif order_by == "alphabetical":
            fig.update_xaxes(categoryorder="category ascending")
        elif order_by == "hydropathy":
            sorted_aa = sorted(list(freq.keys()), key=lambda aa: HYDROPATHY_INDICES[aa])
            fig.update_xaxes(categoryorder="array", categoryarray=sorted_aa)
        elif order_by == "weight":
            sorted_aa = sorted(list(freq.keys()), key=lambda aa: AA_WEIGHTS[aa])
            fig.update_xaxes(categoryorder="array", categoryarray=sorted_aa)

    elif order_by in ["classes chemical", "classes charge"]:
        # Prepare dataframe
        df = pd.DataFrame(
            [
                {
                    "Amino Acid": aa,
                    "Frequency": count,
                }
                for aa, count in freq.items()
            ]
        )
        if order_by == "classes chemical":
            df["Class"] = df["Amino Acid"].map(CHEMICAL_CLASS_PER_AA)
            classes = list(CHEMICAL_CLASS.keys())
        elif order_by == "classes charge":
            df["Class"] = df["Amino Acid"].map(CHARGE_CLASS_PER_AA)
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
            class_df = df[df["Class"] == cls].sort_values("Amino Acid")
            fig.add_trace(
                go.Bar(
                    x=class_df["Amino Acid"],
                    y=class_df["Frequency"],
                    marker_color=CLASS_TO_COLOR[cls],
                    showlegend=False,
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
    fig.update_layout(title=f"Amino Acid Frequency of Sequence {seq}")
    fig.update_yaxes(tickmode="linear", tick0=0, dtick=1)
    return fig


def _hydropathy_profile(seq: str) -> go.Figure:
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


def _classification(seq: str, classify_by: str = "chemical") -> go.Figure:
    """
    Computes a bar plot showing the frequency of each amino acid class based on (Pommié et al., 2004).
        seq: Given sequence
        classify_by: Specification of how the amino acids should be classified, can be "chemical" or "charge".
    """
    classification = _aa_classification(seq, classify_by)
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
    fig.update_traces(
        showlegend=False,
    )
    return fig


# Dataset-specific plots
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
        color_discrete_sequence=COLORS,
    )
    fig.add_hline(y=0, line_dash="dash")
    return fig


def _compare_features(
    df: pd.DataFrame,
    feature_a: str,
    feature_b: str,
    metadata: str,
    intensity_threshold: float = None,
) -> go.Figure:
    """
    Creates a scatter plot to compare two features across a metadata aspect.
        df: Dataframe that contains the features
        metadata: Metadata aspect (e.g. Group, Batch, ...) that peptides get grouped by
        feature_a: Feature shown on x-axis
        feature_b: Feature shown on y-axis
        intensity_threshold: Peptides with intensities below this threshold are not included
    """
    peptides = df.copy()
    intensity_col = get_column_name(peptides, "intensity")
    seq_col = get_column_name(peptides, "sequence")
    if intensity_threshold is not None:
        peptides = peptides[peptides[intensity_col] > intensity_threshold]

    fig = px.scatter(
        peptides,
        x=feature_a,
        y=feature_b,
        color=metadata,
        color_discrete_sequence=COLORS,
        symbol=metadata,
        symbol_sequence=["square", "circle", "arrow-up", "star"],
        title=f"Comparison of peptide features across each {metadata}",
        hover_name=seq_col,
    )
    fig.update_traces(marker=dict(size=10))
    return fig


def _compare_feature(
    df: pd.DataFrame,
    feature: str,
    metadata: str,
    intensity_threshold: float = None,
) -> go.Figure:
    """
    Creates box plots for each group to compare a feature between metadata aspect.
        df: Dataframe that contains the features
        metadata: Metadata aspect (e.g. Group, Batch, ...) that peptides get grouped by
        feature: Feature to be compared
        intensity_threshold: Peptides with intensities below this threshold are not included
    """
    peptides = df.copy()
    intensity_col = get_column_name(peptides, "intensity")
    seq_col = get_column_name(peptides, "sequence")
    if intensity_threshold is not None:
        peptides = peptides[peptides[intensity_col] > intensity_threshold]

    fig = px.box(
        peptides,
        x=metadata,
        y=feature,
        color=metadata,
        color_discrete_sequence=COLORS,
        title=f"Distribution of {feature} across each {metadata}",
        hover_name=seq_col,
    )
    return fig


def _raincloud(df: pd.DataFrame, group_by: str, feature: str) -> go.Figure:
    """
    Creates a raincloud plot (containing half violin, box and scatter) for displaying
    the intensity distribution as well as a chosen feature value.
        df: Dataframe that contains the features
        group_by: Metadata aspect (e.g. Group, Batch, ...) that peptides get grouped by
        feature: Feature to be shown in scatter plot
    """
    intensity_col = get_column_name(df, "intensity")
    groups = df[group_by].unique()
    violin_width = 0.5
    box_width = 0.075

    fig = make_subplots(
        rows=len(groups),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.025,
    )

    # Set unified coloring for scatter plots across subplots
    min_feature_val = df[feature].min()
    max_feature_val = df[feature].max()
    color_norm = lambda x: (x - min_feature_val) / (max_feature_val - min_feature_val)
    colorscale = "Plasma"

    for i, group in enumerate(groups):
        peptides = df[(df[group_by] == group) & (df[intensity_col].notna())].copy()
        intensities = peptides[intensity_col]
        peptides["Color"] = peptides[feature].apply(
            lambda x: sample_colorscale(colorscale, color_norm(x))[0]
        )

        violin_y = np.zeros(len(intensities))
        box_y = np.full(len(intensities), -0.05)
        scatter_y = np.random.uniform(-0.3, -0.1, size=len(intensities))

        violin = go.Violin(
            x=intensities,
            y=violin_y,
            orientation="h",
            side="positive",
            width=violin_width,
            box_visible=False,
            points=False,
            showlegend=False,
            fillcolor=COLORS[7],
            line=dict(color=COLORS[7]),
        )
        scatter = go.Scatter(
            x=intensities,
            y=scatter_y,
            mode="markers",
            marker=dict(size=7, color=peptides["Color"]),
            showlegend=False,
            text=peptides[feature],
            hovertemplate=f"Intensity=%{{x}}<br>{feature}=%{{text}}<extra></extra>",
        )
        box = go.Box(
            x=intensities,
            y=box_y,
            orientation="h",
            whiskerwidth=0.5,
            width=box_width,
            boxpoints=False,
            showlegend=False,
            fillcolor="rgba(0,0,0,0)",  # Transparent
            line=dict(color=COLORS[7]),
        )
        fig.add_trace(violin, row=i + 1, col=1)
        fig.add_trace(scatter, row=i + 1, col=1)
        fig.add_trace(box, row=i + 1, col=1)

        # Add title & set margins by y-range
        fig.update_yaxes(
            row=i + 1,
            col=1,
            title_text=group,
            range=[violin_width * (-0.7), violin_width * 0.6],
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
                    len=0.45,
                    yanchor="top",
                    y=1.045,
                ),
            ),
            hoverinfo="none",
            showlegend=False,
        )
    )
    # Show y-axis title only on last subplot
    fig.update_xaxes(
        row=len(groups),
        col=1,
        title_text="Intensity",
    )
    fig.update_layout(title=f"Raincloud: Intensity and {feature} distribution")
    return fig
