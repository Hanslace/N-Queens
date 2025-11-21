# algorithms/a_star.py
from typing import List, Optional, Tuple, Dict
import heapq
from utils import timeit, conflicts_partial, count_conflicts

@timeit
def a_star(n: int) -> Tuple[Optional[List[int]], Dict]:
    """
    A* search over partial assignments.
    Node: tuple of rows for columns 0..k-1
    g = depth (k)
    h = number of attacking pairs among assigned queens (admissible)
    We prune immediate conflicts to control branching.
    """
    start = tuple()
    counter = 0
    open_heap = []
    # (f, g, h, counter, node)
    heapq.heappush(open_heap, (0, 0, 0, counter, start))
    counter += 1
    closed = set()
    iterations = 0
    nodes_expanded = 0

    while open_heap:
        f, g, h, _, node = heapq.heappop(open_heap)
        iterations += 1
        if node in closed:
            continue
        closed.add(node)
        nodes_expanded += 1
        k = len(node)
        if k == n:
            sol = list(node)
            if count_conflicts(sol) == 0:
                return sol, {'success': True, 'iterations': iterations, 'nodes_expanded': nodes_expanded}
            # otherwise continue
        col = k
        for row in range(n):
            # skip immediate conflicts with partial assignment
            conflict = False
            for c, r in enumerate(node):
                if r == row or abs(r - row) == abs(c - col):
                    conflict = True
                    break
            if conflict:
                continue
            child = tuple(list(node) + [row])
            child_g = g + 1
            child_h = conflicts_partial(list(child))
            child_f = child_g + child_h
            counter += 1
            if child not in closed:
                heapq.heappush(open_heap, (child_f, child_g, child_h, counter, child))
    return None, {'success': False, 'iterations': iterations, 'nodes_expanded': nodes_expanded}
