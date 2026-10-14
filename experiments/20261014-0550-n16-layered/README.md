# n=16, T=9: layered decision by deletion of the maximum vertex

## Lemma (deletion of the maximum) [derived-here, validated computationally at N=9; N=12 check pending]
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

## Results
(see results/*progress.json, results/n16_m{13,14}_summary.json when they exist; filled in below by whoever reads them)
