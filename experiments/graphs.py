# experiments/graphs.py
import matplotlib.pyplot as plt
import os

def save_bar_comparison(algs, success_rates, runtimes, path="experiments/compare.png"):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    x = range(len(algs))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar([xi - width/2 for xi in x], success_rates, width=width, label='Success %')
    ax.bar([xi + width/2 for xi in x], runtimes, width=width, label='Avg runtime (s)')
    ax.set_xticks(list(x))
    ax.set_xticklabels(algs)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path
