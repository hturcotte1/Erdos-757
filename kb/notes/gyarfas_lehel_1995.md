# Gyárfás–Lehel, *Linear sets with five distinct differences among any four elements*, JCTB 64 (1995) 108–118 [published]

The full text was NOT obtained in the build sandbox. An author PDF is at
https://users.renyi.hu/~gyarfas/Cikkek/69_linset5.pdf (download it in a normal browser, or try
`bash scripts/fetch_papers.sh`). What is known from secondary sources (Ma–Tang, the omega thread,
Tao's constants entry):

- **Definitions.** (4,5)-sets; $g(n)$ = largest Sidon subset guaranteed (our $f(n)$); the AP
  hypergraph $H(A)$. Its properties are stated on p. 109 without proof (proved by Ma–Tang
  Lemmas 2.3–2.5).
- **Prop 2.1:** every (4,5)-set splits into two Sidon sets, via a forest 2-colouring. This gives
  $c_*\ge1/2$ ("a short 2-colorability argument", per Tao's entry).
  - **To recover:** the forest structure. The likely mechanism is that the "midpoint graph" is a
    forest, which gives a proper 2-colouring of the APs. A 2-colouring with no monochromatic AP
    yields a colour class of size at least n/2.
- **Prop 2.6:** $H(A)$ contains no $F_7$, by an arithmetic argument. Re-proved here by linear
  algebra over all 243 midpoint labelings (test `test_f7_not_realizable`).
- **Thm 3.2:** a Turán-type transversal estimate for sparse linear $F_7$-free 3-uniform
  hypergraphs, giving $\epsilon=1/(141\cdot76)$.
- **Upper bound:** $g(n)\le 3n/5+1$ from a Fibonacci-based sequence. Start at 2: the set
  $\{1,2,3,5\}$ is not (4,5).

**Why the PDF matters:** it may list further forbidden configurations, or a structural lemma
(the forest colouring) that was never pushed further. Ask the `scout` to fetch and digest it into
this file early in the run.
