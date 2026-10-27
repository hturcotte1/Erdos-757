VERDICT: NEEDS-WORK

**Verdict mapping.** In the commissioning workflow's vocabulary this is **ACCEPT WITH FIXES**.
- My referee rules allow only ACCEPT, NEEDS-WORK or REJECT on the first line, and they reserve ACCEPT for a document in which no problem remains.
- Two editorial items remain (R1, R2 below). Both were introduced by the round-2 edit itself, and each is a one-sentence rewording.
- There is no mathematical problem, and no theorem statement or proof step changed in substance.
- (`scripts/status.py` tests the first line by exact equality with `VERDICT: ACCEPT`, so this line cannot be misread as an acceptance.)

Referee #5, ROUND 3 (fix check only), of results/proofs/L020-joint-induction-i11.md at commit c85ce6d.
- The working tree equals HEAD for this file; file mtime 07:58:24 UTC.
- Scratch folder: experiments/referee/L020-round3-fixcheck/.

## Summary

Commit c85ce6d applies every item requested by the two round-2 reviews (opus 20261027T074931Z, NEEDS-WORK = ACCEPT WITH FIXES; fable 20261027T075547Z, ACCEPT WITH FIXES), and applies them correctly in substance:
- the characterisation is now Remark 1.4, with a correct derivation sketch and an honest tag;
- the Theorem 1 and C8 count attributions match the reviews;
- the "Verification status" paragraph is no longer self-contradictory;
- the lower-bound caveat says "among others" and lists the four sources (a), (b), (f), (i);
- Step 5.2 says "at most 5". My own code confirms the new parenthetical: 21 of the 95 type-(2,2,1) NC pairs have 4 attachment vertices;
- the remainder slacks in Open problem 2 are exactly those of the fable review;
- the C3 phrasing is fixed;
- in DEPENDS ON, L019 is now K68 and "Proposition 9 (next item)" is correct;
- the Theorem 2 tag reads "[derived-here from published results ...]" in both places;
- the STATUS time stamps match the commits.

The diff touches only lines 4, 10–11, 32, 34, 37, 71, 85–86 (new), 116, 130, 140 and 164:
- No theorem statement changed in substance.
- In Theorem 1, apart from the removal of the characterisation sentence, only the attribution clause, the caveat and one new parenthetical changed. The main claim, $K_{29}$, the construction, the counts and (i)–(iii) are verbatim.
- The only proof step that changed is the wording of 5.2.

So Theorem 1 as now stated is what both rounds verified: at least 45 pairwise non-isomorphic connected members of $C$ with $(29,23,12)$, $\Delta=3$ and slack 1, with the lower-bound caveat.

Two residues of the edit remain:
- **R1.** The last sentence of the "Verification status" paragraph credits *both* round-2 referees with rebuilding the pattern-(e) gluings. Only the fable round-2 referee did; Remark 1.4 itself has this right.
- **R2.** A parenthetical left inside the Theorem 1 statement ("For the pattern-(e) vertices the 45 is exact given the lists, Remark 1.4") restates half of the characterisation. This contradicts Remark 1.4's own sentence "This is not part of the statement of Theorem 1".

## Checks performed (commands and outputs)

1. **The diff.**
   - `git log --oneline -- results/proofs/L020-joint-induction-i11.md` gives 09e40f5, db005b4, ef5c9dc, c85ce6d.
   - `git status`: the file is clean.
   - `git diff --unified=0 ef5c9dc c85ce6d -- <file>` gives hunks at lines 4, 10–11, 32, 34, 37, 71, 84+2 (Remark 1.4), 116, 130, 140 and 164, and nothing else. Every hunk was read in the context of the full current file.
2. **Reviews read.**
   - Round 1: opus 072810Z, fable 064109Z.
   - Round 2: opus 074931Z, fable 075547Z.
   - I did not read the scout review.
