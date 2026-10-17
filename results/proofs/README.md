# Proof files

One file per proof, certificate or lemma: `results/proofs/<id>.md`, where `<id>` is short, for
example `P001-degree-discharging`. Reviews refer to the same id.

## Template

```
# <title>
CLAIM: c* >= 5/9
TYPE: lower-bound | lemma | certificate
STATUS: draft | submitted | ACCEPTED by referee round N (<review file(s)>) | NEEDS-WORK | REJECTED   (follow the latest review; record any edits made after it)
DEPENDS ON: <each cited fact with its tag and source, e.g. K8 [published] Henning-Yeo 2021 Thm 7>

## Statement
<precise statement with all hypotheses>

## Proof
<every step justified; number the steps; no "clearly">

## Computer-verified steps
<script path, exact command, output summary, and what the output proves>

## Sanity checks
<the inequality evaluated on A_base, both 12-point sets, Fibonacci sets and glued sets, with numbers>

## Falsifier report
<path to experiments/falsify/<slug>/report.md>
```

Only lower-bound proofs use the `CLAIM: c* >= r` line. status.sh reads it, and it must match
exactly that form, with r a fraction like `5/9` or a decimal. Lemmas and certificates use
`CLAIM-TYPE:` lines or prose instead.

## Index (as of 2026-10-17 17:25 UTC)

Rows L007-L012 (added 2026-10-17: the I11 induction chain, f(16) = 10 up to f(22) = 13, and the n = 23 record cell) come first, newest first. Rows L001-L006 follow, unchanged since the 2026-10-16 16:40 UTC index.

| id | statement | type | status | latest review | tag |
|---|---|---|---|---|---|
| L012-n23-record-no-degree-4 | a 23-point (4,5)-set with h = 13 (ratio 13/23 < 4/7) must have a saturated AP pattern with (n, m, tau) = (23, 21, 10) and every AP-degree at most 3; the cells (23, 19, 10) and (23, 20, 10) are empty; the 699 classes with a degree-4 vertex are not realizable (Q14: the degree-3 case stays open); depends on L007-L011 | certificate | ACCEPTED, rounds 1, 2 and 3 | L012-n23-record-no-degree-4__referee__20261017T162634Z.md, __referee__20261017T172032Z.md and __referee__20261017T171553Z.md; scout CLEAR: L012-n23-record-no-degree-4__scout__20261017T153400Z.md | [verified-here] |
| L011-f22-equals-13 | f(22) = 13 and I11 (11 tau <= 3n + 2m) on the abstract class for n <= 22 (K55); hence no (4,5)-set with at most 22 points beats 4/7; depends on L007-L010 | certificate | ACCEPTED, rounds 1, 2 and 3 | L011-f22-equals-13__referee__20261017T133431Z.md, __referee__20261017T154609Z.md and __referee__20261017T150941Z.md; scout CLEAR: L011-f22-equals-13__scout__20261017T123223Z.md | [verified-here] |
| L010-f20-equals-12 | f(20) = 12 and I11 on the abstract class for n <= 20 (K54); no 20-point (4,5)-set beats 4/7; depends on L007-L009 | certificate | ACCEPTED, rounds 1, 2 and 3 | L010-f20-equals-12__referee__20261017T095245Z.md, __referee__20261017T114101Z.md and __referee__20261017T105333Z.md; scout CLEAR: L010-f20-equals-12__scout__20261017T085737Z.md | [verified-here] |
| L009-f18-equals-11 | f(18) = 11 and I11 on the abstract class for n <= 18 (K53); no 18-point (4,5)-set beats 4/7; depends on L007, L008 | certificate | ACCEPTED, rounds 1, 2 and 3 | L009-f18-equals-11__referee__20261017T091817Z.md, __referee__20261017T101446Z.md and __referee__20261017T095942Z.md; scout CLEAR: L009-f18-equals-11__scout__20261017T081631Z.md | [verified-here] |
| L008-f16-equals-10 | f(16) = 10: every 16-point (4,5)-set has a Sidon subset of size 10, so none beats 4/7; I11 holds on the abstract class for n <= 16 (K52); depends on L007 | certificate | ACCEPTED, rounds 1, 2 and 3 | L008-f16-equals-10__referee__20261017T070236Z.md, __referee__20261017T082214Z.md and __referee__20261017T080425Z.md; scout CLEAR: L008-f16-equals-10__scout__20261017T061250Z.md | [verified-here] |
| L007-no-nonsaturated-extremal-14-point-sets | every 14-point (4,5)-set with h = 8 has exactly 12 three-term APs: there is no non-saturated extremal 14-point set, so the 2,910 classes of L004 are all of them (K51; Q11 closed); Corollaries 3 and 4 use L004 and L005 | certificate | ACCEPTED, rounds 1, 2 and 3 | L007-no-nonsaturated-extremal-14-point-sets__referee__20261017T043430Z.md, __referee__20261017T055829Z.md and __referee__20261017T053731Z.md; scout CLEAR: L007-no-nonsaturated-extremal-14-point-sets__scout__20261017T034349Z.md | [verified-here] |

