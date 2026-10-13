# Data

- Store censuses and search outputs as gzipped JSON lines: `data/<name>_n<k>.jsonl.gz`.
- Use one object per line, with exact values (ints, or strings "p/q").
- Keep every file under 50 MB; split by n if needed.
- Describe each file in this README: generator script, command, date, counts, schema.

## Files
(none yet)

- `forbidden_ordered_n7.json`: ordered linear midpoint-injective AP patterns for n<=7: per-n class counts
  (realizable / order-infeasible / forced extra AP / forced repeated difference) and the 44 minimal forbidden
  cores (S, relation) up to reflection. Schema: cores[]: {n, kind in order|extra_ap|diff, edges [[i,j,k]], relation}.
  Generator: `experiments/20261013-2257-forbidden-library/enumerate.py 7 data/forbidden_ordered_n7.json`
  (e757.realizability), 2026-10-13. Tag: [verified-here].
