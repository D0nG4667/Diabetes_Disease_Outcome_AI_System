import re
import webp
import pandas as pd
import plotly.io as pio
from pathlib import Path
import plotly.express as px
from utils.paths import PLOTS
import plotly.graph_objects as go
from typing import Dict, Union, Optional, Iterable
from IPython.display import display, DisplayHandle

INTERACTIVE = False
SKIP = False

FORMAT = "webp"


def rename_legend(
    fig: go.Figure, mapping: Dict[Union[int, str], str] = {0: "No", 1: "Yes"}
) -> go.Figure:
    """
    Update the legend names of a Plotly figure.

    Parameters:
    - fig: Plotly Figure object
    - mapping: dict mapping original numeric/string labels to desired strings
    """
    fig.for_each_trace(
        lambda t: t.update(
            name=mapping.get(int(t.name) if str(t.name).isdigit() else t.name, t.name)
        )
    )
    return fig


def rename_xaxis(
    fig: go.Figure, mapping: Dict[Union[int, str], str] = {0: "No", 1: "Yes"}
) -> go.Figure:
    """
    Update the x-axis tick labels of a Plotly figure.

    Parameters:
    - fig: Plotly Figure object
    - mapping: dict mapping original numeric/string labels to desired strings
    """
    fig.update_xaxes(tickvals=list(mapping.keys()), ticktext=list(mapping.values()))
    return fig


def title_to_filename(title: str, save_dir: str | Path, ext: str = "webp") -> Path:
    """
    Convert a plot title into a safe, lowercase filename and return the full path.

    Parameters
    ----------
    title : str
        The title to convert into a filename.
    save_dir : str or Path
        Directory where the file will be saved.
    ext : str, default "png"
        File extension (without dot).

    Returns
    -------
    Path
        A Path object representing the full, sanitized file path.
    """
    # Normalize directory path
    save_dir = Path(save_dir)

    # Sanitize the title: keep alphanumeric, and underscores; replace others with underscore
    safe_name = re.sub(r"[^a-zA-Z0-9_]+", "_", title).strip("_").lower()

    # Construct the filename and return as a Path object
    return save_dir / f"{safe_name}.{ext}"


def show_plot(
    fig: go.Figure,
    save_only: bool = False,
    display_only: bool = False,
    save_dir: str | Path = PLOTS,
    interactive: bool = INTERACTIVE,
    skip: bool = SKIP,
) -> Optional[DisplayHandle | Path]:
    """
    Display a plot from either a saved image file or an interactive figure. All figures need a title to be able to create a filename

    Parameters:
    fig (Union[None, go.Figure]): The Plotly Figure object to display interactively. Default is None.
    save_only (bool): True saves the fig but do not render to display.
    display_only (bool): True displays or renders the fig from the saved plots and do not attempt to save it.
    save_dir (str | Path): Directory to save plots, defaults to PLOTS constant.
    interactive (bool): True displays and interactive plot without saving, defaults to INTERACTIVE constant.
    skip (bool): If True, skips both saving and displaying the plot. Default is False.

    Returns:
    Union[None, str]: Returns None if in interactive mode and the displayed image if in non-interactive mode.
    """
    if skip:
        return None

    title = fig.layout.title.text
    if title is None:
        raise ValueError("Fig must have a title")

    if interactive:  # Check if in interactive mode
        return fig.show()
    elif save_only:  # Save fig, no display
        filename = title_to_filename(title, save_dir)
        fig.write_image(filename, format=FORMAT, engine="auto", width=1280, scale=2)
        return filename
    elif display_only:  # Load fig from saved plots folder, no writing to save
        filename = title_to_filename(title, save_dir)
        img = webp.load_image(f"{filename}")  # Load image file
        return display(img)  # Display the image
    else:  # Save and Display
        filename = title_to_filename(title, save_dir)
        fig.write_image(filename, format=FORMAT, engine="auto", width=1280, scale=2)
        img = webp.load_image(f"{filename}")  # Load image file
        return display(img)  # Display the image


def show_plots(
    figs: Iterable[go.Figure],
    save_only: bool = False,
    display_only: bool = False,
    save_dir: str | Path = PLOTS,
    interactive: bool = INTERACTIVE,
    skip: bool = SKIP,
) -> Optional[list[Path]]:
    """
    Display or save multiple Plotly figures using write_images for stability.
    Mirrors show_plot semantics for collections.
    """

    figs = list(figs)

    if skip or not figs:
        return None

    # Interactive: just show all, no saving
    if interactive:
        for fig in figs:
            fig.show()
        return None

    files: list[Path] = []
    for fig in figs:
        title = fig.layout.title.text
        if title is None:
            raise ValueError("Each fig must have a title")
        files.append(title_to_filename(title, save_dir))

    # Save only
    if save_only:
        pio.write_images(fig=figs, file=files, format=FORMAT, width=1280, scale=2)
        return files

    # Display only (load from disk)
    if display_only:
        for f in files:
            img = webp.load_image(f)
            display(img)
        return files

    # Save + display
    pio.write_images(fig=figs, file=files, format=FORMAT, width=1280, scale=2)
    for f in files:
        img = webp.load_image(f)
        display(img)

    return files


def plot_cramers_bar_plotly(
    assoc_df: pd.DataFrame, title: str = "Association Strength with Target (Cramér's V)"
) -> go.Figure:
    """
    Create and return a Plotly horizontal bar Figure of Variable vs Cramér's V.
    Expects assoc_df with columns ['Variable','Cramer_V'].
    """
    df_sorted = assoc_df.sort_values("Cramer_V", ascending=True).reset_index(drop=True)
    fig = px.bar(
        df_sorted,
        x="Cramer_V",
        y="Variable",
        orientation="h",
        color="Cramer_V",
        color_continuous_scale="Reds",
        range_color=(0, 1),
        text="Cramer_V",  # show values on bars
        text_auto=".3f",  # format to 3 decimals
        title=title,
        height=max(600, 30 * df_sorted.shape[0]),
    )
    fig.update_layout(
        xaxis_title="Cramér's V", yaxis_title=None, title_x=0.5, showlegend=False
    )
    return fig


def plot_cramers_heatmap_plotly(
    mat: pd.DataFrame, title: str = "Cramér's V heatmap"
) -> go.Figure:
    """
    Create and return a Plotly heatmap Figure for a symmetric Cramér's V matrix.
    Rows and columns use mat.index/columns; values expected in 0..1.
    """
    labels_x = mat.columns.tolist()
    labels_y = mat.index.tolist()
    z = mat.values.astype(float)

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=labels_x,
            y=labels_y,
            colorscale="Reds",
            colorbar=dict(title="Cramér's V"),
            texttemplate="%{z:.3f}",
            hovertemplate="Variable X: %{y}<br>Variable Y: %{x}<br>Cramér's V: %{z:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=title,
        xaxis=dict(tickangle=45),
        height=max(600, 20 * len(labels_y)),
        width=max(900, 20 * len(labels_x)),
        margin=dict(l=200 if len(labels_y) > 30 else 120, r=120, t=80, b=120),
    )
    return fig
