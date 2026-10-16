# Knowledge-base audit against the run's results (2026-10-15 23:10 UTC)

**Question.** Is the documentation (kb/, README.md, data/README.md, results/) consistent with, and complete relative to, what the run actually established?
**Method.** Read results/FINAL_REPORT.md, results/LEDGER.md, kb/known_results.md (all rows), journal/LOG.md (whole file), kb/00_START_HERE.md, kb/open_questions.md, kb/dead_ends.md, kb/ideas_backlog.md, kb/RESEARCH_PLAN.md, README.md, data/README.md; checked every path cited in kb/known_results.md, results/LEDGER.md, results/FINAL_REPORT.md, kb/dead_ends.md, kb/open_questions.md, kb/ideas_backlog.md and kb/00_START_HERE.md with a glob script (python3, `re` + `glob`, no heavy computation); checked git-tracking with `git ls-files` / `git check-ignore -v`; recounted the 2,910 classes (see Edits made).
**Command (path check).** Script inline in the session: extract every `(experiments|results|data|kb|tests|e757|journal|scripts)/...` token from each file, `glob.glob` it. Output: one miss (K43, a relative path), see (c).
**Result.** Findings below; edits made are listed in "Edits made". Tags: [verified-here] for file-existence and git-tracking facts and counts, [derived-here] for arithmetic, [heuristic] for recommendations. Nothing in kb/00_START_HERE.md, kb/known_results.md, results/*, STATE.md or .gitignore was edited; those are proposals for the principal investigator (PI).
**Conclusion.** The mathematical content of FINAL_REPORT/LEDGER/known_results is mutually consistent. The gaps are (1) key evidence for K45/L004 sits in a git-ignored directory and was not on GitHub, (2) START_HERE and STATE.md predate most of the run, (3) LEDGER omits six K-rows and has a broken table, (4) two overstated sentences in FINAL_REPORT.

## Priority list for the PI (read this first)
1. **[verified-here] K45/L004 evidence is git-ignored.** `.gitignore` line `experiments/20261014-1005-census-dfs/n14/results/` hides `post/summary.json`, `post/real_*.json.gz` (the 2,910 realized classes, 136 KB), `post/filter_counts.json`, `post/judge_spotcheck.txt` and `n14_m12_TOTAL.json`, all cited by K45 and by results/proofs/L004. A fresh clone of the repo cannot check certificate L004. Mitigation done: tracked copies in `data/census_n14_m12_classes.jsonl.gz` and `data/census_n14_m12_summary.json` (see Edits made). Proposal: replace the ignore line by `experiments/20261014-1005-census-dfs/n14/results/n14_m12_prefix_*` (keep the 23 MB of per-prefix files out, or allow them, total directory 23 MB < 50 MB) and un-ignore `.../n14/results/post/` and `n14_m12_TOTAL.json`; also change the evidence cell of K45 to the tracked data/ files.
2. **[verified-here] the relaunch command for the running (14,11) DFS is only in a git-ignored log** (`experiments/**/run.log` is ignored, and FINAL_REPORT section 4 says "relaunch with the command in its run.log"). The command is: `python3 -m e757.ordered_dfs_split 14 8 11 3 4 experiments/20261014-1005-census-dfs/n14m11dfs/results --refl --nice 10 --tag n14_m11` (from n14m11dfs/run.log; 3,437 depth-3 prefixes, started 2026-10-15T22:57Z, 67 prefixes marked done at 23:08). Put it in experiments/20261014-1005-census-dfs/README.md and FINAL_REPORT section 4.
3. **journal/STATE.md is stale** [verified-here]: it still says the n=14 census runs at 1691/2537 prefixes and "finish ~16:30 UTC 10-15", and that the next action is postprocess/L004. In fact the enumeration finished 16:42, L004 was ACCEPTED 23:00, and the running job is the (14,11) DFS (LOG 20:45Z, 23:00Z; LEDGER row K45/L004). Also "Budget end 2026-10-16 23:06 UTC" matches GOAL (72 h from 2026-10-13T23:06:40Z) [derived-here].
4. **Two overstatements in results/FINAL_REPORT.md** [verified-here against LOG and the scout file]:
   - Section 2: "no witness at n=18,20,22,23,25 in one-hour realizability-CEGAR searches". LOG 2026-10-14T13:25Z: n=18, 20, 22 ran 3600 s each; n=23 (m=19,20,21) and n=25 (m=21,22,23) ran 1200 s each. Replacement: "no witness at n=18, 20, 22 (3600 s each), n=23 and n=25 (1200 s each), all UNKNOWN".
   - R5 last sentence: "A novelty scan found none of these in the literature or the problem's forum threads." The only scout file is results/reviews/L002-census-12-point-extremal-sets__scout__20261014T171802Z.md, which covers L002, L003, K30, K31, searched OEIS, the erdosproblems forum thread and the repo digests, and says its absence-from-digests conclusion "does not exclude an implicit use in" the papers. It did not cover K44 (degree bound), K33 (medial 4-cycle), L001 or L004. Replacement: "A novelty scan of 2026-10-14 (OEIS, erdosproblems forum thread, repo digests; Ma-Tang and Gyarfas-Lehel not re-read in full) found K30 and K31 absent; K33 and K44 were not scanned."
5. **results/LEDGER.md** has a blank line between the `chains` row and the `K30-K31` row, which splits the markdown table in two (rows from K30 on render as plain text), and it has no rows for K37, K38, K39, K40, K42, K44 (all [verified-here] or [derived-here] in known_results.md). Proposed rows are in (b).
6. **K43 evidence cell** says `experiments/20261014-1430-small-counts/README.md, results/summary.json`; the second path is relative and does not exist from the repo root. Replacement: `experiments/20261014-1430-small-counts/README.md, experiments/20261014-1430-small-counts/results/summary.json` (the file exists).

## (a) Outdated or answered statements
### kb/open_questions.md (EDITED directly: a Status column was added to every row, Q4 closed, Q11 and Q12 added)
| Row | Old status | New status | Evidence |
|---|---|---|---|
| Q1 | open | undecided; no alpha<=9 pattern found by any method; no certificate reachable | D15, D16; experiments/20261014-0450-n16-cases, -0515-sat-indep, 20261013-2257-anneal16, -1200-census-invariants |
| Q2 | open | no candidate; witness sweeps n=18..25 UNKNOWN; n=27,29,30 not searched | experiments/20261014-0030-feasible-sizes/results/ |
| Q3 | open | no proof; no improvement possible below n=16; Q8-type induction needs >=5-edge cores | K35, K38, K39 |
| Q4 | solved | (unchanged) plus pointer to K35 | K29 |
| Q5 | open | c_hyp(n)=f(n) for n=5..15 (n=13..15 modulo HY); constant itself open | experiments/20261013-2257-chyp-table/table.md; K36 |
| Q6 | open | partial: all extremal sets found have HY slack 5 (n=12) or 4 (n=14, saturated); min slack 3 over the LP dataset for n>=10 [heuristic] | K41, K45, experiments/20261014-0020-lp-fit |
| Q7 | open | partial: library to 8 vertices (44 + 243 = 287 cores) | K32, K33 |
| Q8 | open | holds on realizable data (evidence), false in the abstract class | K34, K38 |
| Q9, Q10 | open | open; necessary conditions K30/K31/K33; Q10 data point f(n)/n minimised at n=14 for n<=15 | K29, K24 |
| Q11 (new) | - | (14,11,alpha<=8) non-saturated case, DFS running | experiments/20261014-1005-census-dfs/n14m11dfs |
| Q12 (new) | - | n=13 and n=15 saturated counts not computed | K43 note |

### kb/00_START_HERE.md (NOT edited; exact replacement text for the PI). START_HERE claims to win over other files, so these updates matter.
1. **Header sentence** "(it already includes the corrections found on 13 Oct 2026)". Replace with: "(it includes the corrections found on 13 Oct 2026 and the status update of 15 Oct 2026; results of the autonomous run are in results/FINAL_REPORT.md and results/LEDGER.md)."
2. **Section 1 Status**, append after the sentence ending "lists exactly these bounds.": "**Autonomous run, 2026-10-13/16 [verified-here].** No improvement of either bound was found. The run produced exact small-case results (section 5), three referee-accepted census certificates (L002 to L004) and one extension certificate (L001), and structural lemmas K30, K31, K44; see results/FINAL_REPORT.md."
3. **Section 2 list "For a (4,5)-set"**, append two items: "6. (Monotone midpoints, K30 [verified-here].) If $(i,j,k)$ and $(i',j',k')$ are APs with $i\le i'$, $k\le k'$ and $(i,k)\ne(i',k')$ in rank order, then $j<j'$. 7. (No medial triangle, K31 [verified-here].) Three APs $\{a,b,c\},\{a,p,e\},\{c,q,e\}$ with midpoints $b,p,q$ do not occur in a (4,5)-set (they force $x_a+x_q=x_b+x_p$)."
4. **Section 3, after "Values on the record sets"**, append: "Every one of the 54,243 extremal 12-point classes has $m=10$, $\delta=5$, $D=11$ (K41); every one of the 2,910 saturated extremal 14-point classes has $m=12$, $\delta=4$, $D=10$ (K45) [derived-here from the counts]."
5. **Section 4 table**, append a line below it: "Status of the feasible sizes [heuristic]: $n=16$ undecided (Q1; no pattern with $\alpha\le9$ found by CP-SAT, SAT, annealing; no certificate reachable); $n=18,20,22,23,25$ searched in witness mode for 1200 to 3600 s each, UNKNOWN (D15, D18). Degree bound in Gyarfas-Lehel-tight saturated hypergraphs (K44): $\deg\le5$ for $n\in\{12,14,16\}$, $\deg\le4$ for $n\in\{18,20,22\}$ [derived-here]."
6. **Section 5**, first bullet: after "all small extremal sets are in `data/small_records.json`." append "Pattern: $f(n)=\lceil n/2\rceil+1$ for $6\le n\le15$ and $n=17$, equal to the Henning-Yeo bound for every $6\le n\le23$ (K35) [verified-here]." Second bullet "**$f(16)\in\{9,10\}$**: the first open case, and exactly where a new record (9/16) would live;" append "undecided after exhaustive solver attempts (Q1, D15, D16); the data lean to $f(16)=10$ [heuristic]". Add a new bullet: "**Extremal-set counts [verified-here].** Saturated extremal affine classes for $n=6,\dots,14$: 1, 4, 66, 1262, 6644, 466961, 54243, (n=13 not computed), 2910 (K41, K43, K45; certificates L002, L003, L004). For $4\le n\le11$ there are also non-saturated extremal families (infinitely many classes); $n=12$ is the smallest $n\ge4$ with finitely many. Whether 2,910 is the complete count at $n=14$ depends on the open $(14,11)$ case (Q11)."
7. **Section 6, bullet "Midpoint-saturated" and "Affinely rigid"** (they describe the record sets only, which is correct). Append to the second: "Not every extremal set is saturated: for $n\le11$ there are positive-dimensional families (K43; the $n=8$ record set is one), but all 54,243 extremal 12-point classes and all 2,910 saturated 14-point classes are rigid (K41, K45)."
8. **Section 6, bullet "The two 12-point sets share an incidence pattern but are not affinely equivalent. A third ... "** Replace by: "The record 12-point sets are a small sample: there are exactly 54,243 affine classes of 12-point (4,5)-sets with $h=7$ (K41), including the three listed here and the two from omega #9804."
9. **Section 7 "Settled: do not redo"**: change "No 2-point extension of $A_{\rm base}$ beats 4/7 [community]" to "[verified-here] (certificate L001, K13)"; append bullets: "Q8 ($7\tau\le3|R|+2e_2+4e_1$) is false for the abstract class and needs forbidden cores with $\ge5$ edges (K38, K39, D17); direct SAT/CP-SAT/annealing decisions of $\alpha\le9$ at $n=16$ do not terminate (D15, D16, D20, D21); witness sweeps at $n=18..25$ UNKNOWN (D18)."
10. **Section 8 Reading order**: append "9. results/FINAL_REPORT.md and results/LEDGER.md (what the autonomous run established); kb/methods/trackL_inductive_framework.md; kb/notes/gl_tight_structure.md; data/README.md (census files)."

### kb/RESEARCH_PLAN.md (not in the requested edit list; status only, PI decides)
Append a status footer: "Status 2026-10-15: Phase 0 done. P1.1: census done as ordered-pattern censuses (n<=8 all patterns; saturated extremal classes n=6..14; data/README.md) rather than the planned data/census_n{n}.jsonl.gz of all abstract hypergraphs, which was not produced. P1.2: f(8), f(10) done; f(16) undecided. P1.3: forbidden library to 8 vertices (287 cores); special-pieces library not built as such. P1.4: c_hyp(n)=f(n) for n=5..15. Track U: U1 (annealing), U2 (CEGAR) run, no record (D15, D16, D18); U3, U4, U5 not run. Track L: L3 tested (K34, K38, K39) with a negative result for abstract proofs; L1, L2, L4, L5 not pursued beyond K44."

### kb/ideas_backlog.md and kb/dead_ends.md: see (e). Both EDITED.

## (b) Verified results in journal/LOG.md not reflected in LEDGER.md or FINAL_REPORT.md
"LEDGER" = results/LEDGER.md rows; "REPORT" = FINAL_REPORT. A result counts as reflected if the specific numbers appear.
| LOG timestamp | Result | In LEDGER? | In REPORT? | Proposed action |
|---|---|---|---|---|
| 2026-10-13T22:30Z | Third inequivalent 12-point set with h=7 (K12-related) | no (START_HERE section 6 only) | no | superseded by the census; one clause in R1 |
| 2026-10-13T23:30Z / 2026-10-14T00:50Z | 20.8% of 2500 random linear saturated maps at n=16 are exact (4,5)-sets [heuristic]; annealer stats | no | partly (annealing counts yes; 20.8% no) | add to Q1/D16 narrative; optional |
| 2026-10-14T00:15Z | c_hyp(n)=4,4,5,5,6,6,7,7 for n=5..12, = f(n); F7-freeness matters only at n=7; n=13..15 modulo HY | only as part of K35/K36 wording ("equal to realizable values") | R7 says abstract saturated value, not c_hyp(n)=f(n) for n=5..15 | LEDGER row K35-K36: add "c_hyp(n)=f(n), n=5..15 (experiments/20261013-2257-chyp-table/table.md)" |
| 2026-10-14T04:50Z (3) | LP fit over 1,333,217 realizable hypergraphs: HY slack >=0 everywhere, min slack 3 for n>=10; frontier tau <= (33/119)n+(3/17)m; no row with D/n<5/7 [heuristic] | no | only a path pointer (section 3) | add the three numbers to REPORT section 3 |
| 2026-10-14T04:50Z (4) | Independent DFS engine agrees with CP-SAT for n=5..12; n=16 estimate about 1e14 nodes | no | yes (section 2/4) | none |
| (no LOG entry; K37 only in known_results.md) | K37: GL colouring constraints are sound and speed UNSAT proofs 10-14x at n=12 | **no (K37 missing)** | no | LEDGER row K37; add a LOG line if desired |
| 2026-10-14T06:55Z | K38: Q8 false in the abstract class | **no** | yes (R8) | LEDGER row K38 |
| 2026-10-14T07:35Z | K39 inductive-fit constants 3/7 vs 31/70 | **no** | yes (R8) | LEDGER row K39 |
| 2026-10-14T08:00Z | K40: 3,980 twelve-point classes from a partial census | **no** | no (superseded by K41) | LEDGER row K40 marked "superseded by K41" |
| 2026-10-14T08:10Z | n=15 layer-1 streams: no solution for m'=9,10 in 2 h; >=3,935 for m'=11 [heuristic] | no | no | add to REPORT section 2 and cite D19 |
| 2026-10-14T11:20Z | K42: 146 realizable 14-point classes from the 2 h partial CP-SAT census; 18/20/22 witness sweeps UNKNOWN | **no** | sweeps yes; partial census superseded by K45 | LEDGER row K42 marked "superseded by K45" |
| 2026-10-14T13:00Z | Census invariants over the 395,196 filtered (12,10) patterns: max degree <=4, colour classes (k-1,k), no reflection symmetry hold for ALL; separators are weak | no | no (only "constrained runs with all census invariants") | add one sentence to REPORT section 2 and D20 (done in dead_ends) |
| 2026-10-14T13:25Z | n=23, n=25 sweeps ran 1200 s each, not one hour | n/a | **inconsistent** (priority item 4) | fix REPORT section 2 |
| 2026-10-14T17:25Z | Novelty CLEAR for L002/L003/K30/K31 only | no | overstated (priority item 4) | fix R5 |
| K44 (derived-here) | Degree bound in GL-tight saturated hypergraphs | **no (K44 missing)** | yes (R5) | LEDGER row K44 |
| 2026-10-15T20:45Z | (14,11) CP-SAT UNKNOWN after 7000 s; DFS launched | no | yes (section 4) | none (row appears at completion) |
| (LOG duplicates) | the entry "2026-10-14T15:30Z result L002 ACCEPTED" appears twice in journal/LOG.md (append-only, so left) | n/a | n/a | note only |

Proposed LEDGER rows (PI to apply; insert after fixing the blank line before the K30-K31 row):
```
| 2026-10-14 | K37 | GL colouring constraints are sound for the SAT model and speed UNSAT proofs 10-14x at n=12; n=13 and n=16 still out of reach | [verified-here] | experiments/20261014-0515-sat-indep/README.md |
| 2026-10-14 | K38-K39 | Q8 is false for the abstract class (explicit 12-vertex violator; every violator contains a 5- or 6-edge core); best inductive constant 3/7 realizable vs 31/70 abstract | [verified-here] | experiments/falsify/q8-abstract/counterexample.json; experiments/20261014-0700-inductive-fit/README.md |
| 2026-10-14 | K40, K42 | Partial censuses (3,980 twelve-point and 146 fourteen-point classes), superseded by K41 and K45 | [verified-here] | experiments/20261014-0610-extremal-census/results/ |
| 2026-10-14 | K44 | Degree bound deg(v)<=(23-k)/3 in Gyarfas-Lehel-tight saturated hypergraphs on n=2k vertices | [derived-here] | kb/known_results.md K44; kb/notes/gl_tight_structure.md |
```

## (c) K-rows (and other cited paths) whose evidence does not exist on disk
Script result [verified-here]: of all path tokens in kb/known_results.md, results/LEDGER.md, results/FINAL_REPORT.md, kb/dead_ends.md, kb/open_questions.md, kb/ideas_backlog.md, kb/00_START_HERE.md, exactly one does not resolve from the repo root: **K43 `results/summary.json`** (exists as experiments/20261014-1430-small-counts/results/summary.json). All named tests (`test_abase`, `test_twelve_point_sets`, `test_rigidity`, `test_f7_not_realizable`, `test_fibonacci_caveat`, `test_chain_densities`, `test_hy_feasibility`, `test_fn_bounds`, `test_small_records`) exist. Brace-lists (K36 `{README.md,check.py}`, chyp-table `{table.md,witnesses.json,check.py}`) were checked by hand: all exist.

Paths that exist on disk but are **git-ignored** (so absent from GitHub) while cited as evidence [verified-here via `git check-ignore -v`]:
- K45, L004: `experiments/20261014-1005-census-dfs/n14/results/post/summary.json` and `.../n14/results/n14_m12_TOTAL.json` (rule `.gitignore:20`). Mitigated by data/census_n14_m12_*.
- K43/L003: `experiments/20261014-1430-small-counts/n11/results/` (raw n=11 pipeline output; summary `results/n11_m9_postprocess_summary.json` is tracked).
- K36/K41-K42, D19: `*_progress.json` and `*_solutions.jsonl` under experiments/20261014-0550-n16-layered and -0610-extremal-census (raw solver streams). The K42 realizable sets file is tracked.
- Every `experiments/**/run.log` (includes the (14,11) relaunch command, priority item 2) and `experiments/**/logs/*.log`.
- Missing README.md (convention in CLAUDE.md): experiments/20261014-0005-ordered-dfs, -0030-feasible-sizes, -0030-n16-decision-realizable, -0610-extremal-census, falsify/, referee/. At 23:12 UTC another agent was creating READMEs for the first three (untracked files appeared during this audit), so they are not duplicated here. -0610-extremal-census is the evidence directory of K36, K40, K42 and still has none; falsify/ and referee/ are containers.

## (d) Root README.md section
EDITED directly: section "Results of the autonomous run (2026-10-13/16)" (19 lines) inserted before "Quick start". It points to FINAL_REPORT.md, LEDGER.md, the L001-L004 certificates, the census data files and the dead ends. It contains only facts that appear in FINAL_REPORT/LEDGER/known_results, plus the two new data files. The remainder of README.md (setup instructions for the original launch) is unchanged and still describes the original model/launch procedure.

## (e) dead_ends.md and ideas_backlog.md
EDITED directly. kb/dead_ends.md: appended D17 (abstract proof of Q8), D18 (witness sweeps n=18..25), D19 (layered 15 to 16 search), D20 (census invariants do not prune n=16), D21 (CP-SAT for the (14,11) case). Existing D1 to D16 untouched. kb/ideas_backlog.md: a Status sentence appended to each of ideas 1 to 12 (untested for 1, 2, 6, 8, 9, 12; tried for 4, 5, 10 partly; partial for 7, 11) and new ideas 13 to 18 (exact n=16 engine; deletion lemma on the census; Q8-type induction with 5/6-edge cores; non-saturated families; extending the sequence and OEIS; cores for 9 to 10 vertices).

## Edits made (exact list)
- kb/open_questions.md: added column "Status (2026-10-15)" to Q1 to Q10, closed Q4 wording, added Q11 and Q12. Original question text unchanged.
- kb/dead_ends.md: appended rows D17 to D21.
- kb/ideas_backlog.md: appended status sentences to ideas 1 to 12; appended ideas 13 to 18.
- README.md: inserted the results section before "## Quick start (Claude Code on the web)".
- data/README.md: replaced "(none yet)" by a header, and documented small_records.json, forbidden_ordered_n8.json, the two new census files and the census data under experiments/.
- NEW data/census_n14_m12_classes.jsonl.gz (100 KB; 2,910 lines; built by concatenating the `real` lists of experiments/20261014-1005-census-dfs/n14/results/post/real_*.json.gz, keys n, m, h, set, edges). Check at creation: 2,910 lines, 2,910 distinct sets, all h=8, is_45 and rigid true in the source; 5 random lines re-verified with e757.core (is_45_set True, alpha 8); A_base = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056] occurs. This does NOT re-prove the count; it only republishes the data certified by L004.
- NEW data/census_n14_m12_summary.json (1 KB): the post/summary.json plus the DFS totals.
- NEW this README.
Not touched: judge/, GOAL.md, scripts/status.*, .claude/, results/*, kb/known_results.md, kb/00_START_HERE.md, journal/STATE.md, .gitignore. Note for the PI: experiments/20261014-0450-n16-cases/README.md had an uncommitted modification (a results table written by aggregate.py: 4 of 30 cases TIMEOUT) that is not from this audit and was not committed with it.
