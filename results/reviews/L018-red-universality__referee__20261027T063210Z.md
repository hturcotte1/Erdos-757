VERDICT: ACCEPT WITH FIXES

# Referee report, round 4 (referee #6, fix check only): results/proofs/L018-red-universality.md, revision fd05f0a

Referee: referee subagent (Claude Opus 5.5), round 4, 2026-10-27, about 06:25-06:35 UTC.
- No scratch folder in the repository. My one recount script is in the session scratchpad, outside the repository.
- As instructed, I modified no file except this review.

**Verdict scale.** The workflow asks for ACCEPT or ACCEPT WITH FIXES. On the generic referee scale (ACCEPT / REJECT / NEEDS-WORK) this is NEEDS-WORK of the mildest kind:
- one line (STATUS) and two words (Insight paragraph) need to change;
- no theorem, proof step or conclusion is affected.

## Summary

Commit fd05f0a changes only the certificate, and only three lines: STATUS (line 4), Remark 5.4 (line 160) and the Insight paragraph (line 236). No later commit touches the file, and the working tree equals fd05f0a. No statement or proof step changed.

**The required round-3 item is applied.** The Insight paragraph's main clause is now correct. Among the census graphs with $9\le n\le14$ and slack $\le5$, exactly the 17 graphs of Proposition 8.2 have no (Red) pair with $|Z|\le5$. I reproduced this with my own code, using a different method from round 3. The new parenthetical "the 2,899 other Red5-free census graphs of redk5_free_graphs.txt.gz all have slack $\ge6$" is exact only within the scope $9\le n\le14$:
- the file has 2,900 graphs other than the 17;
- one of them, the single edge (3,1,1), has slack 0;
- round 3's suggested wording ended with "apart from the single edge", and that qualifier was dropped.

**The optional progress.tsv citation (Remark 5.4) is accurate.**

**The new STATUS line is not fully accurate.**
- It says Henning–Yeo citations were added at the scout's request. The scout's Henning–Yeo recommendation (EJC 2017 Prop. 9 at Step 2.2) was not applied.
- It calls all the fixes "editorial only". Round 1 included two one-line repairs to mathematical text: a missing case in the proof of Lemma 0.5, and a wrong justification in Step 4.5.
- It drops the conditions under which Theorem 8, Proposition 6.2 and Corollary 7.2 are proved: Conjecture T', Conjecture P2, and two unrefereed cell lists. As a result, "Corollary 7.2 accepted as proved" reads as if I11 at $n=28$ were established, which it is not.
- It drops "I11 is NOT proved" and "PARTIAL".

A one-line replacement is given below.

## Item check

### A. Round-3 required item: Insight paragraph (line 236)

**Status: APPLIED. The main clause is correct; the parenthetical needs a scope qualifier.**

New text: "whereas, among the census graphs with $9\le n\le14$ and $\mathrm{slack}\le5$, exactly these 17 have no (Red) pair with $|Z|\le5$ (the 2,899 other Red5-free census graphs of redk5_free_graphs.txt.gz all have $\mathrm{slack}\ge6$; the referee's independent count is experiments/referee/L018-round3/red5_scope.py)."

**Main clause.**
- It is the statement of Proposition 8.2 (line 231), with the same scope: connected members of $C$ with $\Delta\le3$, $9\le n\le14$, slack $\le5$; exactly 17; no (Red) pair with $|Z|\le5$.
- It therefore adds no new claim and replaces the false round-2 clause correctly.

**Independent recount.**
- Input: experiments/20261027-0230-red-config/redk5_free_graphs.txt.gz, which has 2,918 lines: 1 header and 2,917 graphs.
- Method: my own script computes $\tau$ by branching on an uncovered edge. Round 3 used subset enumeration.
- Output per $(n,\ \text{slack}\le5)$: `(3,T)1 (9,F)2 (11,F)2 (11,T)1 (12,F)55 (12,T)8 (13,F)828 (13,T)8 (14,F)2012`. This is identical to experiments/referee/L018-round3/red5_scope_output.txt.
- The low-slack list is:
  - $(3,1,1,\text{slack }0)$;
  - $(11,7,4,3)$;
  - eight $(12,10,5,1)$;
  - one $(13,9,5,2)$;
  - seven $(13,10,5,4)$.
