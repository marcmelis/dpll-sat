# satsolver_practice
Simple COMPLETE SAT Solver.

## Solvers

```
python <solver_name> <formula_to_solve> *[<branching_heuristic>]
```
\**only for elcapo_sat.py*


Solvers list:
* solver_exp.py : experimental solver (too slow)
* original_dpll.py : base solver
* elcapo_sat.py : fast solver with more branching heuristics

### elcapo_sat branching heuristics
* **ZM** (Zabih McAllester) :
   counts the negative occurrences  -l of each given variable l.
* **FRE** (Freeman) : counts both the number of positive l and negative -l occurrences of a given variable l.
* **RAN** (Random) : random selection
* **MO** (Most often) : counts the occurrences of each l literal
* **JW** (Jeroslow Wang) : let C be the set of open clauses containing a single polarity of a given variable l. Then to the given variable l a weight of the summation of 2^(length of c) for each c ∈ C.
* **JW2S** (2 sided Jeroslow Wang) : Jeroslow Wang but C contains either polarity of a given variable.
* **SPC** (Shortest Positive Clause) : searches for the shortest clause with all literals positive.

## Formula generator


CNF formula generator, [DIMACS format].

```
python rnd_cnf_gen.py <num_vars> <num_clauses> <clauses_length> [<seed>] [ > file ]
```

## Solution validator

Validator for SATISFIABLE formulas, [DIMACS format]. 

```
python sat_val.py <formula> <solution>
```

[DIMACS format]: http://www.satcompetition.org/2004/format-solvers2004.html

## References

* An Overview of the MOMs Heuristics - http://www.cs.toronto.edu/~stefan/publications/classes/cse573/sat.ps
* Branching Rules for Satisfiability - http://repository.cmu.edu/cgi/viewcontent.cgi?article=1196&context=tepper 