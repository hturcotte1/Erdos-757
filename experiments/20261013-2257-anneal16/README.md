# Track U1: hypergraph-first annealing over saturated midpoint maps, n=16 (h<=9) and n=18 (h<=10)

Question: is there a linear labeled midpoint map on 16 vertices (14 equations, or 13 plus one free vertex) whose
harmonic values form a (4,5)-set with h <= 9 (9/16 < 4/7)? Secondary: n=18, h <= 10 (10/18).

## Method (code: `e757/anneal.py`, driver `run.py`)
- State: midpoint map mid[j]=(i,k), boundary lo=0, hi=n-1, optionally one free vertex with a generic rational
  value; the labeled hypergraph is kept LINEAR by construction (moves: rewire a midpoint, replace an endpoint,
  swap two pairs, free-vertex transfer / value redraw; illegal moves rejected). [heuristic search]
- Cost = log2(1 + #independent (target+1)-sets of the intended hypergraph) + w * (#colliding pair-sums x+y, x<y) [w=1].
  The first term is 0 iff alpha <= target (smooth surrogate for alpha; plain alpha is a flat plateau).
  Collisions are weak-Sidon violations; an extra AP at a saturated midpoint always produces one, so
  "no collisions" means the AP hypergraph is exactly the intended one. Inner loop is float (numpy, tol 1e-9; all values are
  multiples of 1/det with det<~1e6 so distinct sums differ by >=1e-6). Floats decide nothing.
- Exact layer (`evaluate`, Fractions/integers): exact solve, actual APs via `ap_edges`, exact alpha (`alpha_of_edges`),
  exact (4,5) via `is45_ints` (numpy over all 4-subsets; tested equal to `core.is_45_set`). Run on every state with
  alpha(E)<=target and on a 1% sample of all other collision-free states. A hit (h*7 < 4n, exact) is sent to
  `scripts/new_claim.py` automatically (`on_hit`).
- Seeds: random linear maps (edge-by-edge propagation), and maps of A_base / 12-point records extended by random
  linear wiring of the extra vertices, plus a few random moves.
- Annealing: T 0.8 -> 0.15 geometric, 20000 steps per cycle, restart each cycle (50%: record-extension seeds).

## Commands
- Smoke test (3 min, 4 workers 16:0,16:1,16:0,18:0, seed0 5000): `python3 experiments/20261013-2257-anneal16/run.py --seconds 180 --every 60 --seed0 5000`
  (outputs in `smoke/`).
- Long run (6 h): `bash scripts/start_job.sh experiments/20261013-2257-anneal16 6 python3 experiments/20261013-2257-anneal16/run.py --seconds 21500 --configs 16:0,16:1,16:0,18:0 --seed0 1000 --every 180`
  Progress: `best.json` (merged every 3 min), `logs/ckpt_<k>.json`, `logs/worker_<k>.log` (5-min stats lines; HIT and JUDGE lines).

## Smoke-test results [verified-here for exact quantities, rates are wall-clock under 4-way load]
| worker | n | free | seed | states evaluated (180 s) | float collision-free | exact-verified (4,5) states | best exact h | best smooth cost (#indep (t+1)-sets) |
|---|---|---|---|---|---|---|---|---|
| 0 | 16 | 0 | 5000 | 121893 | 77884 | 747 (h: 10:436, 11:309, 12:2) | 10 | 2.81 (6) |
| 1 | 16 | 1 | 5001 | 20002 | 15645 | 173 | 10 | 4.52 (22) |
| 2 | 16 | 0 | 5002 | 123182 | 79008 | 829 (10:463, 11:364, 12:2) | 10 | 2.81 (6) |
| 3 | 18 | 0 | 5003 | 29152 | 19093 | 202 (11:21, 12:176, 13:5) | 11 | 5.52 (45) |
- Rate: ~680 states/s per worker at n=16 (free-vertex ~110/s in the 4-way run, ~1000/s alone), ~160/s at n=18.
- 2500 uniformly generated (edge-by-edge) random linear saturated maps at n=16: 519 (20.8%) are genuine exact
  (4,5)-sets with the intended hypergraph; float test and exact test agree on all 2500; alpha among them 10:96, 11:410, 12:13.
- Pure hypergraph annealing (no realizability), 40 s each: alpha never below 10 at n=16 (nfree 0 or 1); smooth cost best
  7 independent 10-sets (nfree 0). So alpha=9 is not even combinatorially reached yet; realizability is not the bottleneck so far.
- Best alpha seen at n=16: 10 (ratio 5/8). No hit.

## Incident (fixed)
Workers 0,1,2 crashed within ~5 min with `KeyError` in `FastEval.solve`: `Runner.initial` extended the unsaturated 11-point
record (m=8 < n-2) and the result had no equation for some vertex. Fix: only saturated seeds, `map_is_complete` check, test
`test_nfree1_path_runs`. Workers 0,1,2 were restarted in place (seeds 3000, 2000, 3002; logs `run_w*_restart.log`, same
`logs/ckpt_k.json`; `--no-merge`, `--k0`). Worker 3 (n=18) still runs the OLD code and may crash for the same reason; restart
it the same way (`--configs 18:0 --k0 3 --no-merge --seed0 3003`).

## Results of the long run [exact quantities verified-here; search statements heuristic]
Source: `best.json` (last merge 2026-10-14T00:01:03Z; journal/LOG.md entry 2026-10-14T00:50Z records that the four processes
were stopped after about 95 minutes because the machine was overloaded, so this was NOT the 6 h run requested in the command above).
Command actually launched: the long-run command above (4 workers, seeds 1000+, `--configs 16:0,16:1,16:0,18:0`); workers 0, 1, 2 were restarted
after the crash described under "Incident" with seeds 3000, 2000, 3002 (the `seed` fields of `best.json`).

| worker | n | free vertices | seed | states evaluated | float collision-free | exact (4,5)-sets reached | exact h distribution of those | best h | hits (h*7 < 4n) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 16 | 0 | 3000 | 931,228 | 595,575 | 5,810 | 10: 3,198; 11: 2,600; 12: 12 | 10 | 0 |
| 1 | 16 | 1 | 2000 | 2,132,767 | 1,685,562 | 16,853 | 10: 4,016; 11: 12,654; 12: 183 | 10 | 0 |
| 2 | 16 | 0 | 3002 | 928,286 | 592,873 | 5,926 | 10: 3,211; 11: 2,708; 12: 7 | 10 | 0 |
| 3 | 18 | 0 | 1003 | 511,813 (4,407 singular) | 324,047 | 3,196 | 11: 313; 12: 2,782; 13: 101 | 11 | 0 |

Totals at n = 16: 3,992,281 states, 28,589 genuine (4,5)-sets. `best_valid_by_ratio` in `best.json` is an n = 18 set with h = 11
(ratio 11/18 = 0.611). No state with alpha(E) <= 9 (n = 16) or <= 10 (n = 18) that is also a genuine (4,5)-set was reached.

## Conclusion
[heuristic] Pure hypergraph annealing over saturated midpoint maps found no 16-point set with h <= 9 and no 18-point set with
h <= 10 in about 95 minutes; the exact h of all genuine sets found was 10 to 12 at n = 16 and 11 to 13 at n = 18 (h = 9 at n = 16,
the value that would beat 4/7, was never reached). [verified-here] realizability is not the bottleneck (about 21% of random linear
saturated maps at n = 16 are exact (4,5)-sets, see the smoke-test section); alpha is. Superseded by the exact CP-SAT / DFS methods
(experiments/20261013-2257-chyp-table, experiments/20261014-0450-n16-cases, ...); recorded as dead end D16 in
kb/dead_ends.md. No K-row is based on this folder.
