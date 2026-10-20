/* Referee L009 round 1: hooks for nauty genbg (orderly generation of bicoloured graphs).
   First class = hypergraph vertices (n1), second class = hyperedges (n2); run genbg with -Z1 (two edges share <= 1 vertex:
   linear), -d1:3 -D3:3 (vertex degrees 1..3, edge size exactly 3), -c (connected).
   PRUNE1 (hereditary, valid for every descendant): prune if tau(partial) < TAU0 - (maxn2 - n2)  [adding an edge raises tau by
   at most 1]; if CPRUNE=1 also prune partial graphs containing F7 (F7-freeness is inherited by sub-hypergraphs).
   OUTPROC: for every output hypergraph compute tau exactly, F7 (my own test: 5 edges, union of 7 vertices, some pair of the
   5 edges disjoint), (P3) (all non-empty edge sets F: |U(F)| >= |F|+2), and print
   "G tau=<t> C=<0/1>: (a,b,c) ..." for outputs with tau >= TAU0.  SUMMARY prints counts to stderr.
   Environment: TAU0 (default 0), CPRUNE (default 0). */
#include "gtools.h"
#include <stdint.h>
#include <stdlib.h>
static int TAU0 = -1, CPRUNE = 0;
static unsigned long long n_out = 0, n_tau = 0, n_C = 0, n_f7 = 0, n_p3 = 0;
static void init(void) {
    if (TAU0 >= 0) return;
    char *s = getenv("TAU0"); TAU0 = s ? atoi(s) : 0;
    s = getenv("CPRUNE"); CPRUNE = s ? atoi(s) : 0;
}
static int edges_of(graph *g, int n1, int n2, uint64_t *E) {
    int m = SETWORDSNEEDED(n1 + n2);
    for (int j = 0; j < n2; j++) {
        set *row = GRAPHROW(g, n1 + j, m); uint64_t e = 0;
        for (int i = 0; i < n1; i++) if (ISELEMENT(row, i)) e |= 1ull << i;
        E[j] = e;
    }
    return n2;
}
/* exists a vertex set of size <= k meeting every edge whose index is in 'left'? */
static int cover_le(const uint64_t *E, int ne, uint32_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    int i = __builtin_ctz(left); uint64_t e = E[i];
    while (e) {
        int x = __builtin_ctzll(e); e &= e - 1;
        uint32_t l2 = left;
        for (int j = 0; j < ne; j++) if ((l2 >> j & 1) && (E[j] >> x & 1)) l2 &= ~(1u << j);
        if (cover_le(E, ne, l2, k - 1)) return 1;
    }
    return 0;
}
static int tau_exact(const uint64_t *E, int ne) {
    uint32_t all = ne >= 32 ? 0xffffffffu : ((1u << ne) - 1);
    for (int k = 0; ; k++) if (cover_le(E, ne, all, k)) return k;
}
/* F7 among 5 edges: union has exactly 7 vertices and at least one pair of the 5 is disjoint (in a linear 3-graph). */
static int five_is_f7(const uint64_t *E, const int *ix) {
    uint64_t U = 0; for (int a = 0; a < 5; a++) U |= E[ix[a]];
    if (__builtin_popcountll(U) != 7) return 0;
    for (int a = 0; a < 5; a++) for (int b = a + 1; b < 5; b++) if (!(E[ix[a]] & E[ix[b]])) return 1;
    return 0;
}
/* does the hypergraph contain an F7 using edge 'must' (must < 0: any)? */
static int has_f7(const uint64_t *E, int ne, int must) {
    int ix[5];
    for (ix[0] = 0; ix[0] < ne; ix[0]++) for (ix[1] = ix[0] + 1; ix[1] < ne; ix[1]++) for (ix[2] = ix[1] + 1; ix[2] < ne; ix[2]++)
    for (ix[3] = ix[2] + 1; ix[3] < ne; ix[3]++) for (ix[4] = ix[3] + 1; ix[4] < ne; ix[4]++) {
        if (must >= 0 && ix[0] != must && ix[1] != must && ix[2] != must && ix[3] != must && ix[4] != must) continue;
        if (five_is_f7(E, ix)) return 1;
    }
    return 0;
}
static int p3_ok(const uint64_t *E, int ne) {
    for (uint32_t F = 1; F < (1u << ne); F++) {
        uint64_t U = 0; for (int j = 0; j < ne; j++) if (F >> j & 1) U |= E[j];
        if (__builtin_popcountll(U) < __builtin_popcount(F) + 2) return 0;
    }
    return 1;
}
int refprune(graph *g, int *deg, int n1, int n2, int maxn2) {
    init();
    uint64_t E[64]; int ne = edges_of(g, n1, n2, E);
    int need = TAU0 - (maxn2 - n2);          /* tau(partial) must be >= need */
    if (need >= 1) {
        uint32_t all = ne >= 32 ? 0xffffffffu : ((1u << ne) - 1);
        if (cover_le(E, ne, all, need - 1)) return 1;
    }
    if (CPRUNE && ne >= 5 && has_f7(E, ne, ne - 1)) return 1;
    return 0;
}
void refout(FILE *f, graph *g, int n1, int n2) {
    init();
    uint64_t E[64]; int ne = edges_of(g, n1, n2, E);
    n_out++;
    int t = tau_exact(E, ne);
    if (t < TAU0) return;
    n_tau++;
    int f7 = has_f7(E, ne, -1), p3 = p3_ok(E, ne);
    if (f7) n_f7++;
    if (!p3) n_p3++;
    int inC = !f7 && p3; n_C += inC;
    fprintf(f, "G tau=%d C=%d:", t, inC);
    for (int j = 0; j < ne; j++) {
        fprintf(f, " ("); int first = 1;
        for (int i = 0; i < n1; i++) if (E[j] >> i & 1) { fprintf(f, first ? "%d" : ",%d", i); first = 0; }
        fprintf(f, ")");
    }
    fprintf(f, "\n");
}
void refsummary(nauty_counter nout, double cpu) {
    init();
    fprintf(stderr, "REFSUMMARY TAU0=%d CPRUNE=%d outputs=%llu tau_ge_TAU0=%llu with_F7=%llu P3_violated=%llu in_C=%llu cpu=%.2f\n",
            TAU0, CPRUNE, n_out, n_tau, n_f7, n_p3, n_C, cpu);
}
