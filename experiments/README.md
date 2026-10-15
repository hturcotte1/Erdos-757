# Experiments

One folder per experiment: `experiments/<YYYYMMDD-HHMM>-<slug>/` with:
- `README.md`: question, method, exact command, parameters and seeds, result, conclusion, tags;
- the scripts used (or a pointer to e757/ functions);
- outputs: small ones in the folder; large ones gzipped under data/.

Long runs: `bash scripts/start_job.sh experiments/<id> <max_hours> <command...>`, then
`bash scripts/jobs.sh` to monitor. `run.log` and `job.pid` are git-ignored, so summarize the
results in README.md.

Special folders:
- `experiments/referee/`: the referee's independent checks.
- `experiments/falsify/`: falsifier reports.

## Index of experiment folders (chronological by folder id)
Written 2026-10-15 from each folder's README. Tags are those of CLAUDE.md. "Feeds" gives the K-row of kb/known_results.md, certificate (results/proofs/L00x),
or dead end (kb/dead_ends.md) that cites the folder; "none" means no K-row or certificate cites it. Reminder: `run.log`, `job.pid` and some bulky outputs
(`*_progress.json`, `*_solutions.jsonl`, `n14/results/` of the census, ...) are git-ignored, see `.gitignore`; the READMEs quote the numbers that matter.