- This is exactly the 17 graphs of Proposition 8.2 plus the single edge.

**What this means for the parenthetical.**
- Within $9\le n\le14$, the other Red5-free graphs number $2+2+55+828+2012=2{,}899$, and all have slack $\ge6$. The parenthetical is therefore correct if the scope $9\le n\le14$ of the preceding clause is carried over.
- "of redk5_free_graphs.txt.gz" refers to the whole file. Read that way, it is off by one graph: there are 2,900 others, and the single edge has slack 0.

**Fix (two words):** "the 2,899 other Red5-free census graphs **with $9\le n\le14$** of redk5_free_graphs.txt.gz". Alternatively, append "; the only other graph in the file is the single edge (3,1,1), slack 0".

**Other checks on this item.**
- The cited script experiments/referee/L018-round3/red5_scope.py exists and does what is claimed: exact $\tau$ by subset enumeration, slack $3n+2m-11\tau$, grouping by $n$ and slack $\le5$.
- A cosmetic point outside the certificate, which needs no action: the script's second printed label says "with n<=10", but the list covers all $n$.
- The [heuristic] tag is kept, and the rest of the paragraph is unchanged.

### B. Round-3 optional item: direct citation of progress.tsv

**Status: APPLIED, ACCURATE.**
- It was applied in Remark 5.4 (line 160), not in the note after Corollary 7.2 (line 223), which is unchanged.
- experiments/20261027-0340-induction-n28-n29-f25/progress.tsv line 41 reads `(25,23,11,3)	0	15429	4738908	21.5	0	0	recurse	2026-10-27T05:52:37Z`.
- out/cells/cell_25_23_11_D3.txt contains only its INFO record and no class line.
- The placement is appropriate: Remark 5.4 is where the emptiness of `cell(25,23,11,3)` is quoted as evidence.
- Its conclusion for $n\le26$ still rests on the degree-count fallback, so it does not depend on this unrefereed entry.

### C. New STATUS line (line 4), claim by claim

- **"referee fable ACCEPT in rounds 1 and 2": correct.**
  - …__referee__20261027T051820Z.md: Fable 5.1, ACCEPT, on 57f10ba.
  - …__referee__20261027T060823Z.md: Fable 5.1, ACCEPT, on e187bd7.
- **"referee opus ACCEPT WITH FIXES in rounds 1-3": correct.** The three reviews are …054329Z.md, …060330Z.md and …061449Z.md, all by Opus 5.5 and all ACCEPT WITH FIXES.
- **"editorial only": NOT ACCURATE.**
  - The round-1 opus review (…054329Z.md) raised two points about mathematical text:
    - Problem 1, "Lemma 0.5 (TP) has a gap": the case $d_K(p)\ge4$ was not treated.
    - Problem 4: a justification in Step 4.5 "does not hold in general".
  - Both were repaired in e187bd7. The round-2 fable review confirms this: "The only changes to mathematical text are the completion of the case analysis of Lemma 0.5 … and the corrected one-line justification in Step 4.5".
  - Both repairs are small and change no statement. The previous STATUS recorded this ("the proof of Lemma 0.5 gained the case d >= 3"); the new wording loses it.
- **"all applied": correct for every required item, once the scope qualifier of A is added.**
  - Of the two round-3 optional items, the STATUS-wording one is moot because that clause was removed, and the other is applied (B).
- **"scout PARTIAL: Chvatal-Hanson and HY citations added": NOT ACCURATE.**
  - Under "Recommendations to the main agent", the scout report (…__scout__20261027T061500Z.md) asks for two citations:
    1. Chvátal–Hanson 1976. This was applied, in DEPENDS ON line 7 and in Step 2.4.
    2. "Henning-Yeo EJC 24(2) P2.50 Prop. 9 for tau = m - nu(G)", for Step 2.2. This was **not** added. Step 2.2 (line 70) cites nothing, and a grep of the certificate finds no "2017", "EJC", "Electron" or "Prop. 9".
  - The only Henning–Yeo change in any revision is the DEPENDS ON sentence describing K8 as a redundant filter (line 13). That change answered fable round-2 item (2), not the scout. K8 was already cited in 7.2.1 in the submitted version.
  - Round 3 had recorded that this recommendation "was not taken up". The STATUS now contradicts that review.
