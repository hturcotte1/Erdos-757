# Proof files

One file per proof, certificate or lemma: `results/proofs/<id>.md`, where `<id>` is short, for
example `P001-degree-discharging`. Reviews refer to the same id.

## Template

```
# <title>
CLAIM: c* >= 5/9
TYPE: lower-bound | lemma | certificate
STATUS: draft | submitted
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
