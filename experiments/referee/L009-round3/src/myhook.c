/* Referee L009 round 3: my own genbg hooks (written fresh; not copied from round 1's hooks.c).
   genbg generates bicoloured graphs: first class = hypergraph vertices (n1), second class = edges (n2).
   Options used at the command line: -Z1 (two edges share <= 1 vertex => linear), -D<D>:3 -d1:3 (vertex degrees 1..D,
   every edge has exactly 3 vertices), -c (connected).
   PRUNE1: prune when tau(partial) + (edges still to add) < TAU0 (hereditary: one edge raises tau by at most 1).
           A quick lower bound on tau is a matching of pairwise disjoint edges (greedy); only if the greedy matching is
           too small do we run the exact test.
   OUTPROC: exact tau (branching on an uncovered edge, with the matching bound), F7 by the structural definition
           (a vertex p with three edges E1,E2,E3 at p and two DISJOINT edges D,E avoiding p inside (E1 u E2 u E3) - p),
           (P3) in the S-form: e(S) <= |S|-2 for every vertex set S with |S| >= 2 (all 2^n1 subsets).
   Env: TAU0 (default 0). Output line: "G n=<n1> m=<n2> tau=<t> f7=<0/1> p3=<0/1> C=<0/1> dmax=<d>: (a,b,c) ..." */
#include "gtools.h"
#include <stdint.h>
#include <stdlib.h>
static int TAU0 = -1;
static unsigned long long c_out = 0, c_tau = 0, c_f7 = 0, c_p3bad = 0, c_C = 0, c_prune = 0, c_prunecalls = 0;
static void init(void) { if (TAU0 < 0) { char *s = getenv("TAU0"); TAU0 = s ? atoi(s) : 0; } }
static int get_edges(graph *g, int n1, int n2, uint32_t *E) {
    int m = SETWORDSNEEDED(n1 + n2);
    for (int j = 0; j < n2; j++) {
        set *row = GRAPHROW(g, n1 + j, m); uint32_t e = 0;
        for (int i = 0; i < n1; i++) if (ISELEMENT(row, i)) e |= 1u << i;
        E[j] = e;
    }
    return n2;
}
static int greedy_matching(const uint32_t *E, int ne) {
    uint32_t used = 0; int k = 0;
    for (int j = 0; j < ne; j++) if (!(E[j] & used)) { used |= E[j]; k++; }
    return k;
}
/* is there a vertex set of size <= k meeting every edge in 'alive' (bitmask over edge indices)? */
static int coverable(const uint32_t *E, int ne, uint32_t alive, int k) {
    if (!alive) return 1;
    if (k <= 0) return 0;
    /* lower bound: greedy matching among alive edges */
    { uint32_t used = 0; int mt = 0; for (int j = 0; j < ne; j++) if ((alive >> j & 1) && !(E[j] & used)) { used |= E[j]; mt++; }
      if (mt > k) return 0; }
    /* branch on the alive edge with the fewest ... just the lowest index */
    int i = __builtin_ctz(alive); uint32_t e = E[i];
    while (e) {
        int x = __builtin_ctz(e); e &= e - 1;
        uint32_t rest = alive;
        for (int j = 0; j < ne; j++) if (E[j] >> x & 1) rest &= ~(1u << j);
        if (coverable(E, ne, rest, k - 1)) return 1;
    }
    return 0;
}
static int tau_exact(const uint32_t *E, int ne) {
    uint32_t all = ne >= 32 ? 0xffffffffu : ((1u << ne) - 1);
    int k = greedy_matching(E, ne);           /* tau >= matching size */
    while (!coverable(E, ne, all, k)) k++;
    return k;
}
static int contains_f7(const uint32_t *E, int ne, int n1) {
    for (int p = 0; p < n1; p++) {
        int at[64], na = 0;
        for (int j = 0; j < ne; j++) if (E[j] >> p & 1) at[na++] = j;
        if (na < 3) continue;
        for (int a = 0; a < na; a++) for (int b = a + 1; b < na; b++) for (int c = b + 1; c < na; c++) {
            uint32_t W = (E[at[a]] | E[at[b]] | E[at[c]]) & ~(1u << p);
            if (__builtin_popcount(W) != 6) continue;          /* linear => always 6, kept for safety */
            for (int d = 0; d < ne; d++) {
                if ((E[d] >> p & 1) || (E[d] & ~W)) continue;    /* D avoids p and lies inside W */
                for (int e = d + 1; e < ne; e++) {
                    if ((E[e] >> p & 1) || (E[e] & ~W)) continue;
                    if ((E[d] & E[e]) == 0) return 1;             /* D and E disjoint: {Ea,Eb,Ec,D,E} is F7 */
                }
            }
        }
    }
    return 0;
}
static int p3_holds(const uint32_t *E, int ne, int n1) {
    /* e(S) <= |S|-2 for all S with |S| >= 2 */
    for (uint32_t S = 0; S < (1u << n1); S++) {
        int sz = __builtin_popcount(S); if (sz < 2) continue;
        int es = 0; for (int j = 0; j < ne; j++) if ((E[j] & S) == E[j]) es++;
        if (es > sz - 2) return 0;
    }
    return 1;
}
int myprune(graph *g, int *deg, int n1, int n2, int maxn2) {
    init(); c_prunecalls++;
    uint32_t E[64]; int ne = get_edges(g, n1, n2, E);
    int need = TAU0 - (maxn2 - n2);     /* need tau(partial) >= need */
    if (need <= 0) return 0;
    if (greedy_matching(E, ne) >= need) return 0;
    uint32_t all = ne >= 32 ? 0xffffffffu : ((1u << ne) - 1);
    if (coverable(E, ne, all, need - 1)) { c_prune++; return 1; }
    return 0;
}
void myout(FILE *f, graph *g, int n1, int n2) {
    init();
    uint32_t E[64]; int ne = get_edges(g, n1, n2, E);
    c_out++;
    int t = tau_exact(E, ne);
    if (t < TAU0) return;
    c_tau++;
    int f7 = contains_f7(E, ne, n1), p3 = p3_holds(E, ne, n1);
    c_f7 += f7; c_p3bad += !p3; int inC = (!f7 && p3); c_C += inC;
    int dmax = 0; for (int v = 0; v < n1; v++) { int d = 0; for (int j = 0; j < ne; j++) if (E[j] >> v & 1) d++; if (d > dmax) dmax = d; }
    fprintf(f, "G n=%d m=%d tau=%d f7=%d p3=%d C=%d dmax=%d:", n1, ne, t, f7, p3, inC, dmax);
    for (int j = 0; j < ne; j++) { fprintf(f, " ("); int first = 1;
        for (int i = 0; i < n1; i++) if (E[j] >> i & 1) { fprintf(f, first ? "%d" : ",%d", i); first = 0; }
        fprintf(f, ")"); }
    fprintf(f, "\n");
}
void mysummary(nauty_counter nout, double cpu) {
    init();
    fprintf(stderr, "MYSUMMARY TAU0=%d genbg_outputs=%llu tau_ge_TAU0=%llu with_F7=%llu P3_violated=%llu in_C=%llu prunecalls=%llu pruned=%llu cpu=%.2f\n",
            TAU0, c_out, c_tau, c_f7, c_p3bad, c_C, c_prunecalls, c_prune, cpu);
}
