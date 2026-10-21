# Lemma-E two-point extensions of the community family S_K (exact checks + judge)

Date 2026-10-21. Base family: the anonymous reader's S_K (O = {0,49,75,83,98,101,117,119,121,159,269}, phi(x) = 101 + 18x/269,
n = 11 + 9K, h = 7 + 5K) [community; erdosproblemaday.com day 757, certificate L015, C003 = K6]. The extension idea
(Lemma E, kb/notes/extension_lemmas.md [derived-here]) and every check below are this project's; the base family is the reader's.

## Question
Are min S_K and max S_K universal (in every maximum Sidon subset) for K = 3..6, and do the Lemma-E sets
S_K + {a - t, a + t} (a = min or max, generic t) beat 4/7 with fewer points than C003 (65 points)?

## Method (all arithmetic in Python ints)
- `lib.py`, `lib2.py`: exact tools. h and alpha(H - a) by the frontier DP of experiments/20261020-1730-reader-5-9/check_family.py
  (vertex order by copy index; correct for any order), on the AP hypergraph computed here from a sum dictionary.
- `step1.py` -> `step1_universality_dp.json`: h(S_K), alpha(H - min), alpha(H - max), K = 3..6.
- `step2.py` -> `step2_all_universal.json`: universality of EVERY vertex of S_K, K = 0..6.
- `step3.py` -> `step3.log`, `step3_results.json`, `set_*.json`: sets E1 = S_K + {min - t1, min + t1}, E2 = S_K + {max - t2, max + t2},
  E12 = both; t1 = 3*span + 1000003, t2 = 5*span + 7000027 (span = max - min of S_K; translation to min 0 only).
  Per set: own 4-subset test (all C(n,4) subsets, >= 5 distinct differences) and e757.core.is_45_set; AP count (own, e757) vs m(S_K) + number of
  new pairs; h by frontier DP; independent confirmation by CP-SAT on the AP hypergraph with the valid per-copy cuts (status OPTIMAL, obj = bound) and by
  python-sat/CaDiCaL on the DIRECT sum-collision encoding (>= h SAT with the model re-verified from the Sidon definition, >= h+1 UNSAT);
  universality of every vertex of the new set.
  (A first run with plain CP-SAT without cuts did not terminate for K = 4 within 10 minutes; it was killed and replaced by the cut version, as in the reader-5-9 folder.)
- `step4.py` -> `step4.log`: for S_K, E1, E12 (K = 4, 5, 6), the effect of the Remark-type extension (a, a+t, a+2t) at every vertex a (dh, dm, universal vertices afterwards).
- `step5.py` -> `step5.log`, `step5_results.json`: beam search (width 4, depth 8, score 7h - 4n) over iterated extensions from S_5 and E12(5) [heuristic].
- `make_results.py` -> `results.json`, `table.md`.

Commands (each under timeout and nice): `python3 step1.py; python3 step2.py; python3 step3.py; python3 step4.py; python3 step5.py; python3 make_results.py`.
Judge: `python3 scripts/new_claim.py --slug lemmaE-SK<k>-E1 --set-file claimset_E1_K<k>.json --notes '...'` (logs `claim_E1_K5.log`, `claim_E1_K6.log`).
Seeds: step4/step5 use random.seed(757) for t of the iterated extensions; step3 is deterministic.

## Results [verified-here]
1. Universality: for K = 3, 4, 5, 6, alpha(H - min) = alpha(H - max) = h - 1 (h = 22, 27, 32, 37), so min and max are universal. For K = 0..6 they are the ONLY universal vertices of S_K.
2. Table (n, m = number of 3-APs, h; every row passed own 4-subset test and e757.is_45_set, AP count = m(S_K) + number of pairs, CP-SAT OPTIMAL, SAT agrees):

