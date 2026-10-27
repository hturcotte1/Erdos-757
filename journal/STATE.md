# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: RUN 2026-10-27 (user, 02:17 UTC): 'continue with /goal and work non-stop until 4 pm MST tomorrow; try to find a significant result'. Target: a proof of c* >= 6/11 (I11 in general, goal clause B) or another significant result. Hard stop 2026-10-28 22:00 UTC (4 pm MDT); finalize (FINAL_REPORT section, STATE, tests, status, PR to main) by 21:30 UTC. GOAL.md protected; GOAL_MET YES already via clauses A (C003, a COMMUNITY construction: anonymous reader, Erdős Problem a Day, 19 Oct 2026, verified here, not ours; say so everywhere) and C.
Last updated (UTC): 2026-10-27 06:35
Clock: journal/START_TIME_UTC = 2026-10-13T23:06:40Z; budget 72 h exhausted long ago (status.sh takes 1 h+, re-judges C003-C005: run in background with timeout 14000 nice 19).

## Best verified results (details: results/LEDGER.md, kb/known_results.md K30-K63)
- Upper: c* <= 5/9 (L015, K60) and record sets 65/37 (C003, K59), 58/33 (C004, K62), 67/38 (C005, K63): the family and 5/9 are the reader's [community]; our part is the independent proof, the judging and the Lemma-E extensions. Lower: c* >= 9/17 [published], not improved.
- Exact f(n): n <= 18, 20, 22, 23, 24, 26, 27, 28 (f(16..23 even) = n/2+2, f(23) = 14, f(27) = 16; L008-L011, L014, L016). NEW 2026-10-27: f(21) = 12 RECORDED (K66; claim C006, a realized (21,19,9) class, judge PASS NO-IMPROVEMENT, ratio exactly 4/7; referee ACCEPT, scout CLEAR) [verified-here: set and h; derived-here: f(21) = 12]. Open: f(19) in {11,12}, f(25) = 15 BY COMPUTATION (06:30 UTC: all 6 classes of cell(25,23,11,4) NOT realizable, exact; certificate L023 in preparation; hence no (4,5)-set with <= 28 points beats 4/7, first open record size 29), f(29) in {16,17}.
- I11 (11 tau <= 3n + 2m) [conjecture] on class C: refereed for n <= 27 (L007-L016). Implies c* >= 6/11.

## This run (since 2026-10-27 02:17 UTC)
- L017 structure theorem for a minimal counterexample to I11 (connected, Delta = 3, s in {-1,-2}, Lemma U'', Hall lemma, 7 Hall-deficient patterns, degree-1/2 statements, Thm 6; Thm 7 = I11 for Delta <= 2 is KNOWN [published: HY EJC 24(2) P2.50 + Thm 14 or Chvatal-Hanson], re-proved). Round 1: referee opus NEEDS-WORK (4 editorial), referee fable ACCEPT WITH FIXES (5 editorial), scout KNOWN for Thm 7; no mathematical error; all fixes applied (9a1819e, b2e9c52). ACCEPTED x2 in round 2 (05:25/05:30 UTC): K64 (structure theorem), K65 (Delta <= 2, published, re-proved); LEDGER row L017 added.
- L017 Cor 13.3 (computation, unrefereed): I11 on C <= T'' + cell(25,23,11,3) empty, where T'' [conjecture]: every connected member of C with Delta <= 3 and slack <= 1 has <= 26 vertices (tight: <= 17). All data agree (stress test n = 28..40: every connected slack <= 1 graph with n >= 19 has Delta = 4).
- L018 (Conjecture RU; PARTIAL; Thm 4 non-locality; Thm 6(b'): H - v has at most TWO components; Thm 2 nu >= 2|E|/7 [published: Chvatal-Hanson, re-proved]): ACCEPTED (K67, 06:40 UTC): fable ACCEPT x2, opus ACCEPT after four editorial rounds; Cor 7.2 (I11 at n=28) stays conditional, Prop 8.2 unrefereed; RU and I11 remain open.
- L019 (Conjecture C1): PARTIAL (C1 not proved; GAP 1 s(F) = 1, GAP 2 s(F) = 0 closes under T3); proved: slack floor, gadget richness, pair-pair coverage (connected case), Thm 4 (C1 <=> no minimal counterexample has a degree-3 v with H - v connected), folding lemma (delete a degree-2 vertex, identify two neighbours: slack +1 exactly). Referees opus + fable + scout RUNNING (workflow verify-l019).
- L020 (joint induction I11 + T''; finiteness via coverage failures forcing low-slack subgraphs): prover RUNNING (due ~09:00). Panel workflow i11-proof-panel: L021 (HY deficiency route) and L022 (realizable class, order structure) provers RUNNING, then a judge synthesis (experiments/prover/panel-synthesis/SYNTHESIS.md).
- Conjecture T (connected tight => n <= 17) REFUTED at Delta = 4: cell(21,18,9,4) = 12 classes [verified-here]; T' (Delta <= 3) stands. All 12 (21,18,9) classes NOT realizable (exact, experiments/20261027-0400-realize-21-18-9) [verified-here as a computation]. Record cell (25,23,11) has >= 3 classes in C (Delta = 4, v + (3,1,1) + tight 21) [computation]; exact realizability pending.
- cell(25,23,11,3) = 0 [computation]: with L017 Cor. 13.3, I11 on C <= Conjecture T'' alone. cell(25,23,11,4) = 6 (all Delta = 4, two pendants each).
- I11 at n = 28 by computation: all n = 28 violator cells EMPTY (experiments/20261027-0340-induction-n28-n29-f25/progress.tsv; (27,20,11,3) = 0 in 20261027-0300-tight-cells-d4) [verified-here as a computation, unrefereed].
- Censuses: (Red)-free connected Delta <= 3 C-graphs n <= 14: only (3,1,1) (2,704,610 classes checked); richness data (Lemma U'' 0 exceptions; P2; C1) in experiments/20261027-0300-transversal-richness.

## Running jobs / agents (05:25 UTC)
- induction worker (experiments/20261027-0340-induction-n28-n29-f25): n = 28 done (all empty); now the dense chain for the record cell (25,23,11,4) [decides f(25): any realizable class = 25-point record; none = f(25) = 15] and n = 29 ((29,27,13,3) needs (28,24,12,3), (25,23,11,3)) [f(29) = 17 if I11 holds at 29]. Asked to publish lists/cell_21_19_9_D4.txt and lists/cell_25_23_11_D4.txt early.
- realize worker (experiments/20261027-0400-realize-21-18-9): (32,29,14) gluings; then the 3 (25,23,11) candidates, then cell (21,19,9) [decides f(21)].
- (Red) census n = 15 dense (nice 19); status run (background, timeout 14000); L017 round 2; L018 referees; L019 prover.

## Next actions
1. L017 (K64, K65) and L018 (K67) recorded; on L019 results: record or log.
2. When (21,19,9) and (25,23,11,4) lists exist and are tested: certificate for f(21) and for f(25) (or judge a record set via scripts/new_claim.py); when n = 29 cells are empty: certificate for I11 at n = 28, 29 and f(29) = 17 (prover 2 h, 3 referees).
3. Keep thinking about T'' (slack >= 2 for connected Delta <= 3 members of C with n >= 27): it is the single missing piece for I11 on C. By 21:30 UTC 10-28: FINAL_REPORT section for this run, tests, clean status, PR to main.