3. **Attribution evidence.** All files were read as data.
   - Opus round 2: `ls experiments/referee/L020-round2-opus/` lists bcfg_recount, hgr2, k29_profile, patt, prop6_check, prop6_near, sanity, t3_spot and v28. There is no gluing code: `grep -l -E "glu|pattern_e|econf" *.py` returns nothing.
   - `bcfg_recount_output.txt` only counts e-configured classes (`cell_20_15_8 ... e-config 24`).
   - `k29_profile_output.txt` gives `e853+20158 classes with >=1: 45`, `theta ... {3: 45}`, `f18137+1074 ... 27` and `bE1+251910 ... 31`.
   - Fable round 2: `econf_count_output.txt` gives `gluings 120 not (in C, Delta<=3, tau 12, connected): 0 distinct invariants 45` and `equal to the gluing invariant set: True`.
   - Opus round 1, items 3–6: `t1_roles_triples` covers (i)–(iii) on all 45; `glue_check` rebuilds the 120 gluings from the stored lists into 45 classes; `theta_rebuild` gives 564 graphs hitting the 45 and nothing else; `t3_perclass` gives 27 and 31.
   - Fable round 1, items 1, 2 and 6: (ii) for $K_{29}$; nauty `labelg` on the 45; "no NC pair" in all 45; the $\Theta$ re-run gives exactly the 45.
4. **L019 status.** `grep -n "K68\|L019" results/LEDGER.md` shows row K68: L019 proved parts [verified-here]. The L019 STATUS line reads "ACCEPTED 2026-10-27 as a PARTIAL certificate".
5. **The (27,20,11,3) remark.** `grep "27,20,11" results/proofs/L017-...md` shows L017 line 7 and Remark 13.6: "cell(27,20,11,3) = ∅", from an unrefereed worker run. This matches caveat item (i).
6. **Own code** (stdlib only): `timeout 900 nice -n 10 python3 prop6_attach.py`, output in `prop6_attach_output.txt`:
   - `graphs 483 NC pairs 204 types {(1,1,0): 1, (1,1,1): 3, (1,2,0): 1, (1,2,1): 104, (2,2,1): 95}`. This equals C7.
   - `type (2,2,1): number of vertices other than x,y in edges meeting {x,y}: {4: 21, 5: 74}`. This equals the new parenthetical of Step 5.2.
   - `tau mismatches 0`.
   - Method: exact $\tau$ by memoised branching on edge bitmasks; an NC pair is a pair with $\tau(K-x-y)\ne\tau(K)-2$.
7. **Time stamps.**
   - `git show -s --format=%ci` gives c85ce6d at 07:58:35 and ef5c9dc at 07:31:03.
   - `grep VERDICT scripts/status.py` shows an exact-equality test of the first line.

## Item-by-item check of the round-2 requests

1. **The characterisation moved out of Theorem 1** (opus-2 P1). APPLIED, as Remark 1.4, placed after Step 1.3, with residue R2. I checked the derivation sketch step by step:
   - **$\tau(K-v)$.** $K-v$ has 28 vertices and 20 edges, so $\tau(K-v)\in\{11,12\}$ by 0.1. If $\tau(K-v)=12$, then $s(K-v)=84+40-132=-8$. But both components have at most 25 vertices, so each has slack $\ge0$ by L016, and the component slacks sum to $s(K-v)$. Hence $\tau(K-v)=11$ and the slacks sum to 3.
   - **Free choice and Step 3.7(e).** Free choice follows from (U), using I11 for $F_i-x$. ($\star$) holds because $\tau(K-v)=\tau(K)-1$. Step 3.7(e) uses only these facts, so both components carry e-configurations.
   - **Tight components are excluded.** The four non-empty tight $\Delta\le3$ cells with at most 24 vertices have no e-configuration (C3; re-checked by both round-1 referees). The stored list of $(25,12,9)$ is empty (fable round 1, cells_check). Any 25-vertex component leaves $E_1$, which has slack 0 and no e-configuration.
   - **The cells.** So the slacks are $\{1,2\}$. All slack-1 cells with at most 25 vertices are stored, and only $(8,5,3)$ carries e-configurations. The other component has $m=23-3-5=15$, and $60+30-11\tau=2$ gives $\tau=8$, so it lies in $(20,15,8)$.
   - **Completeness.** C1 enumerates all e-configurations of the 953 + 2 representatives, so every such $K$ is one of the 120 gluings, that is, one of the 45 classes.
   - **The $\Theta$ clause.** The triangle is the unique $(6,3,2)$ graph, the $(22,17,9,3)$ list is complete, and C9 / theta_rebuild enumerate every $\Theta$-gluing.
   - **The tag.** "[derived-here, unrefereed computation inputs]" is honest: the sketch uses L016, the refereed lists, the role facts of L017 C5/C3 (unrefereed computations) and C1. "Nothing in the proof of Theorem 1 uses it" is true: Steps 1.1–1.3 do not refer to it.
   - **The remark's attributions** are accurate (item 3 of the checks):
     - "rebuilt from the stored lists by the opus round-1 and the fable round-2 referees";
     - "isomorphism by nauty in round 1" (fable round 1, `labelg`);
     - "$\Theta$-gluings re-run by both round-1 referees";
     - "re-derived independently by both round-2 referees" (opus-2 gives an 8-step derivation; fable-2 "re-derived by hand").
