# Henning–Yeo: transversals in linear uniform hypergraphs (digest)

Notation: $n$ vertices, $m$ edges, $\tau$ = transversal number, $\alpha=n-\tau$ (for our
"independent" = contains no edge).

## 1. *Affine Planes and Transversals in 3-Uniform Linear Hypergraphs*, Graphs Combin. 37 (2021) 867–890 [published]

Only the abstract is available (paywall; full-text hunt on 2026-10-13 failed: Springer, UJ and SDU portals,
Unpaywall, OpenAlex, zbMATH, arXiv). See the dedicated note `henning_yeo_2021_affine.md` for the
abstract, what the reference list shows, independently computed facts ($F_7$ is exactly the minimal
violator of $17\tau\le5n+3m$; $L(13)$ has slack 2) and what is missing. Q6 in kb/open_questions.md
still depends on the PDF.

- **Context:**
  - $4\tau\le n+m$ (Tuza 1990; Chvátal–McDiarmid 1992);
  - $6\tau\le 2n+m$ (Chvátal–McDiarmid);
  - the linear hypergraphs attaining equality were characterized by Henning–Yeo (JGT 59 (2008);
    DM 313 (2013)).
- **Main theorem (Thm 7, as cited by Ma–Tang):** if a 3-uniform $H$ contains no subhypergraph
  isomorphic to AG(2,3) minus two points ($=F_7$), then $17\tau\le 5n+3m$.
  - The abstract's wording has no "linear"; Ma–Tang cite it for linear $F_7$-free $H$. Check the
    exact hypotheses in the PDF.
- **Corollary:** a graph with minimum degree ≥3, no 4-cycles, and no copy of one specific
  12-vertex graph has $\gamma_t\le 8n/17$. This is the open-neighbourhood-hypergraph dictionary
  (transversal of the ONH = total dominating set).
- **To determine from the PDF:**
  - the proof method (likely minimal counterexample plus reducible configurations);
  - the list of hypergraphs attaining or nearly attaining $17\tau=5n+3m$;
  - whether those are realizable as AP hypergraphs (test with `e757.core.realize`).

## 2. *Transversals in Uniform Linear Hypergraphs*, arXiv:1802.01825 [published]

Read in full.

- **Thm 2 (k ∈ {2,3}):** for linear connected $H$, $\tau\le (n+m)/(k+1)$, with equality iff
  $H=E_k$ (a single edge) or $H$ is AG(2,k) minus one or two points.
  - For $k=3$ these are $F_8$ and $F_7$, with $\tau(F_7)=3$, $\tau(F_8)=4$ and $\tau(F_9)=5$,
    where $F_9=$ AG(2,3).
- **Thm 3 (Dorfling–Henning):** if $\Delta\le2$, then $(k+1)\tau\le n+m$ for every $k$; equality
  iff a single edge, or $k$ even and $H=L_k$.
- **Thm 7 ($k=4$):** $5\tau\le n+m$ for linear 4-uniform $H$.
  - The tool is the **deficiency method:**
    - fix 15 "special" hypergraphs ($H_4, H_{10}, H_{11}, H_{14,i}, H_{21,i}$) whose transversal
      properties were verified by computer (Observation 1 (a)–(p));
    - for a family $X$ of disjoint special subhypergraphs, define
      $\mathrm{def}(X)=\sum w(F)-13|E^*(X)|$, where $E^*$ is the set of outside edges touching $X$;
    - prove the stronger $45\tau\le 6n+13m+\mathrm{def}(H)$ by minimal counterexample.
  - Key moves: Hall's theorem on the bipartite graph (special pieces vs $E^*$) to extend
    transversals; contracting a family to one new edge; a long case analysis on $|X|$ and
    $|\partial X|$.
  - **Template for #757:** replace the special pieces by small realizable AP configurations with
    large $\tau$.
- **Thm 4 / Thm 5:** for large $k$, the conjecture $(k+1)\tau\le n+m$ fails (random restriction
  of projective planes; $k_{\min}\le166$). The best constant is $\Theta(\ln k/k)$.
- **Thm 10:** AG(2,k) minus the points of a subset of one line attains the bound at many densities.
- **Remark 5:** if a bound $\tau\le c(n+m)$ holds and is tight, it cannot be tight at average
  degree $>k$ or $<1$. Deleting a high-degree vertex gives slack. A similar argument might
  constrain extremal AP hypergraphs.

## 3. *Transversals and Independence in Linear Hypergraphs with Maximum Degree Two*, EJC 24(2) P2.50 (2017) [published]

- For connected, linear, $k$-uniform $H$ with $\Delta\le2$ and $k\ge3$ odd:
  - $k(k^2-3)\tau\le (k-2)(k+1)n+(k-1)^2m+k-1$;
  - $k(k^2-3)\alpha\ge (k^2+k-4)n-(k-1)^2m-(k-1)$.
- These are tight for infinite families.
- **For $k=3$:** $18\tau\le 4n+4m+2$. With $m\le n-2$ on each component this gives
  $h\ge(5n+3)/9$ [derived-here, K10]. So beating 5/9 needs points of AP-degree ≥3.

## 4. Other useful statements
- **Henning–Yeo, DAM 304 (2021):** lower bounds on the best $q_k$ with $\tau\le q_k(n+m)$ for
  linear $k$-uniform $H$.
- **Lai–Chang (JCTB 1990):** $\tau\le 2(n+m)/9$ for 4-uniform $H$.
- **Thomassé–Yeo:** $\tau\le 8n/21$ for 3-regular 4-uniform $H$.
  These show what the transversal literature tends to look like: exact rational constants proved
  by discharging or deficiency arguments, with small extremal pieces.
- **Book:** Henning–Yeo, *Transversals in Linear Uniform Hypergraphs* (Springer 2020). Chapters
  on affine and projective planes, upper transversals, the cap set connection, and the Tuza
  constant.
