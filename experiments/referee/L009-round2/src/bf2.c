/* bf2.c -- referee L009 round 2: brute-force enumeration of ALL labelled 3-graphs on the vertex set {0..n-1} with exactly m edges that are
   linear, have maximum degree <= D, cover every vertex, are connected and have tau >= T0.  No symmetry breaking at all: the edges are
   chosen as m-subsets of the C(n,3) triples in increasing order, pruned only by linearity and the degree bound (and a trivial count
   bound: the remaining triples must suffice).  tau by brute force over vertex subsets.
   Usage: bf2 n m T0 D [print]   prints "E: (a,b,c) ..." lines if print=1, and a summary line "BF2 ... labelled=<count>".        */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, m, T0, D, PR;
static int tri[400][3]; static uint32_t tmask[400]; static int nt;
static int chosen[40]; static int dg[32]; static uint32_t pairused[32];
static unsigned long long labelled = 0, leaves = 0;
static int tau_bf(void) {
    for (int k = 0; k <= n; k++) {
        /* any k-subset covering all chosen edges? */
        for (uint32_t S = 0; S < (1u << n); S++) {
            if (__builtin_popcount(S) != k) continue;
            int ok = 1;
            for (int i = 0; i < m; i++) if (!(tmask[chosen[i]] & S)) { ok = 0; break; }
            if (ok) return k;
        }
    }
    return n;
}
static int connected_spanning(void) {
    uint32_t all = 0; for (int i = 0; i < m; i++) all |= tmask[chosen[i]];
    if (all != (n == 32 ? 0xffffffffu : (1u << n) - 1)) return 0;
    uint32_t comp = tmask[chosen[0]], prev = 0;
    while (comp != prev) { prev = comp; for (int i = 0; i < m; i++) if (tmask[chosen[i]] & comp) comp |= tmask[chosen[i]]; }
    return comp == all;
}
static void rec(int start, int k) {
    if (k == m) {
        leaves++;
        if (!connected_spanning()) return;
        if (tau_bf() < T0) return;
        labelled++;
        if (PR) { printf("E:"); for (int i = 0; i < m; i++) printf(" (%d,%d,%d)", tri[chosen[i]][0], tri[chosen[i]][1], tri[chosen[i]][2]); printf("\n"); }
        return;
    }
    for (int t = start; t <= nt - (m - k); t++) {
        int a = tri[t][0], b = tri[t][1], c = tri[t][2];
        if (dg[a] >= D || dg[b] >= D || dg[c] >= D) continue;
        if ((pairused[a] >> b & 1) || (pairused[a] >> c & 1) || (pairused[b] >> c & 1)) continue;
        chosen[k] = t; dg[a]++; dg[b]++; dg[c]++;
        pairused[a] |= (1u << b) | (1u << c); pairused[b] |= (1u << a) | (1u << c); pairused[c] |= (1u << a) | (1u << b);
        rec(t + 1, k + 1);
        dg[a]--; dg[b]--; dg[c]--;
        pairused[a] &= ~((1u << b) | (1u << c)); pairused[b] &= ~((1u << a) | (1u << c)); pairused[c] &= ~((1u << a) | (1u << b));
    }
}
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: bf2 n m T0 D [print]\n"); return 1; }
    n = atoi(argv[1]); m = atoi(argv[2]); T0 = atoi(argv[3]); D = atoi(argv[4]); PR = argc > 5 ? atoi(argv[5]) : 0;
    nt = 0;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) {
        tri[nt][0] = a; tri[nt][1] = b; tri[nt][2] = c; tmask[nt] = (1u << a) | (1u << b) | (1u << c); nt++; }
    rec(0, 0);
    printf("BF2 n=%d m=%d T0=%d D=%d leaves=%llu labelled=%llu\n", n, m, T0, D, leaves, labelled);
    return 0;
}
