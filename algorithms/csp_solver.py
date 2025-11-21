# algorithms/csp_solver.py
from typing import List, Optional, Tuple, Dict
import random
from utils import timeit

@timeit
def csp_mrv_forward(n: int, randomize: bool = False) -> Tuple[Optional[List[int]], Dict]:
    """
    CSP solver using MRV and forward checking.
    Returns (solution, info dict).
    info: success, iterations, nodes
    """
    if n <= 0:
        return [], {'success': True, 'iterations': 0, 'nodes': 0}
    domains = [list(range(n)) for _ in range(n)]
    assignment = {}
    iterations = 0
    nodes = 0

    def select_var(domains, assignment):
        unassigned = [c for c in range(n) if c not in assignment]
        if not unassigned:
            return None
        sorted_vars = sorted(unassigned, key=lambda v: len(domains[v]))
        return sorted_vars[0]

    def consistent(col, row):
        for c, r in assignment.items():
            if r == row or abs(r - row) == abs(c - col):
                return False
        return True

    def forward_check(domains, col, row):
        new_domains = [list(d) for d in domains]
        for c in range(n):
            if c == col or c in assignment:
                continue
            to_remove = []
            for r in new_domains[c]:
                if r == row or abs(r - row) == abs(c - col):
                    to_remove.append(r)
            for r in to_remove:
                new_domains[c].remove(r)
            if not new_domains[c]:
                return None
        return new_domains

    def order_values(vals):
        vals2 = list(vals)
        if randomize:
            random.shuffle(vals2)
        return vals2

    def backtrack(domains):
        nonlocal iterations, nodes
        nodes += 1
        iterations += 1
        if len(assignment) == n:
            return [assignment[i] for i in range(n)]
        var = select_var(domains, assignment)
        if var is None:
            return None
        for val in order_values(domains[var]):
            if consistent(var, val):
                assignment[var] = val
                new_domains = forward_check(domains, var, val)
                if new_domains is not None:
                    result = backtrack(new_domains)
                    if result is not None:
                        return result
                del assignment[var]
        return None

    solution = backtrack(domains)
    return solution, {'success': solution is not None, 'iterations': iterations, 'nodes': nodes}
