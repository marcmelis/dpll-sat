#!/usr/bin/env python
'''
	SAT solver based on DPLL
	Course in Advanced Programming in Artificial Intelligence - UdL
'''

import random
import sys


def parse(filename):
    clauses = []
    for line in open(filename):
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            n_vars = line.split()[2]
            continue
        clause = [int(x) for x in line[:-2].split()]
        clauses.append(clause)
    return clauses, int(n_vars)


def bcp(formula, unit):
    modified = []
    for clause in formula:
        if unit in clause:
            continue
        if -unit in clause:
            new_clause = [x for x in clause if x != -unit]
            if not new_clause:
                return -1
            modified.append(new_clause)
        else:
            modified.append(clause)
    return modified


def get_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter


def get_jw_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 2 ** -len(clause)
            else:
                counter[literal] = 2 ** -len(clause)
    return counter


def pure_literal(formula):
    counter = get_counter(formula)
    assignment = []
    pures = []  # [ x for x,y in counter.items() if -x not in counter ]
    for literal, _ in counter.items():
        if -literal not in counter:
            pures.append(literal)
    for pure in pures:
        formula = bcp(formula, pure)
    assignment += pures
    return formula, assignment


def unit_propagation(formula):
    assignment = []
    unit_clauses = [c for c in formula if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0]
        formula = bcp(formula, unit[0])
        assignment += [unit[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        unit_clauses = [c for c in formula if len(c) == 1]
    return formula, assignment


def backtracking(formula, assignment, heuristic):
    formula, pure_assignment = pure_literal(formula)
    formula, unit_assignment = unit_propagation(formula)
    assignment = assignment + pure_assignment + unit_assignment
    if formula == - 1:
        return []
    if not formula:
        return assignment

    variable = heuristic(formula)
    solution = backtracking(bcp(formula, variable), assignment + [variable], heuristic)
    if not solution:
        solution = backtracking(bcp(formula, -variable), assignment + [-variable], heuristic)
    return solution


# Branching heuristics

def random_selection(formula):
    counter = get_counter(formula)
    return random.choice(counter.keys())


def jeroslow_wang(formula):
    counter = get_jw_counter(formula)
    return max(counter, key=counter.get)

def most_often(formula):
	counter = get_counter(formula)
    return max(counter, key=counter.get)


# Main

def main():

    if not len(sys.argv) == 2:
        sys.exit("Use: %s <cnf_file>" % sys.argv[0])

    clauses, n_vars = parse(sys.argv[1])

    solution = backtracking(clauses, [], JW)

    if solution:
        solution += [x for x in range(1, n_vars + 1) if x not in solution and -x not in solution]
        solution.sort(key=abs)
        print 's SATISFIABLE'
        print 'v ' + ' '.join([str(x) for x in solution]) + ' 0'
    else:
        print 's UNSATISFIABLE'


if __name__ == '__main__':
    JW = jeroslow_wang
    RAN = random_selection
    main()
