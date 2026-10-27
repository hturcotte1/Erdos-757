# KT (132 tau <= 27 n + 35 m + DEF) on C_3 for n <= 27: missing cells and closure

Unrefereed computation [verified-here as a computation]. 2026-10-27, folder experiments/20261027-0730-kt-cells. Spec: experiments/prover/panel-synthesis/SYNTHESIS.md section 5 step 2; statement and Theorem 7(ii): results/proofs/L021-i11-deficiency-route.md.

## Question
L021 Theorem 7(ii) verifies KT^{L*} on C_3 for n <= 24 (A = 27n+35m-132tau < 0 cells stored, 32 irreducible special pieces L*). Does it extend to n <= 27, and does any new irreducible special piece (A + DEF^proper < 0) appear?

## Method
1. Scan (scan2.py): all triples (n,m,tau), n <= 27, that a connected member of C_3 with A <= 15 can have (I11 s >= 0 for n <= 27 by L016, K8, connectivity, (P3)): 62 triples, 43 of them with A < 0. For KT only A < 0 matters (DEF >= 0, so A >= 0 gives P >= 0); A in [0,15] is computed as a bonus where a list exists.
2. Missing A<0 cells with n >= 25: (25,14,9,3), (26,17,10,3), (27,13,9,3), (27,20,11,3) recomputed here with the L012/L014/L016 streamed engine (src/ = copy of experiments/20261027-0340-induction-n28-n29-f25/src, md5 below; ext_d = L016 ext_d_fast) from refereed seed lists (see PROVENANCE.md); (26,13,9,3), (27,15,10,3), (27,16,10,3) (empty) reused from the 0340 folder.
3. Closure (closure2.py = L021 closure.py on the scan2 cell list): for every graph of every A<0 cell in increasing (n,m,tau), tau recomputed, DEF^proper over the pieces found so far (kt.deficiency of L021), P = A + DEF; P < 0 would be a new irreducible piece.
4. Independent checks of the only non-empty new cell and of unrefereed inputs: indep_27_13_9.py, validate_27_13_9.py, indep_small.py, indep_delta2.py.

## Commands (cwd = this folder)
- `bash run_cells.sh A 25,14,9,3 26,17,10,3 27,20,11,3` and `bash run_cells.sh B 27,13,9,3` (nice -n 15, NPROC=1, timeout 3 h per cell; raw rows progress_raw_{A,B}.tsv; logs out/ not committed)
- `python3 export.py` -> lists/*.txt, progress.tsv; `python3 deps_provenance.py` -> deps_provenance.json
- `python3 scan2.py 15 > scan2_15.txt`; `python3 closure2.py 15 > closure2_output.txt`; `python3 make_results.py` -> results.json
- `python3 indep_27_13_9.py`, `python3 validate_27_13_9.py`, `python3 indep_small.py`, `python3 indep_delta2.py 15 21 9`, `python3 indep_delta2.py 15 20 9` (outputs *_output.txt)
- code md5: engine.py a1924839..., stream.py 11c698cf..., decomp22.py b6a9ce4f..., ext_d c7019ef4..., filt cd178fbd..., canon da121753..., enum_conn 5a35810e... (identical to experiments/20261027-0340-induction-n28-n29-f25/checksums_code.txt)

## Results
New cells (lists/, progress.tsv; details and completeness argument in PROVENANCE.md):
| cell | classes | inputs | nodes | s |
|---|---|---|---|---|
| (25,14,9,3) | 0 | 661 | 4.96e7 | 60 |
| (26,17,10,3) | 0 | 11,558 | 6.55e8 | 621 |
| (27,13,9,3) | 18 | 232 | 1.95e7 | 1283 |
| (27,20,11,3) | 0 | 3,865 | 1.02e8 | 155 |
Reused empty: (26,13,9,3), (27,15,10,3), (27,16,10,3). Not computed (A >= 0, not needed for KT): (26,14,9,3) A=4, (26,18,10,3) A=12 [0340 worker running], (27,17,10,3) A=4, (27,21,11,3) A=12 (too expensive: ~1.7 core-hours central estimate, 20 high, and being computed elsewhere).

Closure (closure2_output.txt, results.json): see the final lines of closure2_output.txt.
- A < 0: 43 cells, 346 graphs in 13 non-empty cells (the 12 of L021 with 328 graphs, plus (27,13,9) with 18). Irreducible pieces: exactly the 32 of L*; NO new piece. All other A<0 graphs (296 old + 18 new = 314) have A + DEF = 0 exactly (equality cases); no graph with A + DEF < 0 outside L*.
- Hence KT^{L*} holds on every connected member of C_3 with n <= 27 (so on every member of C_3 with n <= 27 by additivity, L021 0.6) PROVIDED the stored lists are complete: it uses I11 for n <= 27 (L016, refereed), the refereed lists of L012-L016, and the new/reused cells above (unrefereed). A minimal counterexample to KT^{L*} therefore has n >= 28.
- New equality family: the 18 hypertrees of cell(27,13,9,3): 9 disjoint edges (blocks) plus 4 connectors, A = -4, DEF = 4 (9 E_1 minus 4 connectors: 144 - 140). Independently re-derived by structure (18/18 isomorphic to the engine list) and DEF re-checked by brute force (validate_27_13_9_output.txt, 0 mismatches).
- A in [0,15] (bonus): all stored cells give P >= A >= 0 (min P per cell in results.json); equality P = A is not informative.
- Non-refereed inputs re-derived independently: (5,3,1,3)=0, (8,4,2,3)=3, (11,5,3,3)=4 (indep_small); (24,15,9,2)=0 and (25,15,9,2)=2 (indep_delta2 via geng).

## Conclusion
No counterexample to Conjecture KT* and no new irreducible special piece for n <= 27. Theorem 7(ii) extends from n <= 24 to n <= 27 [verified-here, computation, unrefereed]; the only new non-empty cell, (27,13,9,3) (18 hypertrees), consists of equality cases. Caveats: the n >= 25 A<0 cells depend on unrefereed engine runs (three of them also reproduced by two other runs; (27,13,9,3) independently re-derived); A>=0 cells (26,14,9), (26,18,10), (27,17,10), (27,21,11) were not computed.
