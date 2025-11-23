# gui/interface.py
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from viz import board_figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from gui.algorithm_panels import make_alg_panels
from gui.dashboard import show_dashboard_frame
from gui.heatmap_viewer import show_heatmap_window
from utils import ensure_seed, count_conflicts
from algorithms.hill_climbing import steepest_ascent
from algorithms.a_star import a_star
from algorithms.csp_solver import csp_mrv_forward
import numpy as np
import experiments.graphs as graphs_mod

class AppUI:
    def __init__(self, root):
        self.root = root
        self.MAX_BOARD_SIZE = 800
        root.title("N-Queens AI — Hill Climbing | A* | CSP")
        root.geometry("1100x720")
        self._build()

    def _build(self):
        # top level frames
        left = ttk.Frame(self.root, width=720)
        left.pack(side='left', fill='both', expand=True, padx=8, pady=8)
        right = ttk.Frame(self.root, width=360)
        right.pack(side='right', fill='y', padx=8, pady=8)

        # Board area (left)
        board_lab = ttk.LabelFrame(left, text="Board", padding=6)
        board_lab.pack(fill='both', expand=True)
        self.board_container = ttk.Frame(board_lab)
        self.board_container.pack(fill='both', expand=True)
        # placeholder figure
        self.current_canvas = None

        # control row
        ctrl = ttk.Frame(left)
        ctrl.pack(fill='x', pady=6)
        ttk.Label(ctrl, text="N:").pack(side='left')
        self.n_var = tk.IntVar(value=8)
        ttk.Entry(ctrl, textvariable=self.n_var, width=6).pack(side='left', padx=6)
        ttk.Button(ctrl, text="Show Heatmap", command=self._on_heatmap).pack(side='left', padx=6)
        ttk.Button(ctrl, text="Clear board", command=self._clear_board).pack(side='left', padx=6)

        # right side algorithm panels
        cb_frame = ttk.Frame(right)
        cb_frame.pack(fill='y')
        callbacks = {
            'run_hill': self._run_hill_thread,
            'run_astar': self._run_astar_thread,
            'run_csp': self._run_csp_thread,
            'run_all': self._run_benchmark_thread
        }
        self.widgets = make_alg_panels(cb_frame, callbacks)

        # dashboard
        self.dash_frame, self.dash_fig, self.dash_ax, self.dash_canvas = show_dashboard_frame(right)

        # log area
        log_frame = ttk.LabelFrame(self.root, text="Log", padding=6)
        log_frame.pack(fill='x', padx=8, pady=(0,8))
        self.log_text = tk.Text(log_frame, height=6)
        self.log_text.pack(fill='x')

    def _log(self, text: str):
        self.log_text.insert('end', text + '\n')
        self.log_text.see('end')

    def _resize_board(self, event):
        """Keep board square AND limit maximum size."""
        if not self.current_canvas:
            return

        size = min(event.width, event.height, self.MAX_BOARD_SIZE)
        

        widget = self.current_canvas.get_tk_widget()
        widget.place(x=0, y=0, width=size, height=size)

    def _update_board(self, state, title=None):
        """Draw board but apply size limit."""
        if self.current_canvas:
            try:
                self.current_canvas.get_tk_widget().destroy()
            except:
                pass

        fig = board_figure(state, title=title)
        canvas = FigureCanvasTkAgg(fig, master=self.board_container)
        canvas.draw()

        self.current_canvas = canvas

        # Initial sizing (triggered before resize events)
        w = self.board_container.winfo_width()
        h = self.board_container.winfo_height()
        size = min(w, h, self.MAX_BOARD_SIZE)

        widget = canvas.get_tk_widget()
        widget.place(x=0, y=0, width=size, height=size)


    def _clear_board(self):
        if self.current_canvas:
            try:
                self.current_canvas.get_tk_widget().destroy()
            except Exception:
                pass

    def _on_heatmap(self):
        n = int(self.n_var.get())
        # compute conflict score for each square by sampling random placements
        # Simple approach: for each square (c,r), count conflicts when queen placed there and others random
        trials = 200
        conflict_matrix = np.zeros((n, n), dtype=float)
        for c in range(n):
            for r in range(n):
                score = 0
                for _ in range(trials):
                    # random assignment for other columns
                    state = [None] * n
                    state[c] = r
                    for cc in range(n):
                        if cc == c: continue
                        state[cc] = np.random.randint(0, n)
                    # count conflicts involving the queen at (c,r)
                    cnt = 0
                    for cc in range(n):
                        if cc == c: continue
                        if state[cc] == r or abs(state[cc] - r) == abs(cc - c):
                            cnt += 1
                    score += cnt
                conflict_matrix[r, c] = score / trials
        show_heatmap_window(self.root, conflict_matrix.tolist(), title=f"Conflict heatmap N={n}")

    def _run_hill_thread(self):
        t = Thread(target=self._run_hill)
        t.daemon = True
        t.start()

    def _run_astar_thread(self):
        t = Thread(target=self._run_astar)
        t.daemon = True
        t.start()

    def _run_csp_thread(self):
        t = Thread(target=self._run_csp)
        t.daemon = True
        t.start()

    def _run_benchmark_thread(self):
        t = Thread(target=self._run_benchmark)
        t.daemon = True
        t.start()

    def _run_hill(self):
        n = int(self.n_var.get())
        restarts = int(self.widgets['hc_restarts'].get())
        steps = int(self.widgets['hc_steps'].get())
        self._log(f"Running Hill Climbing: N={n} restarts={restarts} steps={steps}")
        sol, info = steepest_ascent(n, max_restarts=restarts, max_steps_per_restart=steps)
        self._log(f"Hill result: success={info.get('success')} restarts={info.get('restarts_used')} steps={info.get('steps_total')} final_conflicts={info.get('final_conflicts')}")
        if sol:
            self._update_board(sol, title=f"Hill result (conflicts={info.get('final_conflicts')})")

    def _run_astar(self):
        n = int(self.n_var.get())
        self._log(f"Running A*: N={n}")
        sol, info = a_star(n)
        self._log(f"A* result: success={info.get('success')} iterations={info.get('iterations')} nodes={info.get('nodes_expanded')}")
        if sol:
            self._update_board(sol, title=f"A* result (conflicts=0)")

    def _run_csp(self):
        n = int(self.n_var.get())
        randomize = bool(self.widgets['csp_randomize'].get())
        self._log(f"Running CSP: N={n} randomize={randomize}")
        sol, info = csp_mrv_forward(n, randomize=randomize)
        self._log(f"CSP result: success={info.get('success')} iterations={info.get('iterations')} nodes={info.get('nodes')}")
        if sol:
            self._update_board(sol, title=f"CSP result (conflicts=0)")

    def _run_benchmark(self):
        n = int(self.n_var.get())
        runs = int(self.widgets['bench_runs'].get())
        self._log(f"Running full benchmark: N={n} runs={runs}")
        import experiments.benchmark as bench
        results = bench.run_all(n=n, runs=runs)
        # results: dict with keys 'hill','astar','csp'
        self._log("Benchmark complete. Updating dashboard...")
        # update dashboard plots
        fig = self.dash_fig
        fig.clear()

        ax1 = fig.add_subplot(111)

        algs = ['Hill', 'A*', 'CSP']
        success = [
            results['hill']['success_rate'] * 100,
            results['astar']['success_rate'] * 100,
            results['csp']['success_rate'] * 100
        ]
        runtimes = [
            results['hill']['avg_runtime'],
            results['astar']['avg_runtime'],
            results['csp']['avg_runtime']
        ]

        x = np.arange(len(algs))
        width = 0.35

        # Success bars
        bars1 = ax1.bar(x - width/2, success, width, color="tab:blue")
        ax1.set_ylabel("Success %")
        ax1.set_xticks(x)
        ax1.set_xticklabels(algs)

        # Runtime bars (2nd axis)
        ax2 = ax1.twinx()
        bars2 = ax2.bar(x + width/2, runtimes, width, color="tab:orange")
        ax2.set_ylabel("Avg runtime (s)")

        # Single unified legend
        ax1.legend(
            [bars1[0], bars2[0]],
            ["Success %", "Avg runtime (s)"],
            loc="upper right"
        )

        self.dash_canvas.draw()

        self._log("Dashboard updated. You can save graphs from experiments/graphs.py")
