# experiments/benchmark.py
import time
import statistics
from algorithms.hill_climbing import steepest_ascent
from algorithms.csp_solver import csp_mrv_forward

def run_algo(func, n, runs, **kwargs):
    results = []
    for i in range(runs):
        sol, info = func(n, **kwargs) if kwargs else func(n)
        results.append((sol, info))
    return results

def summarize(results):
    runs = len(results)
    success = sum(1 for s,i in results if i.get('success'))
    runtimes = [i.get('runtime') for s,i in results if i.get('runtime') is not None]
    avg_runtime = statistics.mean(runtimes) if runtimes else 0
    avg_iter = statistics.mean([i.get('iterations') or i.get('nodes') or 0 for s,i in results]) if results else 0
    return {'success_rate': success / runs if runs>0 else 0, 'avg_runtime': avg_runtime, 'avg_iter': avg_iter, 'raw': results}

def run_all(n=8, runs=5):
    out = {}
    hill = run_algo(steepest_ascent, n, runs, max_restarts=30, max_steps_per_restart=1000)
    out['hill'] = summarize(hill)
    csp = run_algo(csp_mrv_forward, n, runs)
    out['csp'] = summarize(csp)
    # normalize keys for GUI
    return {'hill': out['hill'], 'csp': out['csp']}
