# Computational verification for “Largest Sidon subsets in weak Sidon sets”

This repository contains the exact Python code used for the finite exhaustive verification
appearing in the paper

> Jie Ma and Quanyu Tang, *Largest Sidon subsets in weak Sidon sets*. (https://arxiv.org/abs/2602.23282)

The problem originates from Erdős Problems #757:
https://www.erdosproblems.com/757

It is also listed as constant 5b in the Optimization Problems constant database:
https://teorth.github.io/optimizationproblems/constants/5b.html

The base block verified by the script is
A_{base}={0,136,200,243,246,249,272,286,298,323,400,528,596,1056}.

## What the code does

The script verifies properties of the fixed base block A_{base}:

1. **(4,5)-property**: every 4-point subset of A_{base} determines at least five distinct
   pairwise absolute differences.

2. **Largest Sidon subset size**: it computes h(A_{base}), the maximum size of a Sidon subset
   of A_{base}, by exhaustive enumeration. The verified value is h(A_{base})=8,
   and the script prints an explicit witness Sidon subset of size 8.

The computation is deterministic and uses only exact integer arithmetic (no floating point).

## How to run

Requirements: Python 3.9+ (no external dependencies).

Run:
```bash
python verify_base_block.py
````

Or, on some systems:

```bash
python3 verify_base_block.py
```

## Example output

A typical successful run prints:

```text
|A_base| = 14
A_base is a (4,5)-set: YES
h(A_base) = 8
One maximum Sidon subset witness: [0, 136, 200, 243, 246, 298, 323, 528]
h(A_base)=8: VERIFIED
```
