/* Referee L011 round 2: my own PRUNE1 / OUTPROC / SUMMARY hooks for nauty's genbg.
   Class 1 = points 0..n1-1, class 2 = hyperedges (each of degree 3 via -d?:3 -D?:3).
   Env TAU0=t: prune a partial graph with n2 of maxn2 edges if tau(partial) + (maxn2-n2) < t (sound: deleting an edge lowers
   tau by at most 1, and the condition is preserved under deleting ANY edge, so every ancestor of a wanted graph passes).
   Output: one line per graph, "G: (a,b,c) (d,e,f) ..." with the edges as genbg numbers them.  No F7 pruning here. */
#include "gtools.h"
#include <stdlib.h>
typedef unsigned long long u64;
static int T0 = -1;
static u64 ncalls = 0, npruned = 0, nout = 0, nbad = 0;

static void edges_of(graph *g, int n1, int n2, u64 *E) {
    for (int j = 0; j < n2; j++) {
        set *row = GRAPHROW(g, n1 + j, 1);
        u64 msk = 0;
        for (int i = 0; i < n1; i++) if (ISELEMENT(row, i)) msk |= 1ULL << i;
        E[j] = msk;
    }
}
/* is there a set of at most k points, containing S, that meets every edge? */
static int cover(const u64 *E, int ne, u64 S, int k) {
    int j;
    for (j = 0; j < ne; j++) if (!(E[j] & S)) break;
    if (j == ne) return 1;
    if (k <= 0) return 0;
    u64 e = E[j];
    while (e) { u64 b = e & (~e + 1); e ^= b; if (cover(E, ne, S | b, k - 1)) return 1; }
    return 0;
}
int hprune(graph *g, int *deg, int n1, int n2, int maxn2) {
    if (T0 < 0) { char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0; }
    ncalls++;
    int need = T0 - (maxn2 - n2);
    if (need <= 1) return 0;                 /* tau(partial) >= 1 always (n2 >= 1) */
    if (need > n2) { npruned++; return 1; }   /* tau <= n2 < need */
    u64 E[64]; edges_of(g, n1, n2, E);
    if (cover(E, n2, 0, need - 1)) { npruned++; return 1; }
    return 0;
}
void hout(FILE *f, graph *g, int n1, int n2) {
    u64 E[64]; edges_of(g, n1, n2, E);
    if (T0 < 0) { char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0; }
    if (T0 >= 1 && cover(E, n2, 0, T0 - 1)) { nbad++; return; }
    nout++;
    fprintf(f, "G:");
    for (int j = 0; j < n2; j++) {
        int v[3], c = 0;
        for (int i = 0; i < n1; i++) if (E[j] >> i & 1) { if (c < 3) v[c] = i; c++; }
        if (c != 3) { nbad++; fprintf(f, " BAD"); continue; }
        fprintf(f, " (%d,%d,%d)", v[0], v[1], v[2]);
    }
    fprintf(f, "\n");
}
void hsum(nauty_counter n, double cpu) {
    fprintf(stderr, "HSUM tau0=%d calls=%llu pruned=%llu out=%llu bad=%llu genbg_nout=%llu cpu=%.2f\n",
            T0, ncalls, npruned, nout, nbad, (unsigned long long)n, cpu);
}
