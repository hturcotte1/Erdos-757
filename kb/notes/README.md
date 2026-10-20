# Notes on papers and topics (written mainly by the scout subagent)

One file per paper or topic: `kb/notes/<slug>.md`, containing the citation, the main results with
hypotheses, the techniques, the relevance to #757, and open questions. Tag statements.

## Index
- `ma_tang_2026.md`: Ma–Tang, arXiv:2602.23282v2 [published].
- `gyarfas_lehel_1995.md`: Gyárfás–Lehel, JCTB 64 (1995) 108–118 [published].
- `henning_yeo_2021_affine.md`: Henning–Yeo, Graphs Combin. 37 (2021) 867–890 [published]; full text not obtained, plus independent facts computed here [verified-here].
- `henning_yeo_transversals.md`: digest of three Henning–Yeo transversal papers (Graphs Combin. 2021, arXiv:1802.01825, EJC 24(2) 2017) [published].
- `omega_issue_9804.md`: omega-institute issue #9804 [community].
- `neighbouring_problems.md`: neighbouring problems and transferable techniques. [published] for the cited results (arXiv preprints count as in 00_START_HERE.md); [heuristic] for the "Possible transfer" column.
- `gl_tight_structure.md`: Lemmas 1-3 on Gyárfás–Lehel-tight saturated hypergraphs [derived-here; falsifier NONE-FOUND, experiments/falsify/gl-tight-structure/report.md].
- `extension_lemmas.md`: Lemmas E, U (with Corollaries U1, U2), Δ and Δ' (deletion version) on two-point extensions, universal vertices and Henning–Yeo degree bounds (Δ: a 16-point record, a vacuous hypothesis since f(16) = 10, K52; Δ': two-point deletions that leave an extremal subset) [derived-here; falsifier HOLDS-ON-DATA, experiments/falsify/extension-lemmas/README.md for E, U, Δ and experiments/falsify/deletion-lemma/README.md for Δ']. Supporting theory for K46/L005 and K48/L006 (U1 at (14,12,τ=6) and Lemma U at (12,10,τ=5) predict the outcome of the T2 lines; not load-bearing in either certificate). Δ' is only consistent with the deletion counts of K47 and K49 (it does not imply them).
- `i11_conjecture.md`: the inequality I11, 11τ ≤ 3n + 2m, for AP hypergraphs of (4,5)-sets: evidence, the window-cell induction proving it for n ≤ 22 on the abstract class C (linear F7-free 3-graphs with e(S) ≤ |S| − 2 on every vertex subset, which contains every AP hypergraph of a (4,5)-set; certificates L007–L011, K51–K55; hence f(16) = 10, f(18) = 11, f(20) = 12, f(22) = 13), the first I11-allowed record cell (23,21,10) (L012, K56: the degree-4 case is excluded, the degree-3 case is open, Q14), and what a general proof must use [conjecture in general; verified-here on C for n ≤ 22, computer-assisted; c* ≥ 6/11 would follow only if I11 is proved in general].
