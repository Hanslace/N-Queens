# utils.py
import time
import random
from typing import List, Optional

def timeit(func):
    """Decorator to measure runtime and attach to info dict."""
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        t1 = time.perf_counter()
        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], dict):
            result[1]['runtime'] = t1 - t0
        else:
            result = (result, {'runtime': t1 - t0})
        return result
    return wrapper

def random_state(n: int) -> List[int]:
    """Return a random complete state for N-Queens: state[col] = row."""
    return [random.randrange(n) for _ in range(n)]

def count_conflicts(state: List[int]) -> int:
    """Count number of conflicting pairs in a complete state."""
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i+1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def conflicts_partial(assignment: List[int]) -> int:
    """Count conflicts among a partial assignment (columns 0..k-1)."""
    k = len(assignment)
    conflicts = 0
    for i in range(k):
        for j in range(i+1, k):
            if assignment[i] == assignment[j] or abs(assignment[i] - assignment[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def ensure_seed(seed: Optional[int]):
    if seed is not None:
        random.seed(seed)

