"""Toolkit for Erdos Problem #757 (Sidon subsets of (4,5)-sets).

Modules
-------
core        exact checks: AP edges, (4,5) property, weak Sidon, h(A) = alpha(H(A)), rigidity, realize()
saturated   midpoint maps: build a set from "which AP each interior point is the midpoint of"
fn_bounds   provable bounds on f(n) and the Henning-Yeo feasibility table for beating 4/7
chains      exact independence densities of periodic "chain" hypergraphs (transfer matrix)
realizability  exact (Fractions) order-feasibility / realizability oracle for labeled ordered AP patterns, with Farkas certificates and forced-relation cores
ordered_search plain-Python DFS over ordered midpoint patterns with float LP pruning (scipy) and exact leaf checks (small n only)
ordered_dfs    exact Python DFS over the abstract ordered-midpoint class O(n) (linear, midpoint-injective, K30, optional F7-freeness)
ordered_dfs_c  wrapper for the C port e757/c/ordered_dfs.c (build: bash e757/c/build.sh; needs gcc)
ordered_dfs_split  resumable prefix-split driver around the C DFS (drove the K45 and n=11 K43 censuses and the (14,11) run; validated on K41)
cpsat_model    OR-tools CP-SAT engine for class O' with lazy alpha/F7 cuts and realizability CEGAR (needs ortools)
cpsat_extra    CP-SAT wrapper adding the empirical invariants of sat_indep (UNSAT answers are conditional)
sat_indep      independent python-sat encoding of class O' with optional Gyarfas-Lehel colouring constraints (saturated case; needs python-sat)
anneal         hypergraph-first simulated annealing over (near-)saturated midpoint maps (needs numpy)

This package is yours to extend. The frozen, independent verifier is judge/judge.py (do not edit).
"""
