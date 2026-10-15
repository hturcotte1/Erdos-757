# n=16, T=9: layered decision by deletion of the maximum vertex

## Question
Is there a class-O' ordered midpoint hypergraph on 16 vertices with alpha <= 9 (hence m in {13, 14}), i.e. a candidate for a 16-point (4,5)-set with
h <= 9 < 4*16/7? Method in one line: enumerate all 15-vertex structures with alpha <= 9 (layer 1) and extend them by a new maximum vertex (extension step),
using the deletion lemma below instead of a direct 16-vertex search. Tags: lemma [derived-here]; counts [verified-here]; interpretation [heuristic].

## Lemma (deletion of the maximum) [derived-here, validated computationally at N=9; the N=12 check was killed, see Results]
Let H be in the class O' (linear, midpoint-injective, F7-free, K30 monotone, K31 medial, forbidden cores with
<= 4 edges) on vertices 0..15 with m in {13,14} edges and alpha(H) <= 9.  Let d = deg(15).
* d >= 1: if d = 0 then alpha(H) = alpha(H-15)+1 >= c_hyp(15)+1 = 10 (c_hyp(15)=9, table in
  experiments/20261013-2257-chyp-table, modulo Henning-Yeo).
* H' = H - 15 is in O' on 15 vertices with m' = m-d edges and alpha(H') <= 9 (independent in H' => independent in H),
  so tau(H') >= 6 and Henning-Yeo gives m' >= 9; hence d <= 5 (d <= 4 for m = 13).
* The d edges at 15 are (i,j,15), i<j; their midpoints j are NOT midpoints of H' (injectivity) and lie in 1..14.
  H' has exactly 14-m' non-midpoints in 1..14 (13-m' interior ones plus the maximum 14).  For m = 14 all of them
  are used (d = 14-m'); for m = 13 all but one.
* Moreover the new edges must hit every independent T-set I of H' (I + {15} must contain an edge (i,j,15), i.e.
  both i,j in I); the extension step branches on such uncovered sets (hitting-set DFS), then re-checks everything
  on H exactly (alpha_of_edges, linearity, K30/K31, F7, cores<=4 via fast matcher e757.cpsat_model.satisfies_all).

## Scripts (all in this folder; PYTHONPATH handled by sys.path insert)
* layer1.py NP T MP TIME [LIMIT]  -- native CP-SAT enumeration (enumerate_all_solutions, 1 worker, eager alpha<=T,
  eager F7, K30, K31, cores<=4 edges, NO symmetry breaking: reflection would turn 'delete max' into 'delete min').
  Streams results/n{NP}_m{MP}_solutions.jsonl (flushed per solution) + n{NP}_m{MP}_progress.json
  (count, elapsed, rate, status RUNNING/EXHAUSTED/LIMIT/TIMEOUT).  Finished streams are skipped on relaunch;
  an unfinished stream restarts from scratch (CP-SAT cannot resume an enumeration).
* run_layer1.sh NP T "MP list" TIME PAR -- runs streams with at most PAR in parallel.
* extend.py N T M SHARD NSHARDS -- extension step (shardable by line number); finalize.py N M NSHARDS -- merge,
  dedupe under reflection, realize_exact, new_claim.py for sets with 7*alpha < 4*N.
* direct.py N T M TIME -- direct (non-layered) enumeration for cross-checks.
Tests: tests/test_cpsat_model.py (native enumeration vs brute force vs lazy loop; fast core matcher vs reference).

## Validation of the implementation
* N=9, T=6, M=7 [verified-here]: layered (layer1 on 8 vertices for m'=2..6, then extend.py) gives exactly the
  4394 solutions of the direct enumeration (set equality; all of them have deg(max) >= 1).  validation_n9/.
* N=12, T=7, M=10: `bash crosscheck12.sh` (layered vs direct; the three record 12-point patterns must appear);
  log logs/crosscheck12.log.   [status: see below]
* N=14 (requested): layer-1 streams on 13 vertices were started and ABORTED: at ~1-10 solutions/s (machine load 5) the
  m'=8,9 streams alone would take far more than the 3000 s cap; partial counts are in crosscheck_n14_aborted/.
  The enumeration rate of CP-SAT enumerate_all_solutions with ~1.5M clauses is only ~1-100 solutions/s, and the
  solution counts for mid m' are large, so the n=14 equality check was replaced by the N=9 (done) and N=12 checks.

## Production run (n=16)
Layer 1: `bash scripts/start_job.sh experiments/20261014-0550-n16-layered/prod 3 bash experiments/20261014-0550-n16-layered/run_layer1.sh 15 9 "9 10 11 12 13" 7200 3`
(started 06:00 UTC; 3 streams in parallel, 7200 s each; model build takes ~80 s per stream).  Stop rule: a stream with
> 2M solutions or TIMEOUT is not exhausted => the lemma route needs a second layer (vertex-0 deletion) for that m'.
Extension (after streams are EXHAUSTED):  python3 extend.py 16 9 14 S K (S=0..K-1), python3 extend.py 16 9 13 S K,
then finalize.py 16 14 K and finalize.py 16 13 K.

## Results (filled in 2026-10-15 from the files; `results/*_progress.json` and `*_solutions.jsonl` are git-ignored)
Production layer 1 (`prod/run.log`: `# started 2026-10-14T06:03:16Z max 3h`,
`# command: bash experiments/20261014-0550-n16-layered/run_layer1.sh 15 9 9 10 11 12 13 7200 3`), n = 15, T = 9, 7200 s per stream, build about 80 s:

| stream (n=15, T=9, m') | status | solutions found | rate |
|---|---|---|---|
| m' = 9  | TIMEOUT after 7200.1 s | 0 | 0 /s |
| m' = 10 | TIMEOUT after 7200.0 s | 0 | 0 /s |
| m' = 11 | TIMEOUT after 7200.3 s | 3,935 | 0.6 /s |
| m' = 12, 13 | never started (xargs queue killed, see the 06:25 update below) | | |

No `extend.py` / `finalize.py` run on n = 16 exists and no `results/n16_m*_summary.json` exists. The files `results/n11_m5_*` belong to a small
test stream (not described in the folder). Validation at N = 9 (`validation_n9/`): the direct enumeration `direct_n9_m7_progress.json` is EXHAUSTED with
4,394 solutions, and `n9_m7_ext_shard0.json` (layered route: 15,717 H' candidates, 46,215 candidate extensions) has `n_solutions` 4,394; layer-1 streams
for n = 8, m' = 2..6 are present. `crosscheck_n14_aborted/` holds the progress snapshots of the aborted N = 14 check (RUNNING when stopped:
n=14 m=12 direct 189 solutions at 220 s; n=13 m=7: 0 solutions at 17 s, m=8: 850 at 262 s, m=9: 2,016 at 244 s). The N = 12 cross-check was killed
(`logs/crosscheck12.log` has no result).

## Conclusion
[heuristic] The two streams m' = 9 and m' = 10 found no 15-vertex solution with alpha <= 9 in 2 hours each, but CP-SAT did not prove infeasibility, so the
degree consequence (deg(v) <= 3 for all v of a 16-vertex extremal H with m = 14) quoted in the update below is NOT established, and the layered route did not
decide n = 16. The deletion lemma is validated only at N = 9 (equality of the layered and direct solution counts, 4,394). Logged in journal/LOG.md entry
2026-10-14T08:10Z; dead end D19 in kb/dead_ends.md. No K-row depends on this folder.

## Update (06:25 UTC): redirect
* Streams m'=12 and m'=13 were cancelled (never started: the xargs queue was killed); m'=9, 10, 11 keep running to
  their 7200 s limit.  The N=12 layered cross-check (crosscheck12.sh) was killed (its first stream m'=5 gave no
  solution in 6 min); the extremal census (experiments/20261014-0610-extremal-census/) replaces it as the n=12/14 sanity data.
* Consequence to record IF m'=9 and m'=10 both finish EXHAUSTED with 0 solutions: apply the deletion lemma to any
  vertex v (H-v is in O' on 15 vertices with 14-deg(v) edges and alpha <= 9), then every 16-vertex extremal H
  with m=14 has deg(v) <= 3 for all v, so at least 10 vertices have degree exactly 3 (sum of degrees = 3m = 42; if a vertices have degree 3 and the rest <= 2 then
  3a + 2(16-a) >= 42, i.e. a >= 10).  NOT established (the streams ended in TIMEOUT, see Results); if
  CP-SAT cannot prove UNSAT within 2 h this is simply not available.
