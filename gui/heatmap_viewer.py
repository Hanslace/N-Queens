# gui/heatmap_viewer.py
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from viz import heatmap_figure
import numpy as np

def show_heatmap_window(parent, conflict_matrix, title="Conflict heatmap"):
    top = tk.Toplevel(parent)
    top.title(title)
    fig = heatmap_figure(np.array(conflict_matrix), title=title)
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    top.geometry("520x560")
    return top
