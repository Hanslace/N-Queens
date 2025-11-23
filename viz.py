# viz.py
from typing import List, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
import os

# Visual theme colors (burgundy and cream)
LIGHT = '#f3e7da'   # cream
DARK = '#8b1e1e'    # burgundy

def board_figure(state: List[int], title: Optional[str] = None, square_size: int = 40) -> plt.Figure:
    """
    Create and return a matplotlib Figure showing the board with queens.
    state: list of length N (state[col] = row)
    """
    n = len(state)
    fig, ax = plt.subplots(figsize=(6,6), dpi=100)
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks([])
    ax.set_yticks([])
    for r in range(n):
        for c in range(n):
            color = LIGHT if (r + c) % 2 == 0 else DARK
            rect = plt.Rectangle((c, n-1-r), 1, 1, facecolor=color, edgecolor='none')
            ax.add_patch(rect)
    for c, r in enumerate(state):
        ax.text(c + 0.5, n - 1 - r + 0.5, '♛', fontsize=24, ha='center', va='center')

    plt.tight_layout()
    return fig

def heatmap_figure(conflict_matrix, title: Optional[str] = None) -> plt.Figure:
    """
    conflict_matrix: 2D numpy array with conflict counts (shape NxN)
    """
    fig, ax = plt.subplots(figsize=(6,6), dpi=100)
    im = ax.imshow(conflict_matrix, cmap='Reds', origin='lower')
    ax.set_xticks([])
    ax.set_yticks([])
    if title:
        ax.set_title(title)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.set_ylabel('Conflict score')
    plt.tight_layout()
    return fig

def save_fig(fig: plt.Figure, path: str):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
