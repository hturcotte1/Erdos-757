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

## Index (as of 2026-10-16 16:40 UTC)

Ids: `P###-slug` for lower-bound proofs, `L###-slug` for lemmas and certificates. No lower-bound proof (`CLAIM: c* >= r`) exists yet; `bash scripts/status.sh` prints `lower_bound_proofs: none`. Review files are in `results/reviews/`.

| id | statement | type | status | latest review | tag |
|---|---|---|---|---|---|
| L001-abase-two-point-extensions | every (4,5)-set A_base + {x,y} has h = 10 (K13) | certificate | ACCEPTED, round 4 | L001-abase-two-point-extensions__referee__20261014T095734Z.md | [verified-here] |
| L002-census-12-point-extremal-sets | exactly 54,243 twelve-point (4,5)-sets with h = 7 up to affine equivalence (K41) | certificate | ACCEPTED, round 3 | L002-census-12-point-extremal-sets__referee__20261014T152552Z.md; scout CLEAR: L002-census-12-point-extremal-sets__scout__20261014T171802Z.md (also covers L003 and K30, K31) | [verified-here] |
| L003-census-small-n-extremal-sets | saturated extremal class counts 1, 4, 66, 1262, 6644, 466961 for n = 6..11; infinitely many extremal sets for 4 <= n <= 11 (K43) | certificate | ACCEPTED, round 3 | L003-census-small-n-extremal-sets__referee__20261014T213511Z.md | [verified-here] |
| L004-census-14-point-extremal-sets | exactly 2,910 saturated (m = 12) 14-point (4,5)-sets with h = 8; the m = 11 case is open (K45) | certificate | ACCEPTED, round 1; completeness re-checked by sampling | L004-census-14-point-extremal-sets__referee__20261015T225426Z.md | [verified-here] |
| L005-ext14-all-two-point-extensions | no 16-point (4,5)-set with h <= 9 contains a saturated extremal 14-point set (K46); depends on L004 and L001 | certificate | ACCEPTED, rounds 2 and 3 (after NEEDS-WORK round 1) | L005-ext14-all-two-point-extensions__referee__20261016T013746Z.md and __referee__20261016T013731Z.md; scout CLEAR: L005-ext14-all-two-point-extensions__scout__20261016T002432Z.md | [verified-here] |
| L006-ext12-all-two-point-extensions | no 14-point (4,5)-set with h <= 8 contains an extremal 12-point set; every 12-point subset of every extremal 14-point set has h = 8 (K48); depends on L002 and L001 (same analysis as L005) | certificate | ACCEPTED, rounds 2 and 3 (after NEEDS-WORK round 1) | L006-ext12-all-two-point-extensions__referee__20261016T083111Z.md and __referee__20261016T081040Z.md; scout CLEAR: L006-ext12-all-two-point-extensions__scout__20261016T070619Z.md | [verified-here] |
