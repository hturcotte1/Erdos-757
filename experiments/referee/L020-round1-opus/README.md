# Referee L020, round 1 (opus): scratch folder

Independent code (no import of e757/, judge/ or experiments/prover/*; the prover's files are read only as data):
- `hg.py`: own 3-graph routines (linearity; F7 copies over all 5-edge subsets, two tests; (P3) exhaustively over all
  edge subsets with numpy and, separately, by an own Kuhn matching for every vertex pair; exact tau by own branch and
  bound and by OR-tools CP-SAT; enumeration of all minimum transversals; WL invariant; exact isomorphism backtracking).
- `t1_verify.py` (K29 parsed from the certificate text + all 45 classes), `iso_check.py` (pairwise non-isomorphism),
  `t1_roles_triples.py` (Theorem 1 (i)-(iii)), `glue_check.py` (rebuild of the 120 gluings / 45 classes),
  `k29_decomp.py`, `t3_check.py` (+`--deep`), `t3_perclass.py`, `t3_equiv.py`, `t3_equiv2.py` (Theorem 3),
  `theta_rebuild.py` (all Theta-gluings from (22,17,9,3)), `roles_check.py` (L017 C5 role facts on the 483 small near-tight graphs; Proposition 6), `cells_enum.py`
  (slack 0/1 cells), `t2_check.py` (Lemma 2.1, Theorem 2), `obs7_perclass.py` (Observation 7), `bf_classes.py`,
  `bcfg_slack2.py`. Outputs: `*_output*.txt`.
All runs: `nice -n 10`, one process, `timeout`.

Review written from `review_draft.md` to results/reviews/L020-joint-induction-i11__referee__<UTC>.md.
