# algorithms/hill_climbing.py
from typing import List, Optional, Tuple, Dict
import random
from utils import timeit, count_conflicts, random_state

def _neighbors(state: List[int]) -> List[List[int]]:
    """Generate neighbors by moving each queen in its column to any other row."""
    n = len(state)
    neigh = []
    for c in range(n):
        for r in range(n):
            if r != state[c]:
                ns = state.copy()
                ns[c] = r
                neigh.append(ns)
    return neigh

@timeit
def steepest_ascent(n: int, max_restarts: int = 50, max_steps_per_restart: int = 1000) -> Tuple[Optional[List[int]], Dict]:
    """
    Steepest-ascent hill climbing with random restarts.
    Returns (solution, info dict).
    Info fields: success (bool), restarts_used, steps_total, final_conflicts
    """
    restarts = 0
    steps_total = 0
    best_solution = None
    best_conf = float('inf')

    for restart in range(max_restarts):
        restarts += 1
        state = random_state(n)
        for step in range(max_steps_per_restart):
            steps_total += 1
            cur_conf = count_conflicts(state)
            if cur_conf == 0:
                return state, {'success': True, 'restarts_used': restarts-1, 'steps_total': steps_total, 'final_conflicts': 0}
            # Evaluate all neighbors and pick neighbor with minimal conflicts (steepest descent)
            neighbors = []
            n_best_conf = cur_conf
            n_best_state = None
            for c in range(n):
                for r in range(n):
                    if r == state[c]:
                        continue
                    tmp = state.copy()
                    tmp[c] = r
                    conf = count_conflicts(tmp)
                    if conf < n_best_conf:
                        n_best_conf = conf
                        n_best_state = tmp
            # If found better neighbor, move
            if n_best_state is not None:
                state = n_best_state
            else:
                # local maxima / plateau reached, break to restart
                break
        # track best found
        cf = count_conflicts(state)
        if cf < best_conf:
            best_conf = cf
            best_solution = state.copy()
    # no perfect solution found
    return best_solution, {'success': False, 'restarts_used': restarts, 'steps_total': steps_total, 'final_conflicts': best_conf}
