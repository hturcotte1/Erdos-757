# L023 work folder: f(25) = 15 (certificate results/proofs/L023-f25-equals-15.md)

Question: is there a 25-point (4,5)-set with h = 14 (a record, 14/25 < 4/7)? Answer: no (modulo the GAP of Step 2.7 of the
certificate: 7-17 unrefereed lists of the maximum-degree-3 subtree that were not recomputed here), and C25 (claim C007) has h = 15.
All runs: `nice -n 10`, one engine process (NPROC=1), `timeout` on every command; machine shared (load 11-14).
Tags: everything here is [verified-here] as an UNREFEREED computation unless stated.

## Files and what each shows
| file | command | shows |
|---|---|---|
| `arith23.py`, `arith23_output.txt` | `python3 arith23.py` | arithmetic of Theorem 1 (degree <= 4, tau(H-v) = 10), the top branches (S' = 2, 0), Corollary 5 thresholds |
| `tree.py` (L014's, unchanged), `tree_*.txt` | `CELLDIR=/tmp/nonexist ENGINELOG=/dev/null python3 tree.py 25 23 11 4` | dry runs: 172 keys for (25,23,11,4), sub-trees of the four top component cells |
| `provenance_tree.py`, `provenance_tree_D4_output.txt` | `python3 provenance_tree.py tree_25_23_11_4.txt` | per key: classes, first source, agreeing sources, SHA-256; 146 refereed, 26 unrefereed |
| `topcell/` (engine copy + the 11 component lists; archived in `topcell_cells.tar.gz`, sums in `topcell_cells_sha256.txt`) | `cd topcell && CELLDIR=$PWD/cells ENGINELOG=$PWD/engine.log WORKDIR=$PWD/work PROGRESS=$PWD/progress.jsonl NPROC=1 MD=10 python3 run_cells.py 25,23,11,4 25,23,11,3 > run_top.log` | top cells recomputed in a fresh directory: 6 and 0 classes, identical to the stored lists, identical counters |
| `decomp_bf.py`, `decomp_bf_output.txt` | `python3 decomp_bf.py $PWD/topcell/cells` | own brute force of the decompositions = engine.decompositions; inputs 15,429 + 67 |
| `topcell/gen_inputs.py` (L014's), `topcell/in_d3.txt`, `topcell/in_d4.txt` (not committed) | `CELLDIR=$PWD/cells python3 gen_inputs.py 25 23 11 4 inputs_25_23_11_4.txt inputs_25_23_11_4.tags` (in topcell/), then `head -15429` / `tail -67` | the inputs of the two branches |
| `topcell/noprune_d3.txt`, `topcell/noprune_d4.txt` (not committed) | `./bin/ext_d 24 10 11 3 2 noprune < in_d3.txt`, `./bin/ext_d 24 10 11 4 3 noprune < in_d4.txt` | all extensions with tau >= 11, no F7 pruning, no (P3) test: 2,928 and 15,032 |
| `classify_final.py`, `classify_final_d3_output.txt`, `classify_final_d4_output.txt` | `python3 classify_final.py topcell/noprune_d3.txt 3 topcell/cells/cell_25_23_11_D3.txt 10` (and `... noprune_d4.txt 4 ...D4.txt 20`) | own classification (verify_c.py): d=3: 0 members of C; d=4: the members of C reduce (networkx) to exactly the 6 stored classes |
| `ext_own.py`, `ext_own_d4_output.txt`, `ext_own_d3_sample_output.txt`, `ext_own_d3_sample.txt` | `python3 ext_own.py topcell/in_d4.txt topcell/noprune_d4.txt 24 10 4 0:67`; `python3 ext_own.py topcell/in_d3.txt topcell/noprune_d3.txt 24 10 3 0:0 ext_own_d3_sample.txt` | own extension enumerator (no code of ext_d) = ext_d noprune, input by input |
| `verify_c.py`, `verify_c_unit_tests_output.txt` | `python3 verify_c.py` | own membership verifier for C (linear, F7, (P3) by Lemma P = matchings, connected, tau) and its unit tests |
| `verify_six.py`, `verify_six_output.txt` | `python3 verify_six.py cell_25_23_11_D4.txt` | the 6 classes: in C, connected, tau = 11, Delta = 4, degree sequences, X - w types, tau(X - v) = 10, pairwise non-isomorphic |
| `cell_25_23_11_D4.txt` (copy, git-ignored name), `six_classes_25_23_11_D4.json` (tracked) | | the 6 classes |
| `repro4/seed_refereed.py`, `repro4/` | `cd repro4 && python3 seed_refereed.py && CELLDIR=$PWD/cells ... python3 run_cells.py 21,18,9,4 24,19,10,4` | the 8 unrefereed lists of the degree-4 subtree recomputed from the 247 refereed lists only |
| `compare_repro4.py`, `compare_repro4_output.txt` | `python3 compare_repro4.py` | 8 of 8 EQUAL to the stored lists |
| `repro3/`, `repro7/`, `compare_repro3_output.txt` | `cd repro3 && ... run_cells.py 21,19,9,3`; `cd repro7 && ... run_cells.py 5,3,1,3 8,4,2,3 11,5,3,3 21,11,7,3` | parts of the degree-3 subtree recomputed from refereed lists only (see the certificate, C9) |
| `realize_sdr.py`, `realize_sdr_25_23_11_D4_output.txt` | `python3 realize_sdr.py cell_25_23_11_D4.txt` | Theorem 3: all 325,400 injective midpoint labellings solved exactly; none gives a (4,5)-set |
| `count_sdr.py` | `python3 count_sdr.py cell_25_23_11_D4.txt` | the numbers of labellings |
| `ctl_realize.py`, `ctl_sets_output.txt` | `python3 ctl_realize.py sets` | positive controls: A_base and C006 realized, true labelling recovered |
| `ctl_json.py`, `ctl_14_12_6_output.txt` | `python3 ctl_json.py ../../20261027-0400-realize-21-18-9/results_ctl_14_12_6.json` | agreement with rexact on the 11 classes of cell(14,12,6,4), including the numbers of realizable labellings |
| `sub14.py`, `sub14_output.txt` | `python3 sub14.py` | every X_i contains a (14,12,6) piece of class 5 or 7 of cell(14,12,6,4), both NOT-REALIZABLE (second proof of Theorem 3) |
| `check_refereed_146.py`, `check_refereed_146_output.txt` | `python3 check_refereed_146.py` | the 146 refereed lists used by the run are identical to the refereed tarballs |
| `ext_own_d3_full_output.txt` | `VERBOSE=1 python3 ext_own.py topcell/in_d3.txt topcell/noprune_d3.txt 24 10 3 0:15429` | own extension enumerator on the degree-3 inputs, stopped after inputs 0-769 (770 EQUAL) |
| `posctl_24_20_10.py`, `posctl_24_20_10_output.txt` | `python3 posctl_24_20_10.py` | attempted positive control for cell(24,20,10,3) via X_i - v: vacuous (no X_i - v is connected with Delta <= 3) |
| `c25_construction.py`, `c25_construction_output.txt`, `c25_set.json` | `python3 c25_construction.py` | the witness C25: (4,5), 20 APs, tau = 10, h = 15 |
| `new_claim_c25_output.txt` | `python3 scripts/new_claim.py --slug c25-witness-f25 --set-file experiments/prover/L023/c25_set.json --notes ...` (repo root) | frozen judge: PASS NO-IMPROVEMENT, claim C007 |

Test: `python3 -m pytest -q tests/test_c25_witness.py` (3 passed).
