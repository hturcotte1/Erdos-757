# Census invariants and a constrained n=16 search (Track U)

Question: which structural properties hold for ALL realizable extremal ordered midpoint patterns at n=12 (54,243) and
all known ones at n=14 (157), yet fail for some abstract-but-unrealizable pattern? Impose them on the n=16 search
(T=9, m=14, saturated).

## Data (all exact, [verified-here] counts)
- R12: 54,243 realizable (12,10,alpha<=7) patterns, `20261014-1005-census-dfs/results/realized_n12.json.gz` (edges in rank order).
- U12: 340,796 unrealizable patterns = rows of `n12_m10_filtered.txt.gz` with k31=1 and c4=1 (395,039, the O' class) minus both
  reflections of every R12 pattern. NOTE: U12 is the class O' (K30, K31, cores with <=4 edges, F7-free), i.e. it is already
  filtered by the cheap necessary conditions; the contrast is realizable vs "abstract O' but not realizable".
- R14: 157 realizable 14-point sets (`20261014-0610-extremal-census/results/n14_realizable_sets_partial.json`) turned into patterns by
  `e757.saturated.map_of_set`. This is a PARTIAL, CP-SAT-ordered sample (146 up to reflection), so it is biased.

## Part 1 statistics
Commands (repo root): `python3 experiments/20261014-1200-census-invariants/run_stats.py` (stats.py computes ~65 statistics per
pattern; writes a 230 MB pickle, deleted after use), then `python3 experiments/20261014-1200-census-invariants/analyze.py`.
Full per-statistic distribution tables (R12 / U12 / R14 counts per value): `tables.md`. Scan of value-set invariants: `invariants_scan.json`.
Statistics: degree sequence, max degree, deg of 0, 1, n-2, n-1, #vertices of degree 1..5, role (L/M/R count) multisets, max L/R role count,
M-only / L-only / R-only counts, spans k-i, G_L and G_R trees (depth, leaves, internal vertices, caterpillar, colour classes, max degree,
root degree), matching number nu, number of maximum independent sets (and size alpha-1), vertices in all/no maximum independent set,
reflection symmetry, edges meeting {0, n-1}, local counts (l(j)=j-1, r(j)=j+1, inversions of l and r, span-2 edges).
(The garbled item "edges containing both an endpoint of vertex 0's edges and ..." was not computed.)

Findings:
1. Realizable and unrealizable patterns are structurally almost indistinguishable by these statistics: every statistic takes the
   same values on both sets except for rare tail values. Tier counts (`tier_counts.json`): 
   - Tier 1 (below) holds for 54,243/54,243 R12, 157/157 R14, and 340,391/340,796 U12 (only 405 unrealizable patterns are excluded).
   - Tier 2 holds for 44,237/54,243 R12 (81.6%), 157/157 R14, 284,684/340,796 U12 (83.5%): no enrichment of realizable patterns.
2. Constant on all three sets (no discriminating power but true in 100% of the 395,196 patterns): max degree <= 4 (no degree 5), no reflection-symmetric
   pattern, colour classes of G_L, G_R are (k-1,k) (Lemma 1 of kb/notes/gl_tight_structure.md; n=12: (5,6), n=14: (6,7)), exactly one L-only and one R-only vertex
   (vertices 0 and n-1), no vertex lies in all or in no maximum independent set (n_in_all_MIS = n_in_no_MIS = 0), n_edges with midpoint in lower half = n/2-1 (trivial).
3. Discriminating universal value-set invariants (hold on all R12 and R14, fail for some U12 pattern), exact:
   - at most ONE vertex of degree 1 (R12: 0 or 1; R14: always 0; U12: 405 patterns have 2): excludes 405;
   - deg(0)+deg(n-1) >= 3 (excludes 12 unrealizable; R12 min is 3 although deg(0)=1 and deg(n-1)=1 each occur);
   - at most one midpoint-only vertex (n_Monly <= 1; implied by the degree-1 bound; 209 excluded);
   - others found by the scan (n_l_adj <= 7, inv_l <= 19, n_maxind in the R12 ranges, minspan <= 5, n_Mnodes_with_LR ...) are tail-value cutoffs of an
     n-dependent quantity: overfit, NOT used.
   There is no universal bound on nu (R12: 3,4; R14: always 4, n-dependent), on G_L / G_R depth (3..8 both), caterpillar-ness (both values occur), deg(0), deg(n-1) in {1..4}.
4. n=14-only features (true for all 157, false for many n=12 patterns): no vertex of degree 1, deg of 0, 1, n-2, n-1 all in [2,4], nu = 4, G_R depth >= 4.
   Because R14 is a biased partial sample these are heuristic only. At n=12, 10,006 of R12 have a degree-1 vertex (18%), none of the 157 n=14 sets do.
5. Mild enrichment (not an invariant): realizable patterns have more span-2 edges (i,i+1,i+2): fraction realizable is 0.07 at 0 such edges, 0.14 at 1, 0.24 at 2, 0.40 at 3 and 0.64 at 4 (tables.md, n_span2).

## Part 2: constraints
Hook: `e757/sat_indep.py` `Encoding(..., extra=dict)` / `decide(..., extra=)` / `enumerate_all(..., extra=)` (keys maxdeg, deg_ends, deg_near_ends,
ends_sum_min, n_deg1_max; reflection symmetric); CP-SAT wrapper `e757/cpsat_extra.py` (does not touch cpsat_model.py; same keys). Tests: `tests/test_extra_invariants.py`.
Tiers (`invariants.py`):
- **t1** = {maxdeg<=4, deg(0)+deg(n-1)>=3, at most one vertex of degree 1} + proved Gyarfas-Lehel colour balance (`gl_constraints='LR'`, SAT engine only; CP-SAT lacks it).
- **t2** (heuristic, sample-based) = {maxdeg<=4, no vertex of degree 1, deg(0),deg(n-1),deg(1),deg(n-2) in [2,4]} + GL colour balance (SAT engine).
Skipped as not simply expressible or not discriminating: matching number (cardinality over disjoint families), tree depth/caterpillar (no discrimination anyway),
m=13 (non-saturated: GL colouring and the degree-1 count do not apply; only m=14 was run).
Validation (`validate.py`, `validation.json`, `validate.log`): the n=10 record pattern and its reflection are consistent with t1 and t2 (forced-edge SAT, n=10,T=6,m=8);
(12,7,10) with t1: SAT (glucose4 1.8 s, CP-SAT 16 s); (14,8,12) with t1: SAT (glucose4 9 s, CP-SAT 520 s); (14,8,12) with t2: SAT (2 s / 137 s).
t2 is not validated at n=12 (it is false for 18% of R12 by design). I did not count all (10,8,T=6) solutions: enumerating that class with the lazy SAT loop did not finish in 10 min;
instead the record pattern was forced.

## n=16 runs (T=9, m=14), launched 2026-10-14 12:28 UTC, time_limit 3600 s each (wall), nice 5, machine loaded
`bash scripts/start_job.sh experiments/20261014-1200-census-invariants/n16/<engine>_<tier> 4 nice -n 5 python3 .../run_case.py <engine> 16 9 14 <tier> 3600`
for engine in glucose4, cadical153, cpsat and tier in t1, t2 (6 jobs). Result JSON line is the last line of `n16/<engine>_<tier>/run.log`
(status SAT / UNSAT / UNKNOWN(TIMEOUT), edges, exact alpha, realize_exact result, realized set if any).
Outcome: see the section "Outcomes" below (filled in by the orchestrator after the runs end, ~13:30 UTC).
A SAT answer must be run through `scripts/new_claim.py` if realized. UNSAT under t1 would be the conditional statement
"no 16-point O' extremal structure with maxdeg<=4, deg(0)+deg(n-1)>=3, <=1 vertex of degree 1"; UNSAT under t2 is a statement conditional on the
heuristic n=14 sample properties (not a theorem about f(16)).

## Outcomes (read 2026-10-14 14:25 UTC)
- (16, T=9, m=14) with tier-1 invariants (maxdeg<=4, deg(0)+deg(15)>=3, at most one degree-1 vertex) + G_L/G_R colour balance: CP-SAT UNKNOWN (3600 s), glucose4 TIMEOUT (3600 s), cadical153 still running at 14:25 and killed (uninterruptible in pysat; it had outrun its own limit).
- (16, T=9, m=14) with tier-2 invariants (maxdeg<=4, no degree-1 vertex, deg(0),deg(15) in [2,4], near-end degrees in [2,4]) + balance: CP-SAT UNKNOWN, glucose4 TIMEOUT, cadical153 killed.
- Conclusion [heuristic]: even with every universal invariant of the n=12 and n=14 censuses imposed, no engine finds a 16-vertex extremal structure or refutes one within an hour. The n=16 question stays open; Track U is closed for this run (dead end D15 extended).
