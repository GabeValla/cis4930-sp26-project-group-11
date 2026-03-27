"""
functions.py - Helper functions for Tallahassee Crime Data Analysis
Bonus module demonstrating reusable, well-structured analysis utilities.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def ensure_dir(path):
    """Create directory (and parents) if it does not exist."""
    os.makedirs(path, exist_ok=True)


def save_fig(fig, save_path, dpi=300):
    """Save a figure, creating parent directories as needed."""
    if save_path:
        parent = os.path.dirname(os.path.abspath(save_path))
        ensure_dir(parent)
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight')


# ---------------------------------------------------------------------------
# Summary helpers
# ---------------------------------------------------------------------------

def summary_by_group(df, group_col, value_col, agg_funcs=('count', 'mean', 'median', 'std')):
    """
    Return a grouped summary DataFrame.

    Parameters
    ----------
    df         : pd.DataFrame
    group_col  : str | list  - column(s) to group by
    value_col  : str         - numeric column to aggregate
    agg_funcs  : tuple       - aggregation functions to apply

    Returns
    -------
    pd.DataFrame with one row per group
    """
    return (
        df.groupby(group_col)[value_col]
        .agg(list(agg_funcs))
        .reset_index()
    )


def top_n_by_group(df, group_col, n=10, ascending=False):
    """
    Return the top-n groups by count.

    Parameters
    ----------
    df        : pd.DataFrame
    group_col : str  - categorical column to count
    n         : int  - number of groups to return
    ascending : bool - sort order

    Returns
    -------
    pd.DataFrame with columns [group_col, 'count']
    """
    counts = df[group_col].value_counts(ascending=ascending).head(n).reset_index()
    counts.columns = [group_col, 'count']
    return counts


# ---------------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------------

def plot_hist(df, col, title, xlabel='Value', bins=30,
              color='#4C72B0', figsize=(8, 4), save_path=None):
    """
    Plot a styled histogram for a numeric column.

    Parameters
    ----------
    df        : pd.DataFrame
    col       : str   - column to plot
    title     : str   - plot title
    xlabel    : str   - x-axis label
    bins      : int   - number of bins
    color     : str   - bar color (hex or named)
    figsize   : tuple
    save_path : str | None - path to save figure at 300 dpi

    Returns
    -------
    fig, ax
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.hist(df[col].dropna(), bins=bins, color=color, edgecolor='white', linewidth=0.5)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    save_fig(fig, save_path)
    return fig, ax


def plot_bar(df, x_col, y_col, title, xlabel=None, ylabel='Count',
             palette=None, figsize=(10, 5), horizontal=False, save_path=None):
    """
    Plot a styled bar chart.

    Parameters
    ----------
    df         : pd.DataFrame
    x_col      : str        - categorical column
    y_col      : str        - numeric column (bar height / length)
    title      : str
    xlabel     : str | None
    ylabel     : str
    palette    : list | None - list of colors; defaults to seaborn Blues_r
    horizontal : bool        - if True, plot horizontal bars
    save_path  : str | None

    Returns
    -------
    fig, ax
    """
    colors = palette or sns.color_palette('Blues_r', len(df))
    fig, ax = plt.subplots(figsize=figsize)
    if horizontal:
        ax.barh(df[x_col], df[y_col], color=colors, edgecolor='white', linewidth=0.4)
        ax.set_xlabel(ylabel, fontsize=12)
        ax.set_ylabel(xlabel or x_col, fontsize=12)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    else:
        ax.bar(df[x_col], df[y_col], color=colors, edgecolor='white', linewidth=0.4)
        ax.set_xlabel(xlabel or x_col, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    save_fig(fig, save_path)
    return fig, ax


def plot_scatter(df, x_col, y_col, title, xlabel=None, ylabel=None,
                 hue=None, alpha=0.4, s=15, figsize=(8, 5), save_path=None):
    """
    Plot a scatter plot, optionally coloured by a categorical column.

    Parameters
    ----------
    df        : pd.DataFrame
    x_col     : str - x-axis numeric column
    y_col     : str - y-axis numeric column
    title     : str
    xlabel    : str | None
    ylabel    : str | None
    hue       : str | None - categorical column for colour grouping
    alpha     : float      - point transparency
    s         : int        - marker size
    figsize   : tuple
    save_path : str | None

    Returns
    -------
    fig, ax
    """
    fig, ax = plt.subplots(figsize=figsize)
    if hue:
        palette = sns.color_palette('tab10', df[hue].nunique())
        for idx, (label, group) in enumerate(df.groupby(hue)):
            ax.scatter(group[x_col], group[y_col], label=label,
                       alpha=alpha, s=s, color=palette[idx])
        ax.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    else:
        ax.scatter(df[x_col], df[y_col], alpha=alpha, s=s, color='#4C72B0')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    ax.set_xlabel(xlabel or x_col, fontsize=12)
    ax.set_ylabel(ylabel or y_col, fontsize=12)
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    save_fig(fig, save_path)
    return fig, ax