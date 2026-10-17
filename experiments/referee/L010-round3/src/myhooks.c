/* myhooks.c -- referee L010 round 3 (written from scratch).  Hooks for nauty genbg to enumerate connected linear 3-uniform
   hypergraphs by their incidence bipartite graphs: class 1 = n1 vertices (degree 1..D), class 2 = n2 edges (degree exactly 3),
   -Z1 = two edges share <= 1 vertex (linear), -c = connected incidence graph.  Command: genbg -c -Z1 -d1:3 -D<D>:3 n1 n2 3n2:3n2
   Environment: TAU0 (output only hypergraphs with tau >= TAU0; prune partial graphs with tau(partial) < TAU0 - (edges still to add)),
   F7PRUNE=1 (prune partial graphs containing F7: hereditary under adding edges), P3PRUNE=1 (prune partial graphs with an edge set F,
   |V(F)| < |F|+2: hereditary).  tau is computed by branch-and-bound: lower bound = size of a greedy matching of pairwise disjoint
   edges; branching on the uncovered edge with the fewest vertices still usable (all 3 here), exact.  Output: "FOUND: (a,b,c) ... tau=t" */
#include "gtools.h"
#include <stdint.h>
#include <stdlib.h>
static int T0 = -1, F7P = 0, P3P = 0;
static uint32_t E[64]; static int NE, NV;
static unsigned long long calls = 0, cut_tau = 0, cut_f7 = 0, cut_p3 = 0, nout = 0, nbelow = 0;
static void init(void) { if (T0 < 0) { char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0; s = getenv("F7PRUNE"); F7P = s && atoi(s); s = getenv("P3PRUNE"); P3P = s && atoi(s); } }
static void load(graph *g, int n1, int n2) {
    NE = n2; NV = n1;
    for (int j = 0; j < n2; j++) { setword w = g[n1 + j]; uint32_t e = 0; for (int i = 0; i < n1; i++) if (ISELEMENT(&w, i)) e |= 1u << i; E[j] = e; }
}
/* can the edges in 'left' be covered by <= k vertices?  (my own branching: pick the lowest uncovered edge; try its vertices) */
static int coverable(uint64_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    /* lower bound: greedy disjoint edges */
    { uint64_t l = left; uint32_t used = 0; int cnt = 0;
      while (l) { int i = __builtin_ctzll(l); l &= l - 1; if (!(E[i] & used)) { used |= E[i]; cnt++; } }
      if (cnt > k) return 0; }
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int v = __builtin_ctz(e); e &= e - 1;
        uint64_t l2 = left; for (int j = 0; j < NE; j++) if ((l2 >> j & 1) && (E[j] >> v & 1)) l2 &= ~(1ULL << j);
        if (coverable(l2, k - 1)) return 1; }
    return 0;
}
static uint64_t allmask(void) { return NE >= 64 ? ~0ULL : ((1ULL << NE) - 1); }
static int tau_exact(void) { int k = 0; while (!coverable(allmask(), k)) k++; return k; }
/* F7: a vertex p with 3 edges A,B,C at p, and two disjoint edges e1,e2 not containing p, each meeting A,B,C in one vertex each */
static int has_f7(void) {
    for (int p = 0; p < NV; p++) {
        int at[64], na = 0; for (int j = 0; j < NE; j++) if (E[j] >> p & 1) at[na++] = j;
        if (na < 3) continue;
        for (int x = 0; x < na; x++) for (int y = x + 1; y < na; y++) for (int z = y + 1; z < na; z++) {
            uint32_t A = E[at[x]], B = E[at[y]], C = E[at[z]], U = (A | B | C) & ~(1u << p);
            for (int j = 0; j < NE; j++) { uint32_t e = E[j]; if ((e >> p & 1) || (e & U) != e) continue;
                if (__builtin_popcount(e & A) != 1 || __builtin_popcount(e & B) != 1 || __builtin_popcount(e & C) != 1) continue;
                for (int k = j + 1; k < NE; k++) { uint32_t f = E[k]; if ((f >> p & 1) || (f & U) != f || (f & e)) continue;
                    if (__builtin_popcount(f & A) == 1 && __builtin_popcount(f & B) == 1 && __builtin_popcount(f & C) == 1) return 1; } }
        }
    }
    return 0;
}
/* P3 violated iff some nonempty edge set F has |V(F)| <= |F|+1; all 2^NE subsets (NE <= 20 here) */
static int p3_bad(void) {
    static uint32_t U[1 << 22]; U[0] = 0;
    for (uint32_t F = 1; F < (1u << NE); F++) { U[F] = U[F & (F - 1)] | E[__builtin_ctz(F)]; if (__builtin_popcount(U[F]) < __builtin_popcount(F) + 2) return 1; }
    return 0;
}
int myprune(graph *g, int *deg, int n1, int n2, int maxn2) {
    init(); calls++; load(g, n1, n2);
    int need = T0 - (maxn2 - n2);
    if (need > 0 && coverable(allmask(), need - 1)) { cut_tau++; return 1; }
    if (F7P && n2 >= 5 && has_f7()) { cut_f7++; return 1; }
    if (P3P && p3_bad()) { cut_p3++; return 1; }
    return 0;
}
void myout(FILE *f, graph *g, int n1, int n2) {
    init(); load(g, n1, n2);
    for (int j = 0; j < n2; j++) if (__builtin_popcount(E[j]) != 3) { fprintf(stderr, "edge size != 3\n"); exit(9); }
    int t = tau_exact(); if (t < T0) { nbelow++; return; }
    nout++;
    fprintf(f, "FOUND:");
    for (int j = 0; j < n2; j++) { uint32_t e = E[j]; fprintf(f, " ("); for (int c = 0; c < 3; c++) { int v = __builtin_ctz(e); e &= e - 1; fprintf(f, c ? ",%d" : "%d", v); } fprintf(f, ")"); }
    fprintf(f, " tau=%d\n", t);
}
void mysummary(nauty_counter n, double cpu) {
    fprintf(stderr, "MYSUMMARY TAU0=%d F7PRUNE=%d P3PRUNE=%d prune_calls=%llu cut_tau=%llu cut_f7=%llu cut_p3=%llu genbg_out=%llu below_tau0=%llu printed=%llu cpu=%.2f\n",
            T0, F7P, P3P, calls, cut_tau, cut_f7, cut_p3, (unsigned long long)n, nbelow, nout, cpu);
}