### Rows L001-L006 (unchanged since 2026-10-16 16:40 UTC)

Ids: `P###-slug` for lower-bound proofs, `L###-slug` for lemmas and certificates. No lower-bound proof (`CLAIM: c* >= r`) exists yet; `bash scripts/status.sh` prints `lower_bound_proofs: none`. Review files are in `results/reviews/`.

| id | statement | type | status | latest review | tag |
|---|---|---|---|---|---|
| L001-abase-two-point-extensions | every (4,5)-set A_base + {x,y} has h = 10 (K13) | certificate | ACCEPTED, round 4 | L001-abase-two-point-extensions__referee__20261014T095734Z.md | [verified-here] |
| L002-census-12-point-extremal-sets | exactly 54,243 twelve-point (4,5)-sets with h = 7 up to affine equivalence (K41) | certificate | ACCEPTED, round 3 | L002-census-12-point-extremal-sets__referee__20261014T152552Z.md; scout CLEAR: L002-census-12-point-extremal-sets__scout__20261014T171802Z.md (also covers L003 and K30, K31) | [verified-here] |
| L003-census-small-n-extremal-sets | saturated extremal class counts 1, 4, 66, 1262, 6644, 466961 for n = 6..11; infinitely many extremal sets for 4 <= n <= 11 (K43) | certificate | ACCEPTED, round 3 | L003-census-small-n-extremal-sets__referee__20261014T213511Z.md | [verified-here] |
| L004-census-14-point-extremal-sets | exactly 2,910 saturated (m = 12) 14-point (4,5)-sets with h = 8; the m = 11 case, left open there (K45), is closed by L007 (K51): no non-saturated extremal 14-point set exists | certificate | ACCEPTED, round 1; completeness re-checked by sampling | L004-census-14-point-extremal-sets__referee__20261015T225426Z.md | [verified-here] |
| L005-ext14-all-two-point-extensions | no 16-point (4,5)-set with h <= 9 contains a saturated extremal 14-point set (K46); depends on L004 and L001 | certificate | ACCEPTED, rounds 2 and 3 (after NEEDS-WORK round 1) | L005-ext14-all-two-point-extensions__referee__20261016T013746Z.md and __referee__20261016T013731Z.md; scout CLEAR: L005-ext14-all-two-point-extensions__scout__20261016T002432Z.md | [verified-here] |
| L006-ext12-all-two-point-extensions | no 14-point (4,5)-set with h <= 8 contains an extremal 12-point set; every 12-point subset of every extremal 14-point set has h = 8 (K48); depends on L002 and L001 (same analysis as L005) | certificate | ACCEPTED, rounds 2 and 3 (after NEEDS-WORK round 1) | L006-ext12-all-two-point-extensions__referee__20261016T083111Z.md and __referee__20261016T081040Z.md; scout CLEAR: L006-ext12-all-two-point-extensions__scout__20261016T070619Z.md | [verified-here] |
