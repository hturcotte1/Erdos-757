# experiments/prover/L027: work folder of certificate L027 (Pattern (b) in I11 minimal counterexamples)

Certificate: results/proofs/L027-pattern-b-theorem.md (submitted 2026-10-27; unrefereed).

## Question
The certificate consolidates the proved parts of L025 and L026 (with the tight-set definition fixed to $|S|\ge3$) into one hand-proved reduction:
- the exact effect of the compression operations (Part A);
- every b-configuration of a near-tight connected graph is pendant, and the graph then has slack 1 (Theorem B);
- in a minimal counterexample to I11 on C, a pattern-(b) vertex is the centre of a pendant E1-hub over a connected slack-1 graph, with a rigid tight-set structure (Theorems P and C, Lemma Q);
- the pendant-triple lemma PT is equivalent to "no minimal counterexample has a pattern-(b) vertex" (Theorem D);
- the constraint J1 (Proposition J).

No proof step depends on a computation. The computations here only test the statements on data.

While L027 was being written, L028 (results/proofs/L028-pendant-triple-lemma.md, committed 865692a; unrefereed, under referee) claimed a proof of PT. L027 therefore:
- cites PT as claimed in L028 instead of stating it as an open GAP;
- quotes L028 Theorem 1 and Corollaries 2-4 verbatim (their proofs are not reproduced);
- adds Corollary D.3, conditional on L028 Theorem 1. In a minimal counterexample there is then no pattern-(b) vertex and no E1-hub, so every degree-3 vertex has pattern (a) or (f). This route does not use L025 or L026.

## Method
Everything is exact (Python integers and bitmasks). The scripts are our own code: `hyp27.py` (brute-force tau, minimum transversals, linearity, $F_7$, (P3), tight sets) and `census27.py`. They do not import e757/, judge/ or any L0xx code.

The exception is `run_s2_s3.sh`, which re-runs the panel judge's own checks unmodified: experiments/prover/e1hub-synthesis/checks/checks.py, modes S2 and S3.

All runs used one process, `nice -n 10` and `timeout`.

## Commands and results
1. **E1** (Part A identities, Lemma Q, Lemma A12 and the J1 / gadget formulas, on 3,000 random members of C with $n\le11$):
   ```
   cd experiments/prover/L027 && timeout 1800 nice -n 10 python3 lemmas27.py 1 3000 > lemmas27_output.txt
   ```
   Output: lemmas27_output.txt (counts per statement; run time in lemmas27_time.txt, 6 min 21 s). Result: 0 failures in 37 tested statements. The Lemma Q and A12(b)-(d) tests use a separate random stream, so the other counts are identical to those of the first full run.
   A first trial run stated the gadget range as $\{\tau''+3,\tau''+4\}$. It failed: $\tau''+2$ occurs when a minimum transversal meets all three pairs. The statement (Lemma A11) and the test were corrected before the proof was written.
2. **E2/E3** (judge's S2 and S3, re-run):
   ```
   bash experiments/prover/L027/run_s2_s3.sh
   ```
   Outputs: S2_rerun_output.txt and S3_rerun_output.txt, both identical to the judge's S2_output.txt and S3_output.txt.
   - S2: 0 pendant b-configurations in the ten stored near-tight lists with $\Delta\le3$ (483 classes).
   - S3: 0 candidate triples (A,B,C) and 0 hits in the stored slack-8 lists.
3. **E4** (pairwise non-co-transversal non-edge triples, no degree restriction, same ten lists):
   ```
   bash experiments/prover/L027/run_census27.sh
   ```
   Output: census27_output.txt. Result: 0 in every list.
4. **E5/E6** (sanity: the triangle (6,3,2) with its hub and fold; $A_{\rm base}$):
   ```
   cd experiments/prover/L027 && timeout 600 nice -n 10 python3 sanity27.py > sanity27_output.txt
   ```
   Results:
   - the hub of the triangle is (10,7,4) with s = 0, and its fold is (8,5,3) with s = 1;
   - $A_{\rm base}$ is (14,12,6), tight, in C, with 143 minimum transversals and 0 NC pairs.

## Conclusion
All tested statements hold on all tested configurations. The objects excluded by Theorems B, P and D do not occur in the stored data. The residual statement PT is untouched by these computations: they are tests, not proofs. PT is not proved in L027; it is claimed by L028 Theorem 1 (unrefereed, under referee), and L027 Corollary D.3 is conditional on it. L027 has no GAP of its own.