- **"Theorems 1-8, Corollary 7.2, Propositions 6.2/8.1 accepted as proved": true of the statements as written, but the conditions must be restated in STATUS.**
  - Each of these statements carries its hypotheses:
    - Proposition 6.2 (line 179): "Assume Conjecture P2".
    - Theorem 8 (line 199): "If Conjecture T' holds".
    - Corollary 7.2 (line 214): "Assume … `cell(27,15,10,3)` and `cell(27,20,11,3)` are empty (… unrefereed runs …)".
  - The STATUS line itself no longer says so; the previous STATUS did.
  - STATE, LEDGER and known_results rows are written from this line. "Corollary 7.2 accepted as proved" invites the record "I11 at $n=28$ proved", which is not established, because two cell lists are unrefereed.
  - That Theorems 3(c) and 8 are computer-assisted is still stated in CLAIM-TYPE (line 2), which is enough.
- **"Prop. 8.2 is an unrefereed census computation": accurate**, and consistent with its tag at line 231. Its count of 17 has been reproduced independently twice (round 3, and here), but the census itself is still unrefereed, so the wording stands.
- **"Conjecture RU itself remains OPEN with GAPs 1-2 marked": accurate.** GAP 1 is at line 240 and GAP 2 at line 242.
  - The previous STATUS also said "I11 is NOT proved". That is now only implicit, through GAP 2 and CLAIM-TYPE.
  - It is the certificate's most important negative statement and should be restored.
- **"ACCEPTED" without "PARTIAL".** CLAIM-TYPE still says "partial results". STATUS should say "ACCEPTED as a PARTIAL certificate", so that the acceptance is not read as covering RU or I11.
- **"revised 05:44, 06:10 and 06:23Z": cosmetic.** The commits are e187bd7 at 05:45:29, 821674c at 06:11:14 and fd05f0a at 06:23:27, and the previous STATUS said 05:45Z and 06:11Z.
- **No effect on goal clauses.** L018 has no `CLAIM: c* >= r` line (checked by grep), so scripts/status.py ignores it for clause B whatever the verdict.

### D. Nothing else changed: CONFIRMED

- `git show --stat fd05f0a`: one file, +3/−3.
- `git show fd05f0a --word-diff=plain`: exactly the three lines above.
- `git log -- results/proofs/L018-red-universality.md`: fd05f0a is the latest commit on the file.
- `git diff fd05f0a HEAD` and `git diff HEAD` on the file: both empty.
- The later commit f23934a does not touch the file.

## What remains, exactly

1. **STATUS (line 4).** Correct the three inaccuracies of C ("editorial only"; "HY citations added"; the dropped conditions together with "I11 is NOT proved" and "PARTIAL"). Suggested text, with the round-4 verdict filled in:
   "STATUS: ACCEPTED 2026-10-27 as a PARTIAL certificate (referee fable ACCEPT in rounds 1 and 2; referee opus ACCEPT WITH FIXES in rounds 1-3 [and round 4: …]; all fixes editorial except two one-line proof repairs in round 1, Lemma 0.5 (case $d_K(p)\ge4$) and the justification in Step 4.5, no statement changed; scout PARTIAL: Chvátal–Hanson citation added). Accepted as proved: Theorems 1-8 (Theorem 8 conditional on Conjecture T'; computer-assisted parts as in CLAIM-TYPE), Propositions 6.2 (conditional on Conjecture P2) and 8.1, Corollary 7.2 (conditional on the two unrefereed cell lists `cell(27,15,10,3)`, `cell(27,20,11,3)`, so I11 at $n=28$ is not established). Proposition 8.2 is an unrefereed census computation. Conjecture RU is NOT proved and I11 is NOT proved (GAP 1, GAP 2). Submitted 2026-10-27; revised 05:45, 06:11 and 06:23Z."
   - Either keep "Chvátal–Hanson citation added" alone, as above, or actually add the Henning–Yeo citation at Step 2.2.
   - If it is added, note the hypotheses. Prop. 9 is stated for $\mathcal H_k$, defined as "connected, linear, $k$-uniform hypergraphs with maximum degree 2" (Definition 5, p. 4 of kb/literature/papers/henning_yeo_ejc_2017.pdf). Step 2.2 allows disconnected graphs, isolated vertices and $\Delta\le1$ components, so it should be cited as "the connected case with $\Delta=2$ is Henning–Yeo, Electron. J. Combin. 24(2) (2017) P2.50, Prop. 9; the general case follows componentwise".
