VERDICT: ACCEPT WITH FIXES

# Referee report, round 3 (referee #5, fix check only): results/proofs/L018-red-universality.md, revision 821674c

Referee: referee subagent (Claude Opus 5.5), round 3, 2026-10-27, about 06:12-06:15 UTC. Scratch folder: experiments/referee/L018-round3/.

## Summary

Commit 821674c changes only results/proofs/L018-red-universality.md: 13 insertions and 10 deletions. It is the last commit touching the file, and the working tree equals it. I read every changed line in a word-level diff and matched each change to a round-2 request.

The edits are editorial:
- no theorem, lemma, proposition or corollary statement changed;
- no proof step changed;
- the only text added inside a proof is a citation sentence in Step 2.4.

What was applied:
- All three items of the opus review (N1, N2, N3), and also N4-N7 in substance.
- The fable editorial items (1)-(4), and its information item (5).
- The scout's two requests: the Chvátal–Hanson citation, which is correct, and a scope remark after Theorem 4, which is accurate.

One problem remains. The rewrite of the heuristic Insight paragraph (fix for N2) introduced a false factual clause: "whereas the census graphs other than these 17 do have such pairs". The census's own Red$_5$-free list contradicts it (details below). It sits in a [heuristic] paragraph and affects no proved statement. It is still a false statement, so the verdict is ACCEPT WITH FIXES and not ACCEPT. A one-line fix is given below.

## Item-by-item check

### Opus round-2 review (…__20261027T060330Z.md)

- **N1 (note after Corollary 7.2, line 223): APPLIED, CORRECT.**
  - The note now says that the open input at $n=29$ in Remark 7.3 is `cell(28,24,12,3)`. It adds that `cell(25,23,11,3)` is not an input there, because Remark 7.3 voids $(3,1,1)+(25,23,11)$ by its degree-count argument. I re-read that argument at line 225, and the note matches it.
  - The added remark about `cell_25_23_11_D4` is accurate. progress.tsv of experiments/20261027-0340-induction-n28-n29-f25 has `(25,23,11,4) 6 … 2026-10-27T05:52:00Z`. It also has a direct `(25,23,11,3) 0 … 05:52:37Z` entry, which the note could cite (optional).
- **N2 (Insight paragraph, line 236): APPLIED, but it introduced an error (Problem 1).** The internal contradiction is gone: the 17 graphs are now said to have only global (Red) pairs and, by definition, no local ones. The new trailing clause about "the census graphs other than these 17" is false.
- **N3 (DEPENDS ON honesty, lines 10 and 12): APPLIED, CORRECT.**
  - The L016 bullet now lists Corollary 7.2 and Remark 7.3.
  - The census/tight-cell bullet now says "no theorem of Sections 1-6 and 8", and names the exception: Corollary 7.2's hypothesis on `cell(27,20,11,3)` from experiments/20261027-0300-tight-cells-d4.
  - This is consistent with the rest of DEPENDS ON:
    - Theorem 8 lies in Section 7A, and its dependence on the refereed L013 lists is stated in the separate bullet at line 11;
    - Corollary 7.2 lies in Section 7B;
    - Theorem 3(c) uses the census only for validation.
- **N4 (STATUS precision): APPLIED.** The text now reads "no change to any theorem statement; the proof of Lemma 0.5 gained the case d >= 3".
  - Strictly, the missing case was $d\ge4$; step (1) was generalised from $d=3$ to $d\ge3$.
  - Cosmetic, optional.
- **N5 (Theorem 1 remark): APPLIED.** The wrong reference to Lemma 0.3 is gone. The uses are now given as Theorem 4.6 and minimal counterexamples, which are connected with at least two edges. That is correct. The two-word example was not added (optional).
- **N6 (GAP 2, "at least 26 vertices"): APPLIED** as "(not sharp; …)". This is acceptable.
- **N7 (Remark 5.4, the cell (25,23,11)): APPLIED, accurate.** The text now says the cell is empty with $\Delta\le3$ only by an unrefereed list. The degree-count fallback (at most one pendant) is kept, so the conclusion "P2 for $n\le26$" does not rely on the unrefereed list.

### Fable round-2 review (…__20261027T060823Z.md)

- **(1) Parenthetical on cell(25,23,11,3):** same fix as N1. APPLIED.
- **(2) Henning–Yeo "not used" versus its use as a filter (line 13): APPLIED, CORRECT.** The theorem is now described as a redundant filter in 7.2.1, 7.2.2, Remark 5.4 and Remark 7.3.
  - Remark 7.3 inherits the filter through "the same rules (`prune28.py 29`)".
  - In Remark 5.4 the filter is redundant by hand. For a tight cell, $\tau=(3n+2m)/11$, so $17\tau\le5n+3m$ is equivalent to $m\le4n$, which always holds.
  - For 7.2.1 and 7.2.2, referee 4 regenerated the lists with the filter off and got the same lists.
- **(3) STATUS precision:** same as N4. APPLIED, and "Submitted" is capitalised.
- **(4) Lemma 0.3 in the Theorem 1 remark:** same as N5. APPLIED.
- **(5) Information on cell(25,23,11,4):** recorded in Remark 5.4 and in the note after 7.2. APPLIED.

### Scout report (…__scout__20261027T061500Z.md)