2. **Attribution of the counts** (fable-2 P1, opus-2 P4). APPLIED. Theorem 1 now says "counts computed by the opus round-1 referee and re-verified independently by both round-2 referees", and C8 says the same. This is accurate: opus-1 `t3_perclass`, opus-2 `k29_profile`, fable-2 `patterns45`.
3. **"Verification status" paragraph** (fable-2 P2). APPLIED; it is no longer self-contradictory.
   - (ii) is verified for $K_{29}$ by fable-1, and for all 45 by opus-1 with code independent of `triples_K29.py`, so it rests on two independent codes for all 45.
   - (iii) is verified for all 45 by opus-1.
   - Both statements match the reviews.
   - The last sentence is R1.
4. **Lower-bound caveat** (fable-2 P3, opus-2 P3). APPLIED in Theorem 1 and in C8: "among others", followed by
   - (a) $(28,20,11,3)$;
   - (b) the unsampled part of $(25,19,10,3)+E_1$;
   - (f) the same 3,000-class sample for f-configurations;
   - (i) (i1)–(i3) with tight components on 27 vertices.

   I checked the arithmetic of (i):
   - Theorem 3(ii) with $Y\ne\emptyset$ forces $s(K)=1$ and tight components.
   - $\tau(K-v)=12$ is impossible here: the component slacks would sum to $-11$ on at most 27 vertices each, contrary to L016.
   - $(27,20,11)$ has $s=81+40-121=0$, and $(10,7,4)\sqcup(17,13,7)$ has 27 vertices, 20 edges and $\tau=11$.

   Remark, no fix required: opus-2 argued that (i2) and (i3) are in fact excluded given the lists and the role facts, so listing $(10,7,4)\sqcup(17,13,7)$ is merely over-cautious; the sentence says "could".
5. **Step 5.2** (opus-2 P2). APPLIED: "at most $1+2+2=5$ … (the two unshared edges may meet in a vertex; 21 of the 95 … have only 4)". By linearity the third vertex of the shared edge differs from the other four, and the two unshared edges share at most one vertex, so the step is correct. The count is confirmed by my own code (check 6). Proposition 6 is unchanged.
6. **Open problem 2** (fable-2 P6, opus-2 P5). APPLIED. From $s(K-x-y)=s(K)+5-2|\partial|$:
   - types (1,1,0) and (1,2,1) have $|\partial|=2$, giving $s+1$;
   - type (1,2,0) has $|\partial|=3$, which forces $s=1$ and remainder slack 0;
   - type (1,1,1) has $|\partial|=1$, giving $s+3$;
   - so the range is 0–4, exactly as in both reviews.

   One notation point is cosmetic (R3).