2. **Insight paragraph (line 236).** Add the scope "with $9\le n\le14$" to the parenthetical, as in A, or mention the single edge (3,1,1).

Optional:
- the note after Corollary 7.2 (line 223) could also cite the direct `(25,23,11,3)	0` entry, which is now only in Remark 5.4;
- "Chvatal" should be "Chvátal".

Once items 1 and 2 are made as stated, with no other change, this round would be an ACCEPT. A fix check needs only a word diff of line 4 and line 236.

## Checks performed

1. Change audit:
   - `git show --stat fd05f0a` and `git show fd05f0a --word-diff=plain --unified=0`;
   - `git log --date=iso-strict -- results/proofs/L018-red-universality.md`, which gives the commit times quoted above;
   - `git diff fd05f0a HEAD` and `git diff HEAD` on the file: both empty;
   - `git show --stat f23934a`: the certificate is not touched.
2. Read the five earlier referee reviews and the scout review: first lines, the model of each referee, round-1 Problems 1 and 4, and the scout's "Recommendations to the main agent".
3. `grep` of the certificate for Henning, 2017, EJC, Electron and Prop. 9: the only Henning–Yeo mentions are at lines 4, 13 and 216.
   - Read Step 2.2 (line 70) and the statements at lines 179, 199, 214 and 231.
   - Confirmed there is no `^CLAIM:` line.
4. `pdftotext kb/literature/papers/henning_yeo_ejc_2017.pdf` gives:
   - Prop. 9: "If $H\in\mathcal H_k$ … then $\alpha'(G_H)=|E(H)|-\tau(H)$";
   - Definition 5: $\mathcal H_k$ is the class of connected, linear, $k$-uniform hypergraphs with maximum degree 2.
5. `grep '(25,23,11' experiments/20261027-0340-induction-n28-n29-f25/progress.tsv` gives lines 39 (`(25,23,11,4) 6 … 05:52:00Z`) and 41 (`(25,23,11,3) 0 … 05:52:37Z`). `cat out/cells/cell_25_23_11_D3.txt` shows the INFO record only.
6. `zcat experiments/20261027-0230-red-config/redk5_free_graphs.txt.gz | wc -l` gives 2918 (1 header line and 2,917 graphs).
7. Recount: `timeout 600 nice -n 10 python3 -I <scratchpad>/r4/recount.py experiments/20261027-0230-red-config/redk5_free_graphs.txt.gz`. The script is my own and computes $\tau$ by branching on an uncovered edge. Output:
   - `total 2917`;
   - per-$(n,\text{slack}\le5)$ counts identical to round 3;
   - low-slack list = the 17 graphs of Proposition 8.2 plus (3,1,1);
   - `others (not low-slack, 9<=n<=14): 2899`;
   - `others overall (all minus low-slack 9..14): 2900`.
8. Read scripts/status.py (lines 1-30 and 175-226): only `CLAIM: c* >= r` proofs enter clause B.

## Independence statement

- I read, as permitted, the five earlier referee reviews of L018 and its scout review. I read the certificate's diff and text and the data files it cites.
- My one computation is a script I wrote this session. It imports only gzip, sys and collections, and nothing from e757/, judge/, experiments/prover/ or any other referee's folder. The census list was used as input data only.
- I did not modify the certificate, or any file other than this review.
