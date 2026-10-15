# Verification of the knowledge-base audit (experiments/20261015-2310-kb-audit/README.md, commit c278161)

Verifier notes, 2026-10-15 ~23:40 UTC. Scope: check the audit's findings and its direct edits against the evidence
files they cite; check the "LOG results not reflected elsewhere" table both ways on a sample; flag overclaims in the
proposed (not yet applied) text. No file other than this one was edited. Reading and small scripts only (the
(14,11) DFS kept running). Tags: [verified-here] = I opened the file / ran the check; [derived-here] = arithmetic.

## Overall verdict
**ACCEPT with corrections.** Every direct edit the audit made (kb/open_questions.md, kb/dead_ends.md D17-D21,
kb/ideas_backlog.md, README.md, data/README.md, the two data/ files) is a status update that traces to an evidence
file on disk, carries a tag, and does not change any mathematical statement. The six priority findings are all
correct. I found one factual error the audit copied from FINAL_REPORT into open_questions (the "14% at n=14"
figure), one mislabeled count (395,196 vs 395,039), one double count in a proposed START_HERE sentence (five vs
three known 12-point sets), one wrong citation (D21 for n=16), and a few places where a tag or caveat should travel
with a proposed sentence. Details below; the PI should apply the audit's proposals with the corrections in section 5.

