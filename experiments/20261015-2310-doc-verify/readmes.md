# Verification of the experiment-folder documentation pass (commit 95ffcf3)

Verifier notes, 2026-10-15 ~23:25 UTC. Scope: every README that commit 95ffcf3 wrote or changed (4 new folder
READMEs, 3 index READMEs, 9 filled-in READMEs, data/README.md), checked against the JSON results, logs, scripts and
review files on disk. No README was edited. Method: reading plus small `python3 -I` one-liners that print JSON fields;
the two paper-digest check scripts were re-run (they take about a second each). Tags in this file: [verified-here] for
file facts and arithmetic I redid, [heuristic] for judgements of wording.

**Overall verdict.** Every quoted number I checked matches a file on disk (about 300 numbers across 17 files); the
required sections (question, method, exact command, result, conclusion, tags) are present in the four new READMEs;
the experiments index lists all 21 folders and each outcome cell agrees with its folder's README. The concrete
mismatches are few and listed in section 2; none changes a mathematical statement.

## 1. What was checked, per file (all match unless listed in section 2)

| README | checked against | result |
|---|---|---|
| `20261014-0005-ordered-dfs/README.md` (new) | `results.json` (28 entries: alpha, nodes, sec), `run.log`, `run_timings.py`, `estimate_n16.txt`, `rate_n16.txt` | all 28 table entries, loads 11.13/12.00/12.54, both estimator runs (5.804e13 +- 1.46e13, 1.18e14 +- 5.15e13, surviving 3.233e12 / 8.269e12, level maxima at 11 and 12), both 60 s probes (4,009,984 and 82,063,360 nodes, `timed_out=1`, `sols=0`) match; "50x at n = 10" = 5.38/0.11 = 49x; 0.5-0.65 M nodes/s = 30.06M/58.03 s and 4.32M/6.8 s |
| `20261014-0030-feasible-sizes/README.md` (new) | 9 `results/*.json`, `run.log`, `run_sweep.py`, `run_after_streams.sh` | all 9 rows (status, eager, wall, alpha_cuts, solves, f7_cuts, rounds/learnt), all 5 model-size triples and literal counts, build times 5.8-18.6 s, `fail_kinds` empty, `run.log` header and the DONE lines match; the cited LOG entries (09:25Z, 11:20Z, 13:25Z) exist and are about this sweep |
| `20261014-0030-n16-decision-realizable/README.md` (new) | `run.log` (2 header lines), `job.pid` (5786), `../20261014-0030-n16-decision/run_realizable.py`, LOG 04:50Z | matches; see 2.3 for a caveat on the attribution to the restart |
| `20261014-0610-extremal-census/README.md` (new) | `run.log`, `run_chain.sh`, `census.py` docstring, `results/log12.txt`, `results/*_partial_census.json`, `*_progress.json`, line counts of the three `*_solutions.jsonl`, `results_sets_n12.json` (4,448) / `results_sets_n14.json` (146), `n14_realizable_sets_partial.json` (157), LOG line 108 | all counts (30,559 / 29,228 / 4,448 and the three failure counts; 26,974 / 25,924 / 3,980; 1,474 / 1,409 / 146; n = 15: 16,944 in progress at 3,956.7 s, 16,985 lines, RUNNING, last write 11:57), rates 8.5 and 0.2 /s, file sizes 3.5/0.2/2.7 MB, `known_sets` all false, 4,448/54,243 = 8.2% match; see 2.4 for a wording issue |
| `experiments/README.md` (index) | the 21 folder READMEs, kb/dead_ends.md D15-D21, kb/known_results.md K13, K29-K45, results/LEDGER.md | 21 folders on disk = 21 rows; every outcome cell agrees with the folder README (including the 8 folders the commit did not touch: forbidden-library 2/5/24/189/2364 and 44 cores; forbidden-n8 46,281 = 16,568+28,697+498+518, 243/287 cores, 11 configurations, 145 labelings; lp-fit "no row with D/n < 5/7", 0.4538; slack-landscape unresolved cells (12,9), (13,11), (14,11); sat-indep 3.5x-14x and the 900 s TIMEOUT; inductive-fit 31/70; abase-extensions; kb-audit). "Feeds" column: every cited D-row and K-row exists and cites the folder (chyp-table is cited by LEDGER row K35-K36, not by the K35/K36 rows of known_results.md, which the cell says correctly with "(LEDGER)") |
| `experiments/falsify/README.md` (index) | the three `report.md` first lines and bodies | RESULT lines (NONE-FOUND / COUNTEREXAMPLE / NONE-FOUND) and the quoted numbers (14,645; 1000/1000/400; ~75,000 + 6,500 flips; ~32,000 tree checks; k-2 vs k-3 text error; 60 of 18,180; 57 + 46 witnesses; 10.3M states; 300 each at n = 10..13; UNKNOWN at n = 14, 16; tau = 5, R = 10, e_2 = 2, 35 > 34, 6-edge core, not realizable; 3,253,568 / 94,544; 900 + 900 sets; 300 amalgam trees; 105 > 104; <= 31 points; 34-point amalgams not run; 99,153 vs 94,544 unexplained) all match; see 2.5 for the "about 5.5e8" total |
| `experiments/referee/README.md` (index) | `head -1` of the 12 referee reviews, the scratch paths cited inside each review, the 13 scratch folders, `catalogue-n8/README.md` tail, `q8/report.md` header, LEDGER rows K32-K33 and K45 | round-to-file mapping and all 12 verdicts match; the per-round problem descriptions match the reviews (L001 r1 P1 overclaim "no 16-point ... i.e. cannot be extended", r2 "no mathematical problem" + self-contradictory scope sentence, r3 "no mathematical or computational problem" + unchanged false sentence; L002 r1 DEPENDS ON line, r2 `fastreal` vs `realize_exact`; L003 r1 "n = 12 first size at which ... finite" false, r2 closed under x -> qx + t); the named scratch files exist (`t1_out.json`, `collect14.py`, `coverage.py`, `census_keys.txt.gz`, `check.py`, `sweep.c`, ...); `catalogue-n8` ends "Every recomputed verdict matches"; `q8/report.md` starts `VERIFICATION: CONFIRMED` and says 3a/3b and parts of step 2 were not re-run |
| `20261013-2257-anneal16/README.md` (filled) | `best.json` (4 workers), LOG 00:50Z, smoke section of the same README | all 4 rows (evaluated, coll0, valid45, alpha distributions, 4,407 singular, seeds 3000/2000/3002/1003), totals 3,992,281 and 28,589, `best_valid_by_ratio` n = 18, h = 11, last merge 00:01:03Z match; "about 21%" = 519/2500 = 20.8% from the smoke section; see 2.6 for the tag |
| `20261013-2257-chyp-table/README.md` (filled) | `results/` listing, `results/feas16_m14.log` (0 bytes), `run.log`, LOG 00:15Z | file facts match; see 2.1 (the restart attribution contradicts the folder's own text and the LOG) |
| `20261013-2257-paper-digest/README.md` (filled) | re-ran `chk_fibonacci_F7_AG.py` and `chk_L13_L8.py`; `ls` of the folder, kb/notes, tests | every printed value matches (h = 3,4,4,5,6,6,7,7,8,9,9 then 10; tau = floor(2(n-1)/5); edges n-3; n = 15 prints None; is_45([1,2,3,5]) False, [2,3,5,8] True; AG(2,3) 85 > 81, minus a point 68 > 64, F7 51 > 50; 4 tau = 12, 16, 20 vs n+m = 12, 16, 21; L(8) tau 4, L(13) tau 6, L(13) F7-free, L(8) contains F7); the three .txt files, the four kb/notes digests and the two named tests exist |
| `20261014-0030-n16-decision/README.md` (filled) | `results/` (two 0-byte .gz, `zcat` "unexpected end of file"), `m13.log`/`m14.log` empty, `run.log`, LOG 04:50Z | matches; see 2.3 |
| `20261014-0450-n16-cases/README.md` (filled) | 4 `results/case_m13_k*.json`, 4 empty `*_solutions.jsonl`, `run.log`, `aggregate.py`, LOG 05:50Z | all fields (TIMEOUT, 0 solutions, wall 3000.1/2996.8/3000.1/3000.1, 1 worker, 24,752 / 36,400 / 590,460 clauses (2,495,376 literals), timestamps 05:37) match; the RESULTS block is exactly what `aggregate.py` prints; see 2.7 |
| `20261014-0550-n16-layered/README.md` (filled) | `prod/run.log`, `results/*_progress.json`, `validation_n9/*`, `crosscheck_n14_aborted/*`, `logs/` (both 0 bytes), LOG 08:10Z | all stream rows (7200.1/7200.0/7200.3 s; 0/0/3,935; 0.6 /s; build 76.6-80.0 s), N = 9 validation (4,394 = 4,394; 15,717 H', 46,215 candidates; n = 8 streams m' = 2..6), aborted N = 14 snapshots (189 at 220 s; 0 at 17 s; 850 at 262 s; 2,016 at 244 s), `n11_m5` test stream match |
| `20261014-1005-census-dfs/README.md` (filled) | `n14/results/n14_m12_TOTAL.json`, `post/summary.json`, `post/filter_counts.json`, `n14post/run.log`, `n14m11/run.log`, `n14_m11_result.json`, `n14m11dfs/run.log`, `.done` count, `.gitignore`, `data/census_n14_m12_*` | all counts match (205,529 / 119,844 / 46,419 / 34,995; 2,910 realizable, 43,509 = 41,751 + 912 + 846; 11,424 = 11,378 + 33 + 13 = 46,419 - 34,995; 113,454,008,923 nodes; 277,501 CPU-s = 77.1 h; judge 50/50; A_base present; m = 11 CP-SAT UNKNOWN at 7000.1 s with 299 solves and 596 F7 cuts; 3,437 prefixes, 70 `.done` at 23:19 vs 68 quoted at 23:10); see 2.8 for one wording issue |
| `20261014-1200-census-invariants/README.md` (filled) | existing README body (lines 20, 52-53, 71-72) | the added "Method in brief" paragraph only restates what the body already says (~65 statistics, tiers t1/t2, three engines); consistent |
| `20261014-1430-small-counts/README.md` (filled) | `results/summary.json` | saturated classes 1, 4, 66, 1,262, 6,644, 466,961 for n = 6..11 match `realizable_patterns` of the m = n-2 cells; the L003 review file named exists with VERDICT: ACCEPT |
| `data/README.md` (schema line) | `data/small_records.json` | keys "8","10","11","12","14","12b","12c"; fields set/n/h/m with optional "source" ("Ma-Tang 2026" on "14", "omega issue #9804" on 12b/12c); K29 exists; matches |

## 2. Concrete mismatches and overstatements (file paths given)

2.1 **`experiments/20261013-2257-chyp-table/README.md`, new paragraph "Final status of the n = 16 run"** says the run
"left no result (... background jobs of that night died in the 04:40 UTC container restart)". This contradicts (a) the
same README's later line "Follow-up (2026-10-14): the unconstrained n=16 jobs above were killed", (b) journal/LOG.md
2026-10-14T04:50Z, which lists the jobs that died in the restart (n=16 CP-SAT decision m=13/m=14, realizable-CEGAR,
sweep at n=18) and does not include the chyp-table job, and (c) the job's own limits: `run.log` says `max 2h` from
23:20:44Z, and `scripts/start_job.sh` wraps the command in `timeout 2h`, so the process could not have been alive at
04:40. The correct statement, supported by the files, is only: the job left no result file and `feas16_m14.log` is
empty; the folder's own text says the jobs were killed. [verified-here]

2.2 **`experiments/20261014-0030-n16-decision/README.md` and `.../n16-decision-realizable/README.md`** attribute the
deaths to the 04:40 restart, which is what LOG 04:50Z says, so the READMEs quote the LOG correctly. Caveat worth one
sentence in each: both jobs were started with `max 2h` (00:31:37Z and 00:44:18Z) under `timeout 2h`, i.e. the wrapper
would have ended them by 02:32 / 02:44 UTC, before the restart; and the solver limit was 6500 s, so a normal end would
have written a result JSON before the timeout. The folder evidence (no result file, no DONE line) therefore does not
distinguish "killed by the restart" from "killed by the 2 h timeout before writing"; only the LOG's attribution says
restart. [verified-here for the times; the inference is mine]

2.3 **`experiments/20261014-0030-n16-decision-realizable/README.md`, Open issues**, says "whether the job was killed
after 4 minutes or after 4 hours" is unknown. With `timeout 2h` in `scripts/start_job.sh` the upper bound is 2 hours,
not 4. Minor. [verified-here]

2.4 **`experiments/20261014-0610-extremal-census/README.md`**, sentence "none of the five known 12-point sets ... occurs
among the enumerated patterns": the census JSON has five `known_sets` keys for n = 12, but two of them are the same
sets as 12b/12c under other names (experiments/falsify/gl-tight-structure/report.md line 7: "the 2 omega KNOWN sets,
duplicates of those"; kb/00_START_HERE.md section 6 knows exactly three inequivalent 12-point sets). "Three known
12-point sets (listed under five keys)" would be exact. [verified-here]

2.5 **`experiments/falsify/README.md`**, row `q8-omega-inequality/`: "about 5.5e8 states in total". Summing the rows of
the report's table (step 1: 4.60M; 2a: 118.0M; 2b: 444.9M; 3a: 5.53M; 3b: 6.0M) gives about 5.8e8; K34 says "~560M
sampled" and LEDGER row K34 "~570M". The report itself states no total. The figure is the index's own arithmetic and is
slightly low; "about 5.8e8 (the report gives no total)" would be exact. [verified-here, arithmetic from the table]

2.6 **`experiments/20261013-2257-anneal16/README.md`, Conclusion**: "[verified-here] realizability is not the bottleneck
(about 21% of random linear saturated maps at n = 16 are exact (4,5)-sets)". The 519/2500 = 20.8% count is exact and
[verified-here]; the statement "realizability is not the bottleneck" is an interpretation of a random sample and should
carry [heuristic], as the index row for the same folder does. Tag inflation only. [heuristic]

2.7 **`experiments/20261014-0450-n16-cases/README.md`** says the aggregate block was "rewritten by `aggregate.py` on
2026-10-15", while the documenting agent's report says no code was run beyond the two paper-digest scripts. The block
is byte-for-byte what `aggregate.py` would print from the four JSONs, so the content is right either way; the
provenance sentence is unverifiable from the files (mtime of README.md is the commit time). Minor. [verified-here for
the content]

2.8 **`experiments/20261014-1005-census-dfs/README.md`**, "The 'timing' estimate above (55-70 h single process) was
beaten by the 3-4 worker split: 277,501 CPU-seconds (about 77 CPU-hours)". 77 CPU-hours is more than the 55-70 h
estimate, not less; what the split shortened is wall-clock time. "The estimate was about right in CPU terms (77 h);
the split brought the wall-clock time down" is what the numbers show. [verified-here]

2.9 **`experiments/20261014-0005-ordered-dfs/README.md`**: `run_timings.py`'s docstring says "n=13 and n=16 are
separate jobs, see README", but the README mentions no n = 13 job and the folder holds no n = 13 file. The README's
open-issues list could note that the n = 13 job announced by the script left no trace. Minor. [verified-here]

2.10 **`experiments/referee/README.md`**, row `L001/`: "the Statement overclaimed (16-point and 17-point corollary)".
The review's P1 is about the clause "no 16-point (4,5)-set containing A_base has h <= 9, i.e. A_base cannot be extended
to a new record"; the 17-point case is mentioned by the referee as a corollary that does hold, not as part of the
overclaim. Slight misparaphrase; the verdict and file mapping are right. [verified-here]

## 3. Things the documenting agent flagged as open that I confirm from the files

- ordered-dfs: the estimator / rate-probe arguments are indeed not recorded anywhere in the folder; the 20x node-count
  gap between the two 60 s probes has no explanation in any file.
- extremal-census: `log12.txt` (26,974) vs `n12_m10_partial_census.json` (30,559) are two runs with the same 3600 s
  limit; nothing on disk explains the difference (plausibly machine load, but no load line was recorded).
- n16-decision-realizable: the folder holds only `run.log` and `job.pid`, both git-ignored, so on GitHub the folder is
  README-only.
- census-dfs: the (14,11) prefix-split DFS is still running (70/3,437 prefixes done at 23:19 UTC); the README's m = 11
  section will need a refresh when it finishes.
- forbidden-n8/README.md was not touched; its Reproduction block still says `catalogue.json` while the folder has
  `catalogue.json.gz` (the index row notes this).
- Git-ignored evidence: `.gitignore` lines 8-9 and 15-20 confirm that every `run.log`, `job.pid`, the listed
  `*_progress.json` / `*_solutions.jsonl` files and `n14/results/` are untracked; the tracked copies are
  `data/census_n14_m12_classes.jsonl.gz` and `data/census_n14_m12_summary.json` only.

## 4. Not checked

- The large referee scratch outputs themselves (only file names and the review texts were compared).
- Whether `experiments/20261014-0005-forbidden-n8/README.md` (generated, untouched) matches its data; out of scope.
- The two un-run "heuristic" scripts (`hy_tight_search.py`, annealer) were not executed.
