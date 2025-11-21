
---

## `report_template.md`
```markdown
# CS-323 AI CEP — N-Queens Project Report

**Group members:** Name(s)

**Assignment spec:** `/mnt/data/CS-323 AI CEP Problem Description and Instructions.pdf`

## 1. Problem Representation
- Variables: Columns 0..N-1
- Domains: Rows 0..N-1
- State: list `state[col] = row`
- Constraints: no two queens share same row or diagonal

## 2. Implemented Algorithms
- Hill Climbing (Steepest-Ascent) with Random Restarts (Local search)
- A* Search with heuristic h(n) = number of attacking pairs among assigned queens (Informed search)
- CSP Backtracking with MRV + Forward Checking (CSP)

## 3. GUI & Features
- Tkinter GUI with burgundy-and-cream board theme
- Algorithm panels, parameter inputs, run buttons
- Algorithm Comparison Dashboard (success rate, avg runtime, nodes)
- Conflict heatmap visualization
- Logging and example solution display

## 4. Experimental Setup
Describe N values, runs, seeds, and parameters.

## 5. Results
Insert charts, success rates, sample boards, heatmaps.

## 6. Discussion
Compare algorithms: completeness, runtime, typical node expansion, pros/cons.

## 7. Conclusion

## 8. Generative AI Declaration
We used ChatGPT to scaffold and generate code. Final testing and debugging completed by group.

