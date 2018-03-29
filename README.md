# satsolver_practice
Simple COMPLETE SAT Solver.

##Solvers

```
python <solver_name> <formula_to_solve>
```
Solvers list:
* solver_exp.py : experimental solver
* original_dpll.py : base solver

##Formula generator


CNF formula generator, [DIMACS format].

```
python rnd_cnf_gen.py <num_vars> <num_clauses> <clauses_length> [<seed>] [ > file ]
```

##Solution validator

Validator for SATISFIABLE formulas,[DIMACS format]. 

```
python sat_val.py <formula> <solution>
```

[DIMACS format]: http://www.satcompetition.org/2004/format-solvers2004.html