| id | question | outcome | tag | feeds |
|---|---|---|---|---|
| 20261013-2257-anneal16 | Can hypergraph-first annealing over saturated midpoint maps reach h <= 9 at n = 16 (h <= 10 at n = 18)? | About 4.0M states at n = 16, 28,589 genuine (4,5)-sets, best h = 10 (n = 18: best 11); never alpha <= 9; stopped after about 95 min | [heuristic] (exact h values [verified-here]) | D16 |
| 20261013-2257-chyp-table | What is the minimum independence number c_hyp(n) of ordered, linear, F7-free midpoint hypergraphs (abstract relaxation)? | c_hyp(n) = f(n) for n = 5..15 (n = 13..15 modulo Henning-Yeo); n = 16 run left no result | [verified-here] | K35-K36 (LEDGER) |
| 20261013-2257-forbidden-library | Which labeled ordered AP patterns on n <= 7 points are realizable by (4,5)-sets, and what are the minimal forbidden cores? | Census of 2, 5, 24, 189, 2364 patterns for n = 3..7 with 2, 5, 22, 142, 1312 realizable; 44 minimal cores; yields K30 (monotone midpoints) and K31 (no medial triangle); data/forbidden_ordered_n7.json | [verified-here] | K30, K31, K32 |
| 20261013-2257-paper-digest | What do Gyarfas-Lehel 1995 and Henning-Yeo (2017, 2018) say; sanity checks of the Fibonacci, F7, AG(2,3) facts | Digests in kb/notes; scripts re-verify Fibonacci tau = floor(2(n-1)/5), F7 / AG(2,3) HY violations, L(13) F7-free; HY 2021 full text not obtainable | [verified-here] scripts, [published] digests | none (background for K7-K10, K21) |
| 20261014-0005-forbidden-n8 | Extend the core library to n = 8; catalogue all connected linear configurations with <= 4 edges on <= 8 vertices | 46,281 ordered patterns at n = 8 = 16,568 R + 28,697 O + 498 E + 518 D; 243 new cores (287 total); 11 configurations, 145 labelings; independently recomputed (experiments/referee/catalogue-n8). Note: the Reproduction block uses `catalogue.json`, stored here as `catalogue.json.gz` | [verified-here] | K33; data/forbidden_ordered_n8.json |
| 20261014-0005-ordered-dfs | How fast is the ordered-midpoint DFS (Python vs C), and is a direct n = 16 enumeration conceivable? | C about 50x faster than Python; n = 12 in 58 s; n = 16 estimated at 6e13 to 1.2e14 calls (about 1e8 CPU-seconds), so not attempted directly | [verified-here] timings, [heuristic] estimate | none (engine used by L002-L004) |
| 20261014-0020-lp-fit | Which inequalities tau <= a n + b m + c.f hold on a large dataset of realizable AP hypergraphs; which configurations are Henning-Yeo near-tight? | Dataset consistent with tau <= 3n/7 (A_base the unique tight row for slope <= 0.4538); no row with D/n < 5/7; no feature-augmented inequality beats 3n/7 | [heuristic] fits, validity on rows [verified-here] | none |
| 20261014-0030-feasible-sizes | Does realizability-CEGAR find a record candidate at n = 18, 20, 22, 23, 25? | All 9 cases UNKNOWN (3600 s at n = 18, 20, 22; 1200 s each at n = 23, 25); no witness, no refutation | [heuristic] | K42 (cited), D18 |
| 20261014-0030-n16-decision | Does a class-O' hypergraph on 16 vertices with alpha <= 9 exist (CP-SAT, m = 13 and 14)? | No result: both runs died in the 04:40 UTC container restart (result files empty) | none | none (D15 is evidenced by other folders) |
| 20261014-0030-n16-decision-realizable | Same, via realizability-CEGAR | No result: killed by the container restart; folder has only run.log and job.pid | none | none |
| 20261014-0450-n16-cases | Resumable 30-case split of the n = 16, alpha <= 9 decision | 4 of 30 cases finished, all TIMEOUT at 3000 s; abandoned | [heuristic] | D15 |
| 20261014-0500-slack-landscape | Maximum tau (equivalently HY slack) per (n, m) in the abstract class O' and the realizable class, n <= 14 | Saturated O' cell: tau_max = n/2 - 1 and slack 11 - n/2 for even n = 6..14; realizable class equals O' in every resolved cell; cells (12,9), (13,11), (14,11) unresolved ranges | [verified-here] exact cells, [heuristic] ranges | K35, K36 |
| 20261014-0515-sat-indep | Independent pysat encoding of class O' for cross-checking certificates | Encoding validated by tests; GL colouring constraints speed up n = 12 by 3.5x to 14x; n = 16 single case TIMEOUT at 900 s | [verified-here], timings [heuristic] | K37, D15 |
| 20261014-0550-n16-layered | Decide n = 16 by enumerating 15-vertex structures (alpha <= 9) and extending by a maximum vertex | Streams m' = 9, 10: 0 solutions in 7200 s each (UNSAT not proved); m' = 11: 3,935 solutions (incomplete); lemma validated only at N = 9 | lemma [derived-here], counts [verified-here], interpretation [heuristic] | D19 |
| 20261014-0610-extremal-census | How many extremal ordered patterns exist at (12,10), (14,12), (15,13); how many are realizable? (CP-SAT, time-limited) | n = 12: 30,559 solutions, 4,448 realizable; n = 14: 1,474 solutions, 146 realizable; n = 15 left unfinished; all lower bounds, superseded by the exhaustive DFS | [verified-here] | K36, K40, K42 |
| 20261014-0640-abase-extensions | Does every 2-point extension of A_base that is a (4,5)-set have h = 10? | Yes: all such sets have h = 10 (exact case analysis plus independent brute force); upgraded K13 from [community] | [verified-here] | K13, L001 (ACCEPT after 4 referee rounds) |
| 20261014-0700-inductive-fit | Which constants (b, c, d) in a tau <= b\|R\| + c e_2 + d e_1 inequality are consistent with abstract versus realizable data? | Q8 = (3/7, 2/7, 4/7) is exactly the corner on realizable data; the abstract class O (cores <= 4 edges) forces b >= 31/70 at Q8's (c, d) | [verified-here] finite data, [heuristic] generalization | K39 |
| 20261014-1005-census-dfs | Exact counts of 12- and 14-point extremal sets by exhaustive C DFS | 54,243 twelve-point classes (m = 10; m = 9 has none); 2,910 saturated 14-point classes; (14, 11) case open, prefix-split DFS running | [verified-here] | K41/L002, K45/L004, D21 |
| 20261014-1200-census-invariants | Which structural invariants hold for all extremal patterns at n = 12, 14, and do they make n = 16 tractable? | Invariants do not separate realizable from unrealizable patterns; constrained (16, 9, 14) runs: CP-SAT UNKNOWN, glucose4 TIMEOUT (3600 s), cadical killed | statistics [verified-here], consequence [heuristic] | D20 |
| 20261014-1430-small-counts | Exact numbers of extremal (4,5)-sets for n = 6..13 up to affine equivalence | Saturated classes 1, 4, 66, 1,262, 6,644, 466,961 for n = 6..11; infinite non-saturated families for n = 6..11; n = 13 not computed | [verified-here] | K43/L003 |
| 20261015-2310-kb-audit | Is the documentation consistent with and complete relative to what the run established? | Findings listed in its README (priority list for the PI; evidence of K45/L004 in git-ignored directories; stale STATE.md; missing LEDGER rows) | [verified-here] file facts, [heuristic] recommendations | none |

Sub-indexes: `falsify/README.md` (falsifier reports), `referee/README.md` (referee scratch folders and verdicts).

