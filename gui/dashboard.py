# gui/dashboard.py
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def show_dashboard_frame(parent):
    frame = tk.Frame(parent)
    frame.pack(fill='both', expand=False, pady=6)
    fig = plt.Figure(figsize=(6,2.6), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title("Algorithm Comparison")
    ax.text(0.5, 0.5, "Run benchmark to see charts", ha='center', va='center')
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    # For later updates we will return fig and ax
    return frame, fig, ax, canvas