7. **C3 phrasing** (opus-2 P6). APPLIED: "none in $(16,10,6)$ [16 classes], $(9,4,3)$ [1 class] or $(23,16,9)$ [178 classes]". This is consistent with opus-2 `bcfg_recount_output.txt`.
8. **DEPENDS ON** (fable-2 P4, P5; opus-2 P8). APPLIED.
   - L019 reads "[ACCEPTED as a PARTIAL certificate, K68]", which matches LEDGER K68 and the L019 STATUS line. The parts used here (Theorems 2, 3 and 4(b)) are among those accepted as proved.
   - "Proposition 9 (next item)" is correct.
   - The L016, L013, L017 and L018 entries are unchanged; they were checked in round 2.
9. **Theorem 2 tag** (fable-2 P7). APPLIED, both in the theorem bracket and in the Tags line. The statement and the proof (Lemma 2.1, 2.2–2.3) are unchanged.
10. **STATUS line** (fable-2 P4, opus-2 P8). APPLIED: "revised 07:58 UTC after referee round 2 …; earlier revision 07:31 UTC after referee round 1; submitted 06:13".
    - The commit is at 07:58:35 and the mtime is 07:58:24; ef5c9dc is at 07:31:03.
    - The round-2 verdicts are quoted as on disk.

## No change of substance (confirmation requested)

**Theorem 1.** Against ef5c9dc, the differences are exactly:
- the attribution clause;
- the deleted "Characterisation: …" sentence;
- the expanded caveat;
- the new parenthetical (R2).

Everything else is verbatim:
- the main assertion: at least 45 pairwise non-isomorphic connected members of $C$ with $(n,m,\tau)=(29,23,12)$, maximum degree 3 and slack 1, with degrees $2^{18}3^{11}$;
- $K_{29}$;
- the construction sentence;
- the counts: all 45 have an (e)-vertex and three $\Theta$-vertices; 27; 31;
- (i)–(iii).

This is what was verified:
- **Round 1.** Opus: membership, $\tau$, isomorphism, (i)–(iii) and the rebuild. Fable: $K_{29}$ in full, the 45 classes with `labelg`, and (ii) for $K_{29}$.
- **Round 2.** Fable rebuilt the 120 gluings: all in $C$, $\Delta\le3$, $\tau=12$, connected, with 45 distinct invariants equal to the stored set. Fable and opus both re-derived the counts.

The content of the R2 parenthetical was also re-derived by both round-2 referees, so it adds nothing unverified; its only problem is presentation.

**Other statements.**
- Theorem 2: only the tag and citation changed.
- Theorems 3 and 4, Corollary 5, Proposition 6 and Observation 7 are verbatim. In the Tags line only Theorem 2's entry changed.

**Proof steps.**
- Only the wording of Step 5.2 changed; its conclusion "at most 5 components" is unchanged.
- Remark 1.4 is new and is used by no proof.

## Remaining problems, in order of severity (all editorial)

**R1. "Verification status", last sentence (line 34).** The sentence reads: "The round-2 referees re-derived the pattern counts below with their own codes and rebuilt the pattern-(e) gluings from the stored lists."
- Only the fable round-2 referee rebuilt the gluings (`econf_count.py`).
- The opus round-2 folder has no gluing code; it only recounted the e-configured classes (24 of 953). Its review attributes the 120 gluings to "C1; re-derived by the opus round-1 referee".
- Remark 1.4 states this correctly, so the paragraph and the remark disagree.

Suggested fix: "The round-2 referees re-derived the pattern counts with their own codes; the fable round-2 referee also rebuilt the pattern-(e) gluings from the stored lists."

Optionally, also write "the fable referees of rounds 1 and 2" in the sentence about part (i), which would make it exact:
- fable-1 checked all of (i) for $K_{29}$, and "no NC pair" for all 45;
- for the other 44 classes, the degree-3 vertices were shown co-transversal ($\tau(K-v)=11$) by fable-2 `patterns45`.

**R2. Theorem 1 statement (line 32).** The parenthetical reads: "(For the pattern-(e) vertices the 45 is exact given the lists, Remark 1.4.)"
- It keeps half of the characterisation inside the theorem statement, while Remark 1.4 says "This is not part of the statement of Theorem 1".
- It also drops the qualifier that the derivation uses the role facts (unrefereed computation inputs).

