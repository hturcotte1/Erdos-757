/* Referee L011 round 3: genbg hooks (compile with -DPRUNE1=r3prune -DOUTPROC=r3out -DSUMMARY=r3sum).
   Model: first class = points 0..n1-1, second class = hyperedges.  With -d1:3 -D<D>:3 -Z1 -c genbg generates every connected
   linear 3-graph on n1 points with n2 edges and point degrees in [1,D], one per isomorphism class.
   Env TAU0: prune a partial graph (first n2 edges) iff tau(partial) + (maxn2-n2) < TAU0 (every further edge raises tau by <= 1,
   so no completion can reach TAU0).  Env F7PRUNE=1: also prune iff the partial graph contains F7 (inherited by supergraphs).
   Output lines "G: (a,b,c) ... tau=t" after an exact recomputation of tau (lines with tau < TAU0 are counted as out_bad). */
#include "gtools.h"
#include <stdint.h>
#include <stdlib.h>
static int T0 = 0, FP = 0, inited = 0;
static unsigned long long calls = 0, ptau = 0, pf7 = 0, nout = 0, nbad = 0;
static int NE; static uint32_t E[64]; static uint64_t INC[64];
static void init(void) { char *s = getenv("TAU0"); if (s) T0 = atoi(s); s = getenv("F7PRUNE"); if (s) FP = atoi(s); inited = 1; }
static void load(graph *g, int n1, int n2) {
    NE = n2; for (int x = 0; x < n1; x++) INC[x] = 0;
    for (int i = 0; i < n2; i++) { set *row = GRAPHROW(g, n1 + i, 1); uint32_t e = 0;
        for (int j = 0; j < n1; j++) if (ISELEMENT(row, j)) { e |= 1u << j; INC[j] |= 1ull << i; }
        E[i] = e; }
}
/* can the edges in 'left' be met by <= k points?  branch on the LAST uncovered edge; lower bound = size of a greedy matching */
static int cov(uint64_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    { uint64_t l = left; uint32_t used = 0; int c = 0;
      while (l) { int i = 63 - __builtin_clzll(l); l &= ~(1ull << i); if (!(E[i] & used)) { used |= E[i]; if (++c > k) return 0; } } }
    int i = 63 - __builtin_clzll(left); uint32_t e = E[i];
    while (e) { int x = 31 - __builtin_clz(e); e &= ~(1u << x); if (cov(left & ~INC[x], k - 1)) return 1; }
    return 0;
}
static uint64_t allE(void) { return NE >= 64 ? ~0ull : ((1ull << NE) - 1); }
static int tau_exact(void) { int k = 0; while (!cov(allE(), k)) k++; return k; }
static int isedge(uint32_t m) { for (int i = 0; i < NE; i++) if (E[i] == m) return 1; return 0; }
/* F7 = {c a1 b1, c a2 b2, c a3 b3, a1 a2 a3, b1 b2 b3}: for a point c, three edges at c whose union has 7 points, a choice of one
   point from each pair; the chosen triple and the complementary triple must both be edges.  Valid for any 3-graph. */
static int has_f7(int n1) {
    for (int c = 0; c < n1; c++) {
        uint64_t at = INC[c]; if (__builtin_popcountll(at) < 3) continue;
        int id[64], d = 0; while (at) { id[d++] = __builtin_ctzll(at); at &= at - 1; }
        for (int p = 0; p < d; p++) for (int q = p + 1; q < d; q++) for (int r = q + 1; r < d; r++) {
            if (__builtin_popcount(E[id[p]] | E[id[q]] | E[id[r]]) != 7) continue;
            uint32_t P[3] = { E[id[p]] & ~(1u << c), E[id[q]] & ~(1u << c), E[id[r]] & ~(1u << c) };
            int lo[3], hi[3]; for (int t = 0; t < 3; t++) { lo[t] = __builtin_ctz(P[t]); hi[t] = 31 - __builtin_clz(P[t]); }
            for (int ch = 0; ch < 4; ch++) {   /* ch over choices for pairs 1,2 (pair 0 fixed: complement symmetry) */
                uint32_t f = 1u << lo[0], g = 1u << hi[0];
                for (int t = 1; t < 3; t++) { if (ch >> (t - 1) & 1) { f |= 1u << hi[t]; g |= 1u << lo[t]; } else { f |= 1u << lo[t]; g |= 1u << hi[t]; } }
                if (isedge(f) && isedge(g)) return 1;
            }
        }
    }
    return 0;
}
int r3prune(graph *g, int *deg, int n1, int n2, int maxn2) {
    if (!inited) init();
    calls++; load(g, n1, n2);
    int need = T0 - (maxn2 - n2);
    if (need > 0 && cov(allE(), need - 1)) { ptau++; return 1; }
    if (FP && has_f7(n1)) { pf7++; return 1; }
    return 0;
}
void r3out(FILE *f, graph *g, int n1, int n2) {
    if (!inited) init();
    load(g, n1, n2); int t = tau_exact();
    if (t < T0) { nbad++; return; }
    if (FP && has_f7(n1)) { nbad++; return; }
    nout++;
    fprintf(f, "G:");
    for (int i = 0; i < n2; i++) { uint32_t e = E[i]; int v[3], k = 0; while (e) { v[k++] = __builtin_ctz(e); e &= e - 1; } fprintf(f, " (%d,%d,%d)", v[0], v[1], v[2]); }
    fprintf(f, " tau=%d\n", t);
}
void r3sum(nauty_counter n, double cpu) {
    fprintf(stderr, "R3SUM TAU0=%d F7PRUNE=%d prune_calls=%llu pruned_tau=%llu pruned_f7=%llu out=%llu out_bad=%llu genbg_count=%llu cpu=%.2f\n",
            T0, FP, calls, ptau, pf7, nout, nbad, (unsigned long long)n, cpu);
}
