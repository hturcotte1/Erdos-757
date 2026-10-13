---
name: verify-claim
description: Use whenever a result might be real - a (4,5)-set with ratio below 4/7, a proof of a lower bound above 9/17, an exact value of f(n), a certificate from an exhaustive search, or a lemma you plan to build on. Runs the judge, independent referee reviews and a novelty check, then records the result.
---

# Verify a claim

Stop other work until this is done. Never write review files yourself.

## A. Construction (a set)

1. Save and judge it:
   `python3 scripts/new_claim.py --slug <short-name> --set "<comma-separated values>" --notes "<how found>"`.
   This writes `results/claims/<id>.json` (only if the judge passes) and prints the JUDGE line.
2. If the line says `PASS NEW-RECORD`: spawn the `referee` subagent in the foreground with only
   "Referee claim <id>: results/claims/<id>.json".
3. Spawn `scout` for a novelty check of <id> (informational for constructions).
4. On `VERDICT: ACCEPT`:
   - add a row to results/LEDGER.md, and to kb/known_results.md tagged [verified-here];
   - add the set to `KNOWN_UPPER` in e757/fn_bounds.py, add a test, and run pytest;
   - write results/FINAL_REPORT.md;
   - commit, push, and run `bash scripts/status.sh`.
5. On REJECT or NEEDS-WORK: record it in journal/LOG.md, fix or discard, and re-verify from step 1
   under a new id.

## B. Proof (lower bound or lemma)

1. Write `results/proofs/<id>.md` from the template in results/proofs/README.md. A lower-bound
   proof needs a line exactly like `CLAIM: c* >= 5/9`.
2. Run the `falsifier` on every new inequality or lemma in the proof. Fix anything it breaks.
3. Spawn `referee` #1 (fresh, foreground). Address its findings. If the proof changes
   substantively, earlier ACCEPTs no longer count, because status.sh uses the latest reviews.
4. Spawn `referee` #2 (fresh, separate run). Give it only the id and path; do not mention
   referee #1's review.
5. Spawn `scout` for a novelty check.
6. When the two latest referee reviews are ACCEPT and the latest scout review is CLEAR:
   - update results/LEDGER.md and kb/known_results.md;
   - write results/FINAL_REPORT.md;
   - commit, push, and run status.sh.

## C. Certificate (exact value such as f(16) = 10, or a census)

1. Put the code in e757/ or experiments/<id>/ and write `results/proofs/<id>.md` explaining:
   - the search space;
   - the symmetry breaking and why it is sound;
   - the pruning rules and why they are sound;
   - exact counts and run times;
   - how to reproduce it.
2. A small independent re-implementation must agree on smaller sizes.
3. Run the referee as in B. Record the result in results/LEDGER.md tagged [verified-here]
   (certificate).

## Notes

- A referee review counts for status.sh only if its file starts with `VERDICT: ACCEPT`, and only
  the latest review(s) for that id count.
- A new record should also update the CLAIM in results/FINAL_REPORT.md with the exact ratio and the
  gluing argument (Ma–Tang Lemma 3.6) that turns one finite set into a bound on $c_*$.
