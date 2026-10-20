# Referee round 3 of L014 (scratch folder)

Review: results/reviews/L014-f23-equals-14__referee__20261020T175733Z.md (VERDICT: ACCEPT).
Programs (all written for this review; no code shared with the prover, the judge or e757): ref_decomp.py (decompositions), ref_tree.py
(tree dry run), ref_gen_inputs.py (branch inputs from cell lists), refext.c (final step: all disjoint pair-triples, own cover
enumeration, explicit F7 embeddings and verified P3 violators), refext2.c (same with a complete restriction, graph6 output),
ref_g6filt.c (filter of genbg output), ref_found2g6.py (FOUND lines to graph6), ref_c23.py (witness), ref_misc_checks.py,
run_direct_genbg.sh, run_recursion_cell.sh. nauty 2.8.8 built unmodified in out/nauty/. Large outputs in out/ (git-ignored):
out/final (top cell, 133,804 inputs, 10,986 hits), out/c21, out/c19, out/c22 (sample), out/rc_17_14_7_3, out/rc_20_15_8_3,
out/genbg (86 direct cells + (14,12,6,3), (20,10,7,3), (20,11,7,3), (20,12,7,2)), out/ctrl (699 control classes), out/cells (the
prover's lists, checksums verified).
