# gui/algorithm_panels.py
import tkinter as tk
from tkinter import ttk

def make_alg_panels(parent, callbacks):
    """
    Build collapsible-like panels in parent for algorithm parameters.
    callbacks: dict with keys 'run_hill', 'run_astar', 'run_csp', 'run_all'
    Returns dict of widgets for reading parameter values.
    """
    widgets = {}
    # Hill Climbing panel
    hill_frame = ttk.LabelFrame(parent, text="Hill Climbing (Steepest)", padding=6)
    hill_frame.pack(fill='x', pady=4)
    ttk.Label(hill_frame, text="Max restarts:").grid(row=0, column=0, sticky='w')
    widgets['hc_restarts'] = tk.IntVar(value=30)
    ttk.Entry(hill_frame, textvariable=widgets['hc_restarts'], width=8).grid(row=0, column=1, sticky='w', padx=6)
    ttk.Label(hill_frame, text="Steps per restart:").grid(row=1, column=0, sticky='w')
    widgets['hc_steps'] = tk.IntVar(value=1000)
    ttk.Entry(hill_frame, textvariable=widgets['hc_steps'], width=8).grid(row=1, column=1, sticky='w', padx=6)
    ttk.Button(hill_frame, text="Run Hill Climbing", command=callbacks.get('run_hill')).grid(row=2, column=0, columnspan=2, pady=6)


    # CSP panel
    csp_frame = ttk.LabelFrame(parent, text="CSP (MRV + Forward Checking)", padding=6)
    csp_frame.pack(fill='x', pady=4)
    widgets['csp_randomize'] = tk.BooleanVar(value=False)
    ttk.Checkbutton(csp_frame, text="Randomize value order", variable=widgets['csp_randomize']).grid(row=0, column=0, sticky='w')
    ttk.Button(csp_frame, text="Run CSP", command=callbacks.get('run_csp')).grid(row=1, column=0, pady=6)

    # Dashboard
    dash_frame = ttk.LabelFrame(parent, text="Dashboard", padding=6)
    dash_frame.pack(fill='x', pady=4)
    ttk.Label(dash_frame, text="Runs for benchmark:").grid(row=0, column=0, sticky='w')
    widgets['bench_runs'] = tk.IntVar(value=5)
    ttk.Entry(dash_frame, textvariable=widgets['bench_runs'], width=6).grid(row=0, column=1, sticky='w', padx=6)
    ttk.Button(dash_frame, text="Run Full Benchmark", command=callbacks.get('run_all')).grid(row=1, column=0, columnspan=2, pady=6)

    return widgets
