# Neighbouring problems and transferable techniques

| Problem | Status | Technique | Possible transfer to #757 |
|---|---|---|---|
| Erdős #135: planar (4,5)-sets; are there ≫n² distances? | Disproved by Tao, arXiv:2409.01343 [published] | Randomized Thiele–Dumitrescu parabola $\{(x,y):y\equiv x^2 \bmod p\}$; Dumitrescu's 8 forbidden 4-point patterns (DM 343 (2020)) | Forbidden-pattern bookkeeping; probabilistic constructions with local constraints |
| Weak Sidon (Sárközy–Sós Problem 12) | Solved: $g(n)=\lceil(n+1)/2\rceil$ (Ma–Tang) | 3-adic construction; run-charging proof | The run-charging pattern for lower bounds |
| Erdős #530: largest Sidon subset of $N$ arbitrary reals | $\asymp\sqrt N$; constant improved by Riblet, arXiv:2605.03181 | Freiman 2-isomorphism into cyclic groups | Freiman invariance: build in $\mathbb Z^d$ or $\mathbb Z_m$, project generically |
| Erdős #772: Sidon subsets of $B_2[k]$ sets | $\gg n^{2/3}$ (Alon–Erdős) | Random sampling plus deletion | Gives only about 1/2 here (dead end D9) |
| Erdős–Gyárfás $f(n,4,5)$ (edge colourings with 5 colours on every $K_4$) | $\tfrac56n+o(n)$ (Bennett–Cushman–Dudek–Prałat; Joos–Mubayi) | Conflict-free hypergraph matchings (nibble) | Random-greedy constructions under (4,5)-type local constraints, a possible Track U generator |
| Erdős #707: Sidon set extension | Disproved (arXiv:2510.19804, 2604.25214) | Human plus AI search, exact verification | Workflow precedent |
| Sidon constant $C_{5a}$ (Tao database) | AlphaEvolve improved an upper bound in 2025 | Evolutionary program search | Track U3 precedent |

Distance-Sidon subsets of planar sets ≫$|P|^{1/3}$ (Clemen–Führer–Roche-Newton, arXiv:2606.05841)
and 3-AP-free versus isosceles-free sets (arXiv:2606.17487) are recent, but probably only tangential.
