/* referee_hooks.c -- PRUNE1 and OUTPROC hooks for nauty's genbg (referee of L008, round 1; written from scratch).
   genbg generates bicoloured graphs up to colour-preserving isomorphism by orderly canonical augmentation (McKay), adding one
   vertex of the second class at a time.  Encoding: first class = the n1 vertices of a 3-graph, second class = its edges; with
   -d1:3 -D3:3 every edge-vertex has exactly 3 neighbours and every vertex has degree 1..3; -Z1 (two edge-vertices share at most
   one neighbour) = linearity (and no repeated edge); -c = connected incidence graph = connected 3-graph without isolated vertex.
   PRUNE1 (called on every intermediate graph, which is the output graph minus its last-added edge-vertices): reject if
   tau(current edges) < TAU0 - (maxn2 - n2).  Valid: removing one edge lowers tau by at most 1, so a descendant with tau >= TAU0
   has every ancestor with tau >= TAU0 - (number of missing edges).  At n2 = maxn2 this is the test tau >= TAU0 itself.
   TAU0 is read from the environment.  OUTPROC prints "FOUND: (a,b,c) ..." (vertices 0..n1-1). */
#include "gtools.h"
#include <stdint.h>
static int T0 = -999;
static uint32_t EE[64]; static int NE;
static unsigned long long n_pr_calls = 0, n_pruned = 0, n_out = 0;
static int coverable(uint32_t left, int k) {      /* can the edges with index in 'left' be met by <= k vertices ? */
    if (!left) return 1;
    if (k <= 0) return 0;
    int i = __builtin_ctz(left); uint32_t e = EE[i];
    while (e) {
        int v = __builtin_ctz(e); e &= e - 1;
        uint32_t l2 = left;
        for (int j = 0; j < NE; j++) if ((l2 >> j & 1) && (EE[j] >> v & 1)) l2 &= ~(1u << j);
        if (coverable(l2, k - 1)) return 1;
    }
    return 0;
}
static void load(graph *g, int n1, int n2) {
    NE = n2;
    for (int j = 0; j < n2; j++) {
        setword w = g[n1 + j]; uint32_t e = 0;
        for (int i = 0; i < n1; i++) if (w & bit[i]) e |= 1u << i;
        EE[j] = e;
    }
}
int tauprune(graph *g, int *deg, int n1, int n2, int maxn2) {
    if (T0 == -999) { char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0; }
    n_pr_calls++;
    int need = T0 - (maxn2 - n2);
    if (need <= 0) return 0;
    load(g, n1, n2);
    uint32_t all = (n2 >= 32) ? 0xffffffffu : ((1u << n2) - 1);
    if (coverable(all, need - 1)) { n_pruned++; return 1; }   /* tau <= need-1 : prune */
    return 0;
}
void refout(FILE *f, graph *g, int n1, int n2) {
    load(g, n1, n2); n_out++;
    fprintf(f, "FOUND:");
    for (int j = 0; j < n2; j++) {
        int first = 1; fprintf(f, " (");
        for (int i = 0; i < n1; i++) if (EE[j] >> i & 1) { fprintf(f, first ? "%d" : ",%d", i); first = 0; }
        fprintf(f, ")");
    }
    fprintf(f, "\n");
}
void refsummary(nauty_counter nout, double cpu) {
    fprintf(stderr, "REFSUMMARY TAU0=%d prune_calls=%llu pruned=%llu outputs=%llu cpu=%.2f\n", T0, n_pr_calls, n_pruned, n_out, cpu);
}
