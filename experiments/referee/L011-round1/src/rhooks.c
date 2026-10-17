/* Referee L011 round 1: hooks for nauty's genbg (compiled with -DPRUNE1=rprune -DOUTPROC=rout -DSUMMARY=rsum).
   Bipartite model: first class = points 0..n1-1, second class = hyperedges n1..n1+n2-1 (genbg -d1:3 -D<D>:3 gives every
   hyperedge exactly 3 points and every point degree 1..D; -Z1 = two hyperedges share at most one point = linear; -c connected).
   genbg outputs one bicoloured graph per isomorphism class (colour-preserving), i.e. one 3-graph per isomorphism class.
   rprune (exact, monotone, hence sound for every completion):
     - tau prune: prune iff tau(partial) + (maxn2 - n2) < TAU0   (each further hyperedge raises tau by at most 1);
     - if env CMODE=1: also prune iff the partial 3-graph contains F7 (containment is inherited by supergraphs).
   rout: prints "G: (a,b,c) ..." (points as labelled by genbg), after re-checking tau >= TAU0 exactly.
   Environment: TAU0 (default 0), CMODE (default 0). */
#include "gtools.h"
#include <stdint.h>
static int T0 = 0, CMODE = 0, inited = 0;
static unsigned long long ncalls = 0, npruned_tau = 0, npruned_f7 = 0, nout = 0, nout_bad = 0;
static void init(void) {
    char *s = getenv("TAU0"); if (s) T0 = atoi(s);
    s = getenv("CMODE"); if (s) CMODE = atoi(s);
    inited = 1;
}
static int NE; static uint32_t E[64]; static uint64_t INC[32]; /* INC[x]: bitmask of hyperedges containing point x */
static void load(graph *g, int n1, int n2) {
    NE = n2;
    for (int x = 0; x < n1; x++) INC[x] = 0;
    for (int i = 0; i < n2; i++) {
        set *row = GRAPHROW(g, n1 + i, 1);
        uint32_t e = 0;
        for (int j = 0; j < n1; j++) if (ISELEMENT(row, j)) { e |= 1u << j; INC[j] |= 1ull << i; }
        E[i] = e;
    }
}
/* is there a set of <= k points meeting every hyperedge in 'left'? */
static int cover_le(uint64_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    /* lower bound: greedy pairwise disjoint hyperedges among 'left' */
    { uint32_t used = 0; int cnt = 0; uint64_t l = left;
      while (l) { int i = __builtin_ctzll(l); l &= l - 1; if (!(E[i] & used)) { used |= E[i]; if (++cnt > k) return 0; } } }
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int x = __builtin_ctz(e); e &= e - 1;
        if (cover_le(left & ~INC[x], k - 1)) return 1; }
    return 0;
}
static uint64_t alledges(void) { return NE >= 64 ? ~0ull : ((1ull << NE) - 1); }
static int tau_exact(void) { int k = 0; while (!cover_le(alledges(), k)) k++; return k; }
static int isedge(uint32_t m) { for (int i = 0; i < NE; i++) if (E[i] == m) return 1; return 0; }
/* F7 = {c a1 b1, c a2 b2, c a3 b3, a1 a2 a3, b1 b2 b3} as a (not necessarily induced) subhypergraph of a LINEAR 3-graph:
   for every point c, every 3 hyperedges through c, every choice f of one point from each of the three pairs: f and its
   complement within the three pairs are both hyperedges. */
static int has_f7(int n1) {
    for (int c = 0; c < n1; c++) {
        uint64_t at = INC[c]; if (__builtin_popcountll(at) < 3) continue;
        int idx[64], d = 0; while (at) { idx[d++] = __builtin_ctzll(at); at &= at - 1; }
        for (int p = 0; p < d; p++) for (int q = p + 1; q < d; q++) for (int r = q + 1; r < d; r++) {
            uint32_t P[3] = { E[idx[p]] & ~(1u << c), E[idx[q]] & ~(1u << c), E[idx[r]] & ~(1u << c) };
            int lo[3], hi[3];
            for (int t = 0; t < 3; t++) { lo[t] = __builtin_ctz(P[t]); hi[t] = 31 - __builtin_clz(P[t]); }
            for (int ch = 0; ch < 8; ch++) {
                uint32_t f = 0, gg = 0;
                for (int t = 0; t < 3; t++) { if (ch >> t & 1) { f |= 1u << hi[t]; gg |= 1u << lo[t]; } else { f |= 1u << lo[t]; gg |= 1u << hi[t]; } }
                if (isedge(f) && isedge(gg)) return 1;
            }
        }
    }
    return 0;
}
int rprune(graph *g, int *deg, int n1, int n2, int maxn2) {
    if (!inited) init();
    ncalls++;
    load(g, n1, n2);
    int r = maxn2 - n2, need = T0 - r;      /* need tau(partial) >= need */
    if (need > 0 && cover_le(alledges(), need - 1)) { npruned_tau++; return 1; }
    if (CMODE && has_f7(n1)) { npruned_f7++; return 1; }
    return 0;
}
void rout(FILE *f, graph *g, int n1, int n2) {
    if (!inited) init();
    load(g, n1, n2);
    int t = tau_exact();
    if (t < T0) { nout_bad++; return; }
    nout++;
    fprintf(f, "G:");
    for (int i = 0; i < n2; i++) {
        uint32_t e = E[i]; int v[3], k = 0; while (e) { v[k++] = __builtin_ctz(e); e &= e - 1; }
        fprintf(f, " (%d,%d,%d)", v[0], v[1], v[2]);
    }
    fprintf(f, " tau=%d\n", t);
}
void rsum(nauty_counter n, double cpu) {
    fprintf(stderr, "RSUM TAU0=%d CMODE=%d prune_calls=%llu pruned_tau=%llu pruned_f7=%llu out=%llu out_bad=%llu genbg_count=%llu cpu=%.2f\n",
            T0, CMODE, ncalls, npruned_tau, npruned_f7, nout, nout_bad, (unsigned long long)n, cpu);
}
