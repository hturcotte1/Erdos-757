## Problems found (in order of severity)

No mathematical or computational error was found. Remarks, all minor and editorial:

1. (Editorial) The branch $d=2$ of $(27,14,10,3)$ in Step 4.2 and C4 does not spell out the `ext_d` arguments; the engine (and C4's `ext_validate.py`) use $EP=d-1=1$ there (the deleted vertex has maximum degree $d$, so the two neighbours have $G$-degree $\le d-1$), not $EP=D-1=2$. With $EP=2$ my program finds 3 extensions with $\tau\ge10$ (all containing $F_7$, all disconnected, all with a degree-3 vertex, i.e. belonging to the $d=3$ branch); with the engine's $EP=1$ it finds 0, as stated. Nothing is wrong, but a reader checking C4 with the wrong $EP$ would be puzzled; one clause "(`ext_d 26 9 10 2 1`)" in 4.2 would remove the ambiguity.
2. (Editorial) `STATUS: submitted 2026-10-21 01:09 UTC`, but run G is dated 01:10 and the file's last modification is 01:20; the submission time should be the time of the final text.
3. (Editorial) 0.6 says "for an input with $P\le256$ the two builds perform the same operations": correct (the guard `P >= MAXP` fires only when a 257th pair is about to be stored), but the phrase "at most 256 admissible pairs" would be clearer than the inequality on the running counter.

## What was and was not recomputed by me

Recomputed independently (own code, no code from experiments/prover/L016 or the worker's folder; L012's refereed `canon` used only as an isomorphism oracle, nauty's `genbg`/`geng` as published generators): all arithmetic and decompositions; $C_{27}$; the input multisets of every branch of the five top cells and of the chain; the final step of all five top cells (including every extension with the required $\tau$ without pruning); the whole cell $(26,22,11,3)$ from its 229,369 inputs; six random chunks (150,000 inputs) of $(25,19,10,3)$; own filters on all 83,545 classes of the 51 new lists; own closure tests on $(23,13,8,3)$, $(25,19,10,3)$ and $(26,22,11,3)$; the sparse cells $(27,13,10,2)$ (genbg, no list used) and $(27,18,11,2)$ (dual cubic graphs, no list used); the two source diffs, Lemma B, and the regression of four `ext_d` builds on 5,789 inputs.

Not recomputed by me (time): the full cells $(24,16,9,3)$ (127,766 inputs) and $(25,19,10,3)$ (2,082,993 inputs; only 150,000 inputs and the closure test), the 45 run-A lists (only filtered and, for $(23,13,8,3)$, closure-tested), the 198 refereed seeds (refereed in L013/L014), and the sparse cells $(27,14,10,3)$, $(27,19,11,3)$ by genbg (see the genbg section for how far the generation got). For these I rely on the certificate's own cross-checks (identical lists and counters from the worker's independent Gosper-based run, which I confirmed for the four heavy lists as sets) and on Lemma B, which I audited and tested.

## Independence statement

I did not read any other review of L016 before writing this verdict. All programs in `experiments/referee/L016-round3/src/` were written by me for this review; they import nothing from `e757/`, `judge/`, `experiments/prover/L016/`, `experiments/prover/L014/` or the worker's folder. External tools: nauty 2.8.8 (`genbg30` built by the L013 round-3 referee with `-DMAXN1=30`, `geng`), L012's refereed `canon` (isomorphism oracle only), OR-tools CP-SAT (one of three independent computations of $h(C_{27})$), networkx (matching numbers of cubic graphs).
