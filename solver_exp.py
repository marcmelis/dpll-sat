#!/usr/bin/env python
'''
	SAT solver based on DPLL
	Course in Advanced Programming in Artificial Intelligence - UdL
'''

import sys, copy


class Formula(object):
    def __init__(self, n_vars, n_clauses):
        self.n_vars = int(n_vars)
        self.n_clauses = int(n_clauses)
        self.list = []
        # Initialize the linked list with every possible literal
        self.linked = [[] for _ in xrange(self.n_vars * 2)]
        self.assignment = []
        self.modifications = []
        self.empty = False
        self.contradiction = False

    def add_clause(self, clause):
        clause = clause
        self.list.append(clause)
        # Positive vars go from 0 to n_vars - 1
        # Negative vars go from n_vars to 2*n_vars - 1
        for var in xrange(self.n_vars):
            if var + 1 in clause:
                self.linked[var].append(clause)
            if -(var + 1) in clause:
                self.linked[var + self.n_vars].append(clause)

    def is_empty(self):
        return True if (len(self.list) == 0) else False

    def has_contradiction(self):
        return self.contradiction


def parse(filename):
    for line in open(filename):
        if line.startswith('c'): continue
        if line.startswith('p'):
            n_vars, n_clauses = line.split()[2:4]
            formula = Formula(n_vars, n_clauses)
            continue
        clause = [int(x) for x in line[:-2].split()]
        formula.add_clause(clause)
    return formula


def bcp(formula, unit):
    modified = Formula(formula.n_vars, formula.n_clauses)
    modified.assignment = copy.deepcopy(formula.assignment)
    for clause in formula.list:
        if unit in clause: continue
        if -unit in clause:
            new_clause = [x for x in clause if x != -unit]
            if len(new_clause) == 0:
                modified.contradiction = True
                return modified
            modified.add_clause(new_clause)
        else:
            modified.add_clause(clause)
    return modified


def pure_literal(formula):
    pures = []
    for literal in xrange(formula.n_vars):
        p_lit = len(formula.linked[literal])
        n_lit = len(formula.linked[literal + formula.n_vars])
        if p_lit == 0 and not 0 == n_lit:
            pures.append(literal)
        elif not p_lit == 0 and n_lit == 0:
            pures.append(-literal)
    for pure in pures:
        formula = bcp(formula, pure)
    formula.assignment += pures
    return formula


def unit_propagation(formula):
    unit_clauses = [c for c in formula.list if len(c) == 1]
    while len(unit_clauses) > 0:
        unit = unit_clauses[0]
        formula = bcp(formula, unit[0])
        formula.assignment.append(unit[0])
        if formula.has_contradiction() or not formula.list:
            return formula
        unit_clauses = [c for c in formula.list if len(c) == 1]
    return formula


def most_often_selection(formula):
    max = 0
    most_often_var = 1
    for var in xrange(formula.n_vars):
        n_positive = len(formula.linked[var])
        n_negative = len(formula.linked[var + formula.n_vars])
        if (n_positive + n_negative) > max:
            max = n_positive + n_negative
            # Var + 1 as the original vars start at 1
            most_often_var = var + 1
    return most_often_var


# wip
'''
def jeroslow_wang(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if abs(literal) in counter:
                counter[abs(literal)] += 2 ** len(clause)
            else:
                counter[abs(literal)] = 2 ** len(clause)
    least_often_value = max(counter.values())
    counter_list = counter.items()
    for item in counter_list:
        if item[1] <= least_often_value:
            least_often_key = item[0]
    return least_often_key
'''


def backtracking(formula, selection_function=most_often_selection):
    formula = pure_literal(formula)
    formula = unit_propagation(formula)

    if formula.has_contradiction():
        return None
    if formula.is_empty():
        return formula.assignment

    variable = selection_function(formula)
    new_formula = bcp(formula, variable)
    new_formula.assignment.append(variable)
    solution = backtracking(new_formula)

    if not solution:
        new_formula = bcp(formula, -variable)
        new_formula.assignment.append(-variable)
        solution = backtracking(new_formula)

    return solution


def main():
    formula = parse(sys.argv[1])
    solution = backtracking(formula)
    if solution:
        solution += [x for x in range(1, formula.n_vars + 1) if x not in solution and -x not in solution]
        solution.sort(key=lambda x: abs(x))
        print 's SATISFIABLE'
        print 'v ' + ' '.join([str(x) for x in solution]) + ' 0'
    else:
        print 's UNSATISFIABLE'


if __name__ == '__main__':
    main()
