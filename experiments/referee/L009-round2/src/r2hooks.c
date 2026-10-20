/* r2hooks.c -- referee L009 round 2: PRUNE / OUTPROC / SUMMARY hooks for nauty genbg (written from scratch for this review).
   genbg generates bicoloured graphs: class 1 = points 0..n1-1, class 2 = hyperedges n1..n1+n2-1 (each of degree 3 by -d?:3 -D?:3,
   linearity by -Z1).  Environment:
     TAU0=t     : output only graphs with tau >= t; PRUNE1 prunes a partial graph with k of the K final edges when
                  tau(partial) < t - (K - k)   (valid: adding one edge raises tau by at most 1, and genbg's intermediate graphs are
                  edge-subsets of the final graph containing all points);
     F7PRUNE=1  : PRUNE2 also prunes partial graphs containing a copy of F7 (valid for an enumeration of F7-free graphs, because F7-freeness
                  is inherited by edge-subsets).
   OUTPROC writes one line per output graph: graph6 of the bicoloured graph, TAB, then "tau=.. f7=.. p3=.. C=.. deg=.. E: (a,b,c) ...".
   tau: exact (branching on the lowest uncovered edge, with a greedy matching lower bound);
   F7: pattern search (a centre c, three edges at c, two disjoint edges avoiding c inside the six other points meeting each of the
       three edges in exactly one point);
   P3: e(S) <= |S|-2 for EVERY vertex subset S with |S| >= 2 (brute force over all 2^n1 subsets).                              */
#include "gtools.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static int inited = 0, T0 = 0, F7P = 0;
static unsigned long long n_out = 0, n_C = 0, n_f7 = 0, n_p3bad = 0, pr_tau = 0, pr_f7 = 0, n_prune_calls = 0;
static unsigned long long tau_hist[40];

static void init(void) {
    if (inited) return;
    inited = 1;
    const char *s = getenv("TAU0"); T0 = s ? atoi(s) : 0;
    s = getenv("F7PRUNE"); F7P = s ? atoi(s) : 0;
}

/* current hypergraph */
static int NE, NV;
static uint32_t E[64];
static uint64_t INC[32];   /* INC[x] = set of edge indices containing point x */

static void load(graph *g, int n1, int n2) {
    int m = SETWORDSNEEDED(n1 + n2);
    NE = n2; NV = n1;
    for (int x = 0; x < n1; x++) INC[x] = 0;
    for (int j = 0; j < n2; j++) {
        set *row = GRAPHROW(g, n1 + j, m);
        uint32_t e = 0;
        for (int x = 0; x < n1; x++) if (ISELEMENT(row, x)) { e |= 1u << x; INC[x] |= 1ull << j; }
        E[j] = e;
    }
}

/* is there a set of at most k points meeting every edge in 'left'? */
static int cover_le(uint64_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    /* greedy matching lower bound: if more than k pairwise disjoint edges remain, no k-cover exists */
    {
        uint64_t l = left; uint32_t used = 0; int cnt = 0;
        while (l) { int i = __builtin_ctzll(l); l &= l - 1; if (!(E[i] & used)) { used |= E[i]; if (++cnt > k) return 0; } }
    }
    int i = __builtin_ctzll(left);
    uint32_t e = E[i];
    while (e) {
        int x = __builtin_ctz(e); e &= e - 1;
        if (cover_le(left & ~INC[x], k - 1)) return 1;
    }
    return 0;
}
static uint64_t alledges(void) { return NE >= 64 ? ~0ull : ((1ull << NE) - 1); }
static int tau_exact(void) { int k = 0; while (!cover_le(alledges(), k)) k++; return k; }

