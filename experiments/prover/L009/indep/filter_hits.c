/* filter_hits.c -- independent filters (prover, certificate L008) for hypergraphs given as lines "TAG: (a,b,c) (d,e,f) ...".
   For each hypergraph: linearity; F7 by Lemma F of L007 (in a linear 3-graph five edges form a copy of F7 iff their union has
   7 vertices with within-degrees 3,2,2,2,2,2,2; all 5-subsets of edges are tested); property (P3) e(S) <= |S|-2 for all S, tested
   in the equivalent form |union(F)| >= |F|+2 for every nonempty set F of edges; exact tau (smallest k with a k-subset of the
   vertices meeting every edge); maximum degree; number of vertices; connectivity.
   Output: one summary line, plus "SURVIVOR:" lines for linear, F7-free, P3-satisfying hypergraphs.
   Usage: filter_hits TAG < file */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int E3[64][3]; static uint32_t M[64]; static int ne, nv;
static int linear(void) { for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) if (__builtin_popcount(M[i] & M[j]) >= 2) return 0; return 1; }
static int has_f7(void) {
    int idx[5];
    for (idx[0] = 0; idx[0] < ne; idx[0]++) for (idx[1] = idx[0] + 1; idx[1] < ne; idx[1]++)
    for (idx[2] = idx[1] + 1; idx[2] < ne; idx[2]++) for (idx[3] = idx[2] + 1; idx[3] < ne; idx[3]++)
    for (idx[4] = idx[3] + 1; idx[4] < ne; idx[4]++) {
        uint32_t U = 0; for (int k = 0; k < 5; k++) U |= M[idx[k]];
        if (__builtin_popcount(U) != 7) continue;
        int d3 = 0, d2 = 0;
        for (int v = 0; v < 32; v++) if (U >> v & 1) {
            int d = 0; for (int k = 0; k < 5; k++) if (M[idx[k]] >> v & 1) d++;
            if (d == 3) d3++; else if (d == 2) d2++;
        }
        if (d3 == 1 && d2 == 6) return 1;
    }
    return 0;
}
static int p3_ok(int *worst) {  /* returns 1 iff |U(F)| >= |F|+2 for all nonempty F; *worst = min over F of |U(F)|-|F| */
    static uint32_t U[1 << 20]; int w = 1000; U[0] = 0;
    for (uint32_t F = 1; F < (1u << ne); F++) {
        int low = __builtin_ctz(F); U[F] = U[F & (F - 1)] | M[low];
        int d = __builtin_popcount(U[F]) - __builtin_popcount(F); if (d < w) w = d;
    }
    *worst = w; return w >= 2;
}
static int tau(void) {
    for (int k = 0; k <= nv; k++) {
        /* iterate over k-subsets of [nv] by Gosper's hack */
        if (k == 0) { if (ne == 0) return 0; continue; }
        uint32_t S = (1u << k) - 1;
        while (S < (1u << nv)) {
            int ok = 1; for (int i = 0; i < ne; i++) if (!(M[i] & S)) { ok = 0; break; }
            if (ok) return k;
            uint32_t c = S & -S, r = S + c; S = (((r ^ S) >> 2) / c) | r;
        }
    }
    return nv;
}
static int connected(void) {
    uint32_t used = 0; for (int i = 0; i < ne; i++) used |= M[i];
    uint32_t comp = M[0], prev = 0;
    while (comp != prev) { prev = comp; for (int i = 0; i < ne; i++) if (M[i] & comp) comp |= M[i]; }
    return comp == used;
}
int main(int argc, char **argv) {
    const char *tag = argc > 1 ? argv[1] : "HIT";
    char line[4096]; size_t tl = strlen(tag);
    unsigned long long tot = 0, nlin = 0, nf7 = 0, np3bad = 0, nsurv = 0, nconn = 0, f7free_p3bad = 0;
    int taumin = 99, taumax = -1, mdmax = 0, nvmin = 99, nvmax = 0, worstmin = 99, worstmax = -99;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, tag, tl) || line[tl] != ':') continue;
        ne = 0; nv = 0; char *p = line + tl + 1;
        while ((p = strchr(p, '('))) {
            int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) return 2;
            E3[ne][0] = a; E3[ne][1] = b; E3[ne][2] = c; M[ne] = (1u << a) | (1u << b) | (1u << c); ne++;
            int mx = a > b ? (a > c ? a : c) : (b > c ? b : c); if (mx + 1 > nv) nv = mx + 1; p++;
        }
        tot++;
        int lin = linear(); nlin += lin;
        int f7 = has_f7(); nf7 += f7;
        int worst; int p3 = p3_ok(&worst); np3bad += !p3;
        if (!f7 && !p3) f7free_p3bad++;
        if (worst < worstmin) worstmin = worst; if (worst > worstmax) worstmax = worst;
        int t = tau(); if (t < taumin) taumin = t; if (t > taumax) taumax = t;
        int md = 0; for (int v = 0; v < nv; v++) { int d = 0; for (int i = 0; i < ne; i++) if (M[i] >> v & 1) d++; if (d > md) md = d; }
        if (md > mdmax) mdmax = md; if (nv < nvmin) nvmin = nv; if (nv > nvmax) nvmax = nv;
        nconn += connected();
        if (lin && !f7 && p3) { nsurv++; printf("SURVIVOR:%s", line + tl + 1); }
    }
    printf("SUMMARY tag=%s total=%llu linear=%llu contain_F7=%llu P3_violated=%llu F7free_and_P3_violated=%llu survivors=%llu "
           "connected=%llu tau_range=[%d,%d] maxdeg_max=%d vertices_range=[%d,%d] min(|U(F)|-|F|)_range=[%d,%d]\n",
           tag, tot, nlin, nf7, np3bad, f7free_p3bad, nsurv, nconn, taumin, taumax, mdmax, nvmin, nvmax, worstmin, worstmax);
    return 0;
}