| set | n | m (APs) | h (DP) | CP-SAT cuts | SAT (>=h, >=h+1) | h/n | 7h<4n | universal vertices after (indices) |
|---|---|---|---|---|---|---|---|---|
| E1_K3 | 40 | 37 | 23 (expected 23) | OPTIMAL 23/23 | True, False | 23/40 | False | [] |
| E2_K3 | 40 | 37 | 23 (expected 23) | OPTIMAL 23/23 | True, False | 23/40 | False | [] |
| E12_K3 | 42 | 38 | 25 (expected 24) | OPTIMAL 25/25 | True, False | 25/42 | False | [0, 1, 3, 6, 38, 40, 41] |
| E1_K4 | 49 | 46 | 28 (expected 28) | OPTIMAL 28/28 | True, False | 28/49 | False | [] |
| E2_K4 | 49 | 46 | 28 (expected 28) | OPTIMAL 28/28 | True, False | 28/49 | False | [] |
| E12_K4 | 51 | 47 | 30 (expected 29) | OPTIMAL 30/30 | True, False | 30/51 | False | [0, 1, 3, 6, 47, 49, 50] |
| E1_K5 | 58 | 55 | 33 (expected 33) | OPTIMAL 33/33 | True, False | 33/58 | True | [] |
| E2_K5 | 58 | 55 | 33 (expected 33) | OPTIMAL 33/33 | True, False | 33/58 | True | [] |
| E12_K5 | 60 | 56 | 35 (expected 34) | OPTIMAL 35/35 | True, False | 35/60 | False | [0, 1, 3, 6, 56, 58, 59] |
| E1_K6 | 67 | 64 | 38 (expected 38) | OPTIMAL 38/38 | True, False | 38/67 | True | [] |
| E2_K6 | 67 | 64 | 38 (expected 38) | OPTIMAL 38/38 | True, False | 38/67 | True | [] |
| E12_K6 | 69 | 65 | 40 (expected 39) | OPTIMAL 40/40 | True, False | 40/69 | False | [0, 1, 3, 6, 65, 67, 68] |


3. E1/E2 follow Lemma E exactly: (n + 2, h + 1), n = 13 + 9K, h = 8 + 5K; they beat 4/7 (7h < 4n) iff K >= 5 (K = 4 gives 28/49 = 4/7 exactly). Smallest n obtainable this way: 58 (K = 5).
4. E12 does NOT behave as the sequential use of Lemma E predicts. h(E12) = h(S_K) + 3 (not + 2): after E1 the old max is no longer universal, and E1 itself has no universal vertex at all (so the same side cannot be extended again, and neither can the new extremes). So the predicted 51-point (4) / 60-point (5) / 69-point (6) records with h = 29 / 34 / 39 do not exist; the actual h is 30 / 35 / 40.
5. Iteration [heuristic, step5]: after a non-universal extension (D = 17h - 9n rises by 16) a few universal vertices appear (4..7 in the depth-1 data of step4.log), each worth -1 in D and mostly destroying the others; the beam search from S_5 and E12(5) (width 4, depth 8, minimum score 7h - 4n) never got below the first step: best is E1(5) with score -1 (33/58); chains from E12(5) reached at best score 3 (37/64). Not exhaustive.

## Judge verdicts
Exact JUDGE lines (frozen judge via scripts/new_claim.py; K5 took 3 min, K6 69.6 min):

    JUDGE: PASS NEW-RECORD C004-lemmaE-SK5-E1 n=58 h=33 ratio=33/58 (0.568966) vs 4/7=0.571429
    JUDGE: PASS NEW-RECORD C005-lemmaE-SK6-E1 n=67 h=38 ratio=38/67 (0.567164) vs 4/7=0.571429

Claim files: results/claims/C004-lemmaE-SK5-E1.json, results/claims/C005-lemmaE-SK6-E1.json (a first K6 run was interrupted by my own pkill, its half-written claim file C005 was deleted and the judge re-run from scratch).

## Conclusion
Lemma E at the universal extreme points of S_5 gives a 58-point (4,5)-set with h = 33, 33/58 = 0.568966 < 4/7, verified exactly here and accepted by the frozen judge (the 58-point set is smaller than C003's 65 points and has a smaller ratio than C003's 37/65 = 0.569231). The predicted two-sided variants do not exist. Tags: family [community]; Lemma E [derived-here]; all checks above [verified-here]; the beam search [heuristic]. This is a judge PASS only; no referee review has been run on it.