static int has_f7(void) {
    for (int c = 0; c < NV; c++) {
        uint64_t at = INC[c];
        int idx[64], d = 0;
        while (at) { idx[d++] = __builtin_ctzll(at); at &= at - 1; }
        for (int a = 0; a < d; a++) for (int b = a + 1; b < d; b++) for (int q = b + 1; q < d; q++) {
            uint32_t p1 = E[idx[a]] & ~(1u << c), p2 = E[idx[b]] & ~(1u << c), p3 = E[idx[q]] & ~(1u << c);
            if ((p1 & p2) || (p1 & p3) || (p2 & p3)) continue;   /* cannot happen in a linear graph */
            uint32_t P = p1 | p2 | p3;
            uint32_t tr[64]; int nt = 0;
            for (int j = 0; j < NE; j++) {
                uint32_t f = E[j];
                if (f & (1u << c)) continue;
                if ((f & ~P) != 0) continue;
                if (__builtin_popcount(f & p1) != 1 || __builtin_popcount(f & p2) != 1 || __builtin_popcount(f & p3) != 1) continue;
                tr[nt++] = f;
            }
            for (int u = 0; u < nt; u++) for (int v = u + 1; v < nt; v++) if (!(tr[u] & tr[v])) return 1;
        }
    }
    return 0;
}

static int p3_ok(void) {
    uint32_t full = (NV >= 32) ? 0xffffffffu : ((1u << NV) - 1);
    for (uint32_t S = 0;; S++) {
        int sz = __builtin_popcount(S);
        if (sz >= 2) {
            int e = 0;
            for (int j = 0; j < NE; j++) if ((E[j] & S) == E[j]) e++;
            if (e > sz - 2) return 0;
        }
        if (S == full) break;
    }
    return 1;
}

int r2prune1(graph *g, int *deg, int n1, int n2, int maxn2) {
    init();
    n_prune_calls++;
    int need = T0 - (maxn2 - n2);
    if (need <= 0) return 0;
    load(g, n1, n2);
    if (cover_le(alledges(), need - 1)) { pr_tau++; return 1; }
    return 0;
}

int r2prune2(graph *g, int *deg, int n1, int n2, int maxn2) {
    init();
    if (!F7P) return 0;
    if (n2 < 5) return 0;
    load(g, n1, n2);
    if (has_f7()) { pr_f7++; return 1; }
    return 0;
}

void r2out(FILE *f, graph *g, int n1, int n2) {
    init();
    load(g, n1, n2);
    int t = tau_exact();
    if (t < T0) { fprintf(stderr, "R2ERROR output with tau %d < TAU0 %d\n", t, T0); exit(7); }
    int f7 = has_f7(), p3 = p3_ok();
    int C = (!f7 && p3);
    n_out++; if (C) n_C++; if (f7) n_f7++; if (!p3) n_p3bad++;
    if (t < 40) tau_hist[t]++;
    int m = SETWORDSNEEDED(n1 + n2);
    char *s = ntog6(g, m, n1 + n2);
    size_t L = strlen(s); while (L && (s[L - 1] == '\n' || s[L - 1] == '\r')) s[--L] = 0;
    int dg[32] = {0};
    for (int j = 0; j < NE; j++) for (int x = 0; x < NV; x++) if (E[j] >> x & 1) dg[x]++;
    int dc[8] = {0}; for (int x = 0; x < NV; x++) dc[dg[x] < 7 ? dg[x] : 7]++;
    fprintf(f, "%s\ttau=%d f7=%d p3=%d C=%d deg=%d,%d,%d,%d,%d+ E:", s, t, f7, p3, C, dc[0], dc[1], dc[2], dc[3], dc[4]+dc[5]+dc[6]+dc[7]);
    for (int j = 0; j < NE; j++) {
        fprintf(f, " (");
        int first = 1;
        for (int x = 0; x < NV; x++) if (E[j] >> x & 1) { fprintf(f, first ? "%d" : ",%d", x); first = 0; }
        fprintf(f, ")");
    }
    fprintf(f, "\n");
}

void r2summary(nauty_counter nout, double cpu) {
    init();
    fprintf(stderr, "R2SUMMARY TAU0=%d F7PRUNE=%d out=%llu inC=%llu f7=%llu p3bad=%llu prune_tau=%llu prune_f7=%llu prune1_calls=%llu cpu=%.1f tau_hist:",
            T0, F7P, n_out, n_C, n_f7, n_p3bad, pr_tau, pr_f7, n_prune_calls, cpu);
    for (int t = 0; t < 40; t++) if (tau_hist[t]) fprintf(stderr, " %d:%llu", t, tau_hist[t]);
    fprintf(stderr, "\n");
}
