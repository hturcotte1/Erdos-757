# Reviews (written only by the referee and scout subagents)

File names: `<id>__referee__<YYYYMMDDTHHMMSSZ>.md` and `<id>__scout__<YYYYMMDDTHHMMSSZ>.md`.

The first line must be exactly one of:
- referee: `VERDICT: ACCEPT`, `VERDICT: REJECT` or `VERDICT: NEEDS-WORK`;
- scout: `NOVELTY: CLEAR`, `NOVELTY: PRIOR-WORK` or `NOVELTY: UNSURE`.

`scripts/status.py` uses only the latest review(s) for each id. The main agent never writes here.
