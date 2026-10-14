RESULT: NONE-FOUND

Statement tested: Lemmas 1, 2, 3 of kb/notes/gl_tight_structure.md (saturated, GL-tight, even n=2k, tau=k-1). Evidence only, not proof.
Scripts: lemmas.py (checker), run_main.py, run_own.py, lemma3.py; data: main_results.json, own_results.json, lemma3_results.json. All checks exact (integers; alpha via e757 exact B&B).

## Scope (Lemma 1 and 2, both G_L and G_R via reflection v -> n-1-v)
- Realizable records: A_base (n=14), 12-pt sets (rec 12, 12b, 12c, and the 2 omega KNOWN sets, duplicates of those), n=10 record: all saturated and GL-tight; all pass. n=8 record (m=5) and n=11 record are not saturated/even-saturated: lemmas not applicable (skipped, not counted).
- Abstract witnesses: 10 cells of witnesses.json (op+real; n=6,8,10) pass.
- Census n=12, m=10, alpha<=7: 14645 hypergraphs (file read at time of run; all saturated, GL-tight): pass.
- Own CP-SAT enumeration (enumerate_solutions, m=n-2, alpha<=n/2+1): 1000 at n=8, 1000 at n=10, 400 at n=12 (n=8 and 10 hit the limit, not full enumeration): pass.
- Lemma 2 instances checked: flipped case (t1-t0 in {0,1}, new tree, colouring equals predicted, both classes transversal, sizes >= k-1) over ~75000 flips in census alone, ~6500 flips in own data; non-flipped case (colouring unchanged) also ~120000+ instances; zero failures. Lemma 1: 0 failures in ~32000 tree checks.

## Lemma 3 (A_base, n=14, k=7)
- h(A-v)=8 for all 14 v: every vertex lies in a min transversal (tau(H-v)=5=k-2). Holds.
- No 12-point subset of A_base has h=7 (all 91 deletions have h=8), so the hypothesis of the pair statement holds, and every pair lies in a common minimum transversal. Holds.
- TEXT ERROR (not a counterexample to the conclusion): the lemma says tau(H-u-v)=k-2. The data give tau(H-u-v)=4=k-3 for all 91 pairs, as the proof requires (h(A-u-v)>=k+1 => tau = 2k-2-(k+1) = k-3; adding {u,v} gives k-1). Fix the statement to k-3.