Suggested fix: make it a pure pointer, for example "(Remark 1.4, which is not part of this theorem, shows that given the refereed lists and the role facts no class with a pattern-(e) vertex is missing.)", or delete it.

**R3 (cosmetic). Open problem 2 (line 164).** "the remainder $K-x-y$" uses Proposition 6's letters inside a sentence whose e-configuration is $(z;x,y)$ and whose first remainder is $K-z-x$; there $\{x,y\}$ is not the NC pair. Write "the remainder ($K$ minus the NC pair)".

**R4 (optional, carried over; non-blocking per opus round 2, items 7–8).**
- "is an instance of the Henning–Yeo operation (D)" (line 34) and "this is the vertex-gluing … operation (D)" (Observation 7) overstate the relation. HY's operation (D) works on non-uniform pieces with 2-edges and a 4-edge, so "analogous to" would be accurate.
- The parenthetical "extremal graph $K_4$ with one edge subdivided" in Theorem 2's bracket is established here (C6), not quoted from Chvátal–Hanson.
- F5 (the K8 remark) and O5 (the wording of Step 3.8) are still unapplied.

**Note for the acceptance step (not a fix).** Theorem 1 and Observation 7 still carry "[verified-here as a computation, unrefereed]". If the certificate is accepted, update these tags together with the LEDGER entry.

Once R1 and R2 are applied, which is editing only, I recommend ACCEPT without a further round; a diff check suffices.

## Independence statement

- I read the four earlier referee reviews of L020 (round 1: 064109Z, 072810Z; round 2: 074931Z, 075547Z) as the task allows. I did not read the scout review.
- Other referees' and the prover's output files were read as data only, to check attributions: opus-2 `bcfg_recount_output.txt`, `k29_profile_output.txt` and `prop6_check_output.txt`; fable-2 `econf_count_output.txt`; the opus-2 folder listing.
- My only computation is experiments/referee/L020-round3-fixcheck/prop6_attach.py (Python standard library only; nothing imported from e757/, judge/, experiments/prover/ or any referee folder), with output `prop6_attach_output.txt`. It reads the stored lists in experiments/20261027-0300-transversal-richness/inputs/ as data.
- I modified nothing except this review and that scratch folder.

## Round 3 re-check (commit c434c4d, 2026-10-27 08:13:30 UTC; checked 08:14 UTC)

**Scope of the commit.**
- `git show c434c4d` and `git diff --unified=0 c85ce6d c434c4d -- results/proofs/L020-joint-induction-i11.md` show hunks at lines 4, 32 and 34 only (3 insertions, 3 deletions).
- The file is clean at HEAD (c434c4d).

**R2 applied.**
- The parenthetical "(For the pattern-(e) vertices the 45 is exact given the lists, Remark 1.4.)" is deleted from the Theorem 1 statement; `grep -c` gives 0.
- The caveat now runs directly into "Moreover each of the 45 graphs $K$: (i) …".
- Remark 1.4's sentence "This is not part of the statement of Theorem 1" (line 85) is now consistent with the statement.

**R1 applied.** The sentence now reads: "Both round-2 referees re-derived the pattern counts below with their own codes; the fable round-2 referee also rebuilt the pattern-(e) gluings from the stored lists."
- This is accurate. Both re-derived the counts (opus-2 `k29_profile`/`t3_spot`, fable-2 `patterns45`/`thm3_sample`), and only fable-2 rebuilt the gluings (`econf_count`).
- It agrees with Remark 1.4.

**STATUS line.** It records "round-3 wording items R1, R2 applied 08:13 UTC", which matches the commit time.

**Nothing else changed.**
- No theorem statement, proof step, tag or other text changed.
- The main claim of Theorem 1, $K_{29}$, the construction, the counts, the caveat and (i)–(iii) are verbatim as verified in rounds 1 and 2.

**Remaining items, all cosmetic or optional and none blocking:**
- R3 and R4 above;
- the optional part (i) wording of R1;
- a stray ".;" before the round-3 note in the STATUS line ("stated as such.; round-3 …").

Final verdict: ACCEPT. All required fixes of rounds 1–3 are applied correctly; no mathematical or attribution problem remains.
