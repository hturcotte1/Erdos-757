/* hooks.c -- referee L010 round 1 (written from scratch).  PRUNE1 / OUTPROC / SUMMARY hooks for nauty's genbg.
   Encoding: class 1 = the n1 vertices of a 3-graph, class 2 = its edges.  Run with -c -Z1 -d1:3 -D<D>:3 n1 n2 3n2:3n2:
   every edge-vertex has exactly 3 neighbours, every vertex has degree 1..D, two edges share <= 1 vertex (linear, no repeated
   edge), incidence graph connected (= connected 3-graph without isolated vertices).
   Environment variable TAU0 (default 0).  PRUNE1 rejects an intermediate graph (first n2 edges of a descendant) when
   tau(current) < TAU0 - (maxn2 - n2): deleting one edge lowers tau by at most 1, so every ancestor of an output with
   tau >= TAU0 passes.  OUTPROC re-computes tau exactly and prints "FOUND: (a,b,c) ..." when tau >= TAU0.
   tau algorithm: smallest k for which cover(k) succeeds, where cover branches on the LOWEST-index edge not yet met
   (any cover contains one of its three vertices). */
#include "gtools.h"
#include <stdint.h>
static int T0 = -1;
static uint32_t E[64]; static int NE;
static unsigned long long npr = 0, ncut = 0, nout = 0, nlow = 0;
static int cov(uint64_t left, int k) {
    if (!left) return 1;
    if (k == 0) return 0;
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    for (int t = 0; t < 3; t++) {
        int v = __builtin_ctz(e); e &= e - 1;
        uint64_t l2 = left;
        for (int j = 0; j < NE; j++) if ((l2 >> j & 1ULL) && (E[j] >> v & 1u)) l2 &= ~(1ULL << j);
        if (cov(l2, k - 1)) return 1;
    }
    return 0;
}
static uint64_t allm(void) { return NE >= 64 ? ~0ULL : ((1ULL << NE) - 1); }
static int tau_exact(void) { int k = 0; while (!cov(allm(), k)) k++; return k; }
static void load(graph *g, int n1, int n2) {
    NE = n2;
    for (int j = 0; j < n2; j++) {
        setword w = g[n1 + j]; uint32_t e = 0; int c = 0;
        for (int i = 0; i < n1; i++) if (w & bit[i]) { e |= 1u << i; c++; }
        if (c > 3) { fprintf(stderr, "edge with %d vertices\n", c); exit(9); }
        E[j] = e;
    }
}
int refprune(graph *g, int *deg, int n1, int n2, int maxn2) {
    if (T0 < 0) { char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0; }
    npr++;
    int need = T0 - (maxn2 - n2);
    if (need <= 0) return 0;
    load(g, n1, n2);
    if (cov(allm(), need - 1)) { ncut++; return 1; }
    return 0;
}
void refout(FILE *f, graph *g, int n1, int n2) {
    if (T0 < 0) { char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0; }
    load(g, n1, n2);
    for (int j = 0; j < n2; j++) if (__builtin_popcount(E[j]) != 3) { fprintf(stderr, "bad edge size\n"); exit(9); }
    int t = tau_exact();
    if (t < T0) { nlow++; return; }
    nout++;
    fprintf(f, "FOUND:");
    for (int j = 0; j < n2; j++) {
        uint32_t e = E[j]; fprintf(f, " (");
        for (int c = 0; c < 3; c++) { int v = __builtin_ctz(e); e &= e - 1; fprintf(f, c ? ",%d" : "%d", v); }
        fprintf(f, ")");
    }
    fprintf(f, " tau=%d\n", t);
}
void refsummary(nauty_counter n, double cpu) {
    fprintf(stderr, "REFSUMMARY TAU0=%d prune_calls=%llu pruned=%llu printed=%llu below_tau0=%llu genbg_out=%llu cpu=%.2f\n",
            T0, npr, ncut, nout, nlow, (unsigned long long)n, cpu);
}