- **Chvátal–Hanson citation: APPLIED, CORRECT.** It appears in DEPENDS ON (line 7, [published]) and in Step 2.4 (line 69, "[published, re-proved here]").
  - The reference is correct: V. Chvátal, D. Hanson, "Degrees and matchings", J. Combin. Theory Ser. B 20 (1976) 128–138.
  - The quoted consequence is right. The extremal function is $f(\nu,\Delta)=\nu\Delta+\lfloor\Delta/2\rfloor\lfloor\nu/\lceil\Delta/2\rceil\rfloor$. At $\Delta=3$ this gives $e\le3\nu+\lfloor\nu/2\rfloor\le7\nu/2$, i.e. $\nu\ge2|E|/7$, the bound of Step 2.4.
  - Step 2.4's Edmonds proof is untouched; the citation sentence was only prepended.
  - The scout's optional suggestion to cite Henning–Yeo EJC 2017 Prop. 9 for $\tau=m-\nu(G)$ was not taken up. That is not required.
- **Scope remark after Theorem 4 (line 119): APPLIED, ACCURATE.**
  - Theorem 4 gives, for every $R$, a connected $H\in C$ with $\Delta=2\le3$ and $n\ge4$ in which every (Red) pair has $|Z|>R$. Conjecture RU asks for a (Red) pair in exactly such graphs.
  - So no argument that produces (Red) pairs of bounded size, i.e. bounded-size reducible configurations or bounded-radius discharging, can prove RU. That is what the remark says, and it correctly adds that this is not a limit on all proofs.
  - Two attributions are slightly loose but acceptable:
    - "folklore" for the large-girth/tree-locality mechanism, attributed to the scout;
    - "appears new (scout: NOVELTY PARTIAL)". The scout's PARTIAL verdict was driven by the unread Henning–Yeo 2021 text, which concerns item (2b), not Theorem 4. Still, the scout did say the Theorem 4 statement is new "to my searching".

## Problems remaining

1. **(Minor; introduced by 821674c; heuristic paragraph, no theorem affected.)** The Insight paragraph (line 236) ends its first sentence with "whereas the census graphs other than these 17 do have such pairs", meaning (Red) pairs with $|Z|\le5$. This is false.
   - experiments/20261027-0230-red-config/redk5_free_graphs.txt.gz lists 2,917 connected census members of $C$ with $\Delta\le3$ and no (Red) pair with $|Z|\le5$.
   - I recomputed $\tau$ and the slack of every one of them with my own brute force: experiments/referee/L018-round3/red5_scope.py, output red5_scope_output.txt.
   - Exactly 17 have $9\le n\le14$ and slack $\le5$: one (11,7,4), eight (12,10,5), seven (13,10,5) and one (13,9,5). This matches Proposition 8.2 and independently confirms its count.
   - Of the rest, 2,899 have slack $\ge6$ (2 at $n=9$, 2 at 11, 55 at 12, 828 at 13, 2,012 at 14), and the last is the single edge (3,1,1).
   - The census README (item 4) itself says that the Red$_k$-free graphs are almost all high-slack.
   - **Fix:** replace the clause with "whereas every other census graph with $9\le n\le14$ and slack $\le5$ does have such a pair (Proposition 8.2; the other Red$_5$-free census graphs, 2,899 of them, all have slack $\ge6$, apart from the single edge)". Alternatively, drop the clause.
2. **(Cosmetic, optional.)**
   - STATUS: "gained the case d >= 3" would be exact as "now treats $d\ge4$ (step (1) generalised to $d\ge3$)".
   - The note after 7.2 cites progress.tsv for the `cell_25_23_11_D4` export. The same file also records `(25,23,11,3) 0` directly at 05:52:37Z, which is the more direct evidence.

No other change is needed. Every other round-2 item is applied correctly, and nothing else in the certificate was altered.

## Checks performed

1. Diff audit:
   - `git show --stat 821674c`: one file, +13/−10.
   - `git log -- results/proofs/L018-red-universality.md`: 821674c is the latest commit.
   - `git diff 821674c HEAD -- …`: empty.
   - `git show 821674c --word-diff=plain`: 12 changed or added lines (STATUS; DEPENDS ON lines 7, 10, 12, 13; Theorem 1 remark; Step 2.4; scope remark after Theorem 4; Remark 5.4; the note after 7.2; Insight; GAP 2 (M1)). Each was matched to a request above.
2. Re-read in context: Conjecture RU (0.3), Theorem 4, Remark 4.1, Remark 5.4, Theorem 8 and Steps 8.1-8.4, Remark 7.3, Proposition 8.2, the Insight paragraph, and the section headers (Theorem 8 is in §7A, Corollary 7.2 in §7B).
3. `grep` of experiments/20261027-0340-induction-n28-n29-f25/progress.tsv:
   - `(25,23,11,4) 6 … 05:52:00Z`;
   - `(25,23,11,3) 0 … 05:52:37Z`;
   - the lists `cell_25_23_11_D4.txt` and `out/cells/cell_25_23_11_D3.txt` both exist.
4. `timeout 900 nice -n 10 python3 experiments/referee/L018-round3/red5_scope.py experiments/20261027-0230-red-config/redk5_free_graphs.txt.gz`. Output, per $(n,\ \text{slack}\le5)$: `(3,T)1 (9,F)2 (11,F)2 (11,T)1 (12,F)55 (12,T)8 (13,F)828 (13,T)8 (14,F)2012`. The low-slack list is exactly the 17 graphs of Proposition 8.2 plus (3,1,1).
5. Hand checks:
   - the Chvátal–Hanson formula at $\Delta=3$;
   - redundancy of the Henning–Yeo filter on tight cells ($m\le4n$);
   - consistency of the scope remark with the statements of Theorem 4 and RU.

## Independence statement

- I read the three round-2 reports, as instructed, and no other review of L018 or any referee scratch folder.
- The only code I ran, experiments/referee/L018-round3/red5_scope.py, is my own: a brute-force $\tau$. It imports nothing from e757/, judge/ or the prover folders.
- I used the census list as input data only.
- I modified no file except this review and my scratch folder.