## 1. Priority findings: all six confirmed [verified-here]
| # | Audit claim | Check |
|---|---|---|
| 1 | K45/L004 evidence is git-ignored | `git check-ignore -v`: `.gitignore:20 experiments/20261014-1005-census-dfs/n14/results/` hides `post/summary.json` and `n14_m12_TOTAL.json`. Directory 23 MB (5,074 per-prefix `n14_m12_prefix_N.jsonl.gz`/`.done` files + `n14_m12_prefixes.txt` + `n14_m12_TOTAL.json` + `post/`). `post/` is 2.2 MB (the 12 `real_*.json.gz` are 136 KB; `judge_tmp/` holds 50 claim files, which an un-ignore of `post/` would also add). The proposed pattern `n14_m12_prefix_*` matches exactly the per-prefix files and not `n14_m12_prefixes.txt`. |
| 2 | (14,11) relaunch command only in an ignored run.log | `n14m11dfs/run.log` line 2 is verbatim `python3 -m e757.ordered_dfs_split 14 8 11 3 4 experiments/20261014-1005-census-dfs/n14m11dfs/results --refl --nice 10 --tag n14_m11`; header `# started 2026-10-15T22:57:17Z max 26h`; `prefixes: 3437 (depth 3)`. `.gitignore:8` ignores `experiments/**/run.log`. FINAL_REPORT section 4 indeed says "relaunch with the command in its run.log". |
| 3 | STATE.md stale | STATE still says census at 1691/2537, next action L004. LOG 2026-10-15T16:42Z (enumeration COMPLETE), 20:45Z ((14,11) DFS launched), 23:00Z (L004 ACCEPTED). Confirmed stale. |
| 4a | FINAL_REPORT "one-hour" for n=23, 25 | FINAL_REPORT line 68. experiments/20261014-0030-feasible-sizes/README.md and results/*.json: n=18,20,22 wall 3600 s; n=23 (m=19,20,21) and n=25 (m=21,22,23) wall 1199-1209 s each. Audit's replacement text is accurate. |
| 4b | FINAL_REPORT R5 novelty sentence overstated | Only two scout files exist: `baseline__scout__20261013T230359Z.md` (bounds only) and `L002-...__scout__20261014T171802Z.md`, whose header says "Claims checked: (1) 54,243 ... (2) counts n=6..11 (3) K30, K31". K33's medial 4-cycle and K44 are not mentioned anywhere in it. Its Limits section says the papers were "not re-read in full today". Audit's replacement text is accurate. |
| 5 | LEDGER blank line and missing rows | `cat -A`: blank line 13 between the `chains` row and the `K30-K31` row. Rows present: baseline x2, small-f, hy-feasible, f8-f10, chains, K30-K31, K32-K33, K34, K35-K36, L001, K41/L002, K43/L003, K45/L004. K37, K38, K39, K40, K42, K44 absent. Confirmed. |
| 6 | K43 evidence `results/summary.json` relative | known_results.md line 49 cell reads `experiments/20261014-1430-small-counts/README.md, results/summary.json`; `experiments/20261014-1430-small-counts/results/summary.json` exists and is tracked. Confirmed. |

## 2. The two new data files [verified-here]
- `data/census_n14_m12_classes.jsonl.gz`: 2,910 lines; 2,910 distinct `set` values; every line has 14 points, 12 edges,
  `h: 8`. Re-built the set of sets from the ignored source `n14/results/post/real_*.json.gz` (12 files, 2,910 records):
  identical as a set. A_base occurs (grep of the compact JSON: 1 hit). 5 random lines (seed 7, different from the audit's
  sample) re-checked with `e757.core`: `is_45_set` True, `alpha` 8, 12 APs, all five.
- `data/census_n14_m12_summary.json`: byte-for-byte the content of `post/summary.json` plus a `dfs_totals` object equal to
  `n14_m12_TOTAL.json` (prefixes 2537, solutions 205529, nodes 113454008923, cpu_seconds 277501.0). Correct.
- The audit's own caveat ("does NOT re-prove the count; only republishes the data certified by L004") is the right one.

## 3. Direct edits, item by item
### kb/open_questions.md
Diff: first four columns of Q1-Q10 unchanged (Q4 included); a fifth column added; Q11, Q12 added. Each status traces:
- Q1: 4.0M states / 28,589 genuine sets / best h=10 = LOG 00:50Z and anneal16 README table; ~1e14 DFS nodes = LOG 04:50Z (4). OK.
  Nit: "no certificate reachable" is a judgment; the timeouts are [verified-here], the consequence is [heuristic].
- Q2: matches feasible-sizes README exactly (3600 s / 1200 s, 3 workers, UNKNOWN). OK.
- Q3: HY 2021 unobtainable = LOG 23:20Z. OK.
- Q5: **ERROR**: "about 14% of abstract extremal patterns realizable at n=12,14". n=12: 54,243/395,039 = 13.7% (OK).
  n=14: 2,910/46,419 = 6.3% of the O' class (8.3% of the all-cores set); the partial K42 sample gave 157/1,474 = 10.7%.
  The 14% figure was copied from FINAL_REPORT section 2, line 67 ("about 14% ... at n=12 and n=14"), which is itself
  wrong for n=14 and which the audit did not flag. Fix both: "13.7% at n=12 (K41), 6.3% at n=14 (K45)".
- Q6: min slack 3 for n>=10 = lp-fit README line 25 (also 3 at n=9). OK. delta/D arithmetic: n=12,m=10,tau=5: 60+30-85=5, D=119-108=11; n=14,m=12,tau=6: 70+36-102=4, D=136-126=10 [derived-here]. OK.
- Q7: 44 cores (n=5..7, <=5 edges) and 243 new at n=8 (<=6 edges) re-read from the two JSON files. `experiments/referee/catalogue-n8` tracked. OK.
- Q8, Q9, Q10: match K34/K38, K30/K31/K33, K24/K29. OK.
- Q11: 3,437 prefixes, 22:57Z, CP-SAT UNKNOWN 7000 s = run.log + `n14_m11_result.json` (wall 7000.1). OK.
- Q12: "about 10 h per m" = K43. OK.
### kb/dead_ends.md D17-D21
- D17: 60/18,180 violators, |D|=2, 5-6-edge cores, 31/70 vs 3/7 = K38/K39 and LOG 06:55Z/07:35Z; evidence paths exist and are tracked. OK.
- D18: = feasible-sizes README. Tag [heuristic] correct (UNKNOWN only). OK.
- D19: m'=9,10 no solution in 2 h, m'=11 >= 3,935 = LOG 08:10Z. Progress JSONs are indeed ignored (.gitignore:17). OK.
- D20: numbers = LOG 13:00Z/14:25Z and census-invariants README. **Mislabel**: "395,196 filtered (12,10,alpha<=7) patterns" is R12 (54,243) + U12 (340,796) + R14 (157 fourteen-point patterns) = 395,196; the (12,10) O' class has 395,039 patterns (census-dfs README, invariants README line 9). The invariants do hold on all three sets, so the fact stands; the label should read "all 395,039 O' patterns at (12,10) and the 157 partial (14,12) patterns". Same mislabel in LOG 13:00Z, K44, and ideas_backlog idea 11 (pre-existing in LOG/K44; new in D20 and idea 11).
- D21: = `n14_m11_result.json`. OK.
### kb/ideas_backlog.md
Status sentences 1-12 and ideas 13-18 trace to: lp-fit README (idea 5: 33/119, 3/17, 3n/7 tight only at A_base), gl_tight_structure.md header (idea 7: ~80k flip instances), K44/invariants (idea 11, with the 395,196 mislabel above), scout file (idea 17). "No LLM-written generator programs were run [no claim]" (idea 10) is consistent with the LOG. Idea 3 "untested as stated" is fair. OK.
### README.md (19-line section)
Every number traces to LEDGER/known_results (54,243; 1,4,66,1262,6644,466961; 2,910; 287 cores; K35; D15-D21). `experiments/20261014-1005-census-dfs/results/realized_n12.json.gz` is tracked. The L001 line correctly says "2-point". OK.
### data/README.md
small_records keys are 8, 10, 11, 12, 12b, 12c, 14 ("12 (three inequivalent)" correct); n7 file: 44 cores, max 5 edges; n8 file: n=8 only, 243 cores, max 6 edges; `n12_m10_all.jsonl.gz`, `realized_n12.json.gz`, `n11_m9_postprocess_summary.json` tracked; `n11/results` and `n14m11dfs/results` ignored (.gitignore:27, 29). OK.

## 4. The "LOG results not reflected elsewhere" table, checked both ways on 10 sampled entries [verified-here]
| LOG entry | Audit says | My check |
|---|---|---|
| 23:30Z / 00:50Z annealing (20.8% of random maps realizable) | not in LEDGER/REPORT | REPORT has the 4M/28,589 counts, not the 20.8%. Correct. |
| 00:15Z c_hyp(n)=f(n), n=5..15 | LEDGER only via K35-K36 wording | LEDGER K35-K36 row says "equal to the realizable extremal values in all resolved cells"; REPORT R7 does not state c_hyp(n)=f(n). Correct. |
| 04:50Z (3) LP fit numbers | REPORT path pointer only | REPORT section 3 cites experiments/20261014-0020-lp-fit without the numbers. Correct. |
| 06:55Z K38 | LEDGER no, REPORT R8 yes | Confirmed (R8 at line 53). |
| 07:35Z K39 | same | Confirmed. |
| 08:00Z K40 (3,980) | LEDGER no, REPORT no | grep "3,980" in REPORT: no hit. Correct. |
| 08:10Z n=15 streams | neither | grep "layer"/"m'=" in REPORT: no hit. Correct. |
| 11:20Z K42 (146) | LEDGER no; sweeps in REPORT | grep "146" in REPORT: no hit. Correct. |
| 13:00Z invariants | REPORT one phrase only | REPORT line 66 "constrained runs with all census invariants" only. Correct. |
| 17:25Z novelty CLEAR | overstated in R5 | see 1/4b. Correct. |
Also confirmed: K37 has no LOG entry (grep colouring/K37/gl_constraints: none); the 15:30Z L002 entry is duplicated
(lines 126 and 130). Reverse direction: I found no LOG result that is absent from the audit's table AND from
LEDGER/REPORT; e.g. 05:50Z (K35/K36 observation) is in LEDGER, 04:50Z (1)-(2) are K33/K34 rows, 15:30Z's by-product
(f(12)>=7 without HY) is in K41. The table is complete as far as I can see.
Not rerun: the audit's exhaustive glob scan of every cited path. I opened ~30 cited paths by hand (listed in this
file); all exist, and the git-ignored ones are exactly the ones the audit lists.

## 5. Overclaims / corrections to apply to the PROPOSED text (not yet in any file)
1. **START_HERE item 8** ("including the three listed here and the two from omega #9804"): double count.
   small_records 12b and 12c are byte-identical to core.KNOWN "12-point example 1/2 (omega #9804)"; the three known
   classes are {0,269,...,575}, 12b and 12c. Write "including the three sets listed here (two from omega #9804)".
   The same "all five known sets" wording in LOG 10:40Z and the census-dfs README counts duplicates.
2. **START_HERE item 9**: "(D15, D16, D20, D21)" for n=16 decisions: D21 is the (14,11) CP-SAT run, not n=16. Cite D15, D16, D20.
3. **START_HERE item 6** (extremal-set counts tagged [verified-here]): consistent with K45's tag, but since START_HERE
   "wins" over other files, carry L004's scope caveat: completeness of the 205,529-pattern enumeration was re-checked by
   the referee on 28% of the prefixes plus consistency checks, not by a full second enumeration (K45, LEDGER, REPORT R3
   and the L004 proof all say this; the proposed sentence does not).
4. **START_HERE item 2** lists "structural lemmas K30, K31, K44" under a [verified-here] tag; K44 is [derived-here].
5. **START_HERE item 5 / Q1**: "no certificate reachable" should be [heuristic] (the timeouts are verified, the conclusion is a judgment).
6. **Proposed LEDGER row K38-K39**: K39 is tagged "verified-here (fits [heuristic])" in known_results; the proposed row drops the "(fits [heuristic])" qualifier. Keep it.
7. **RESEARCH_PLAN footer** "U5 not run": 736 one-vertex amalgams and 300 three-piece amalgam trees (<=31 points, exact (4,5) check) were built as Q8 test data (experiments/falsify/q8-omega-inequality/report.md, rows 3a/3b). Say "U5: amalgams generated only as Q8 test data; no record search over amalgams".
8. **FINAL_REPORT line 67 and open_questions Q5**: the "14% at n=14" error (section 3 above). The audit's list of FINAL_REPORT overstatements should include it.
9. **395,196 -> 395,039 + 157** (section 3, D20) in D20, ideas_backlog 11, K44 and LOG 13:00Z (LOG is append-only; add a correction line).
10. L001 scope: every place the audit touches (README.md, proposed START_HERE item 9) keeps "2-point"; no overclaim found. L004 scope: FINAL_REPORT R3 (lines 21-26) already states the sampling caveat and the open m=11 case; no overclaim there.

## 6. Other observations
- Working tree at verification time: 8 experiment READMEs modified and 4 untracked README/dirs from another agent
  (not from the audit); the n16-cases table "4 of 30 cases TIMEOUT" matches LOG 05:50Z. A `git add -A` commit by any
  agent will sweep these in; this verification commits only this file.
- The audit's item (c) missing-README list is accurate at 23:12; `experiments/20261014-0610-extremal-census/README.md`
  now exists untracked (another agent), so that gap is being closed.
- `experiments/20261014-1005-census-dfs/n14/results/post/judge_tmp/` (50 temp claim files) would be added by an un-ignore of
  `post/`; harmless but worth an explicit ignore line.
