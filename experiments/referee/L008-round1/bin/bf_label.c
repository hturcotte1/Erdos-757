/* bf_label.c -- referee brute force (L008 round 1), no symmetry reduction at all.
   Enumerates every labelled set of triples of [n] (each edge set exactly once: DFS over the C(n,3) triples in index order) that
   is linear and has maximum degree <= D, and tallies the CONNECTED SPANNING ones (every vertex in an edge, primal graph connected)
   by (m, tau).  tau computed exactly by brute force over vertex subsets in increasing size.
   Usage: bf_label n D   -> lines "n m tau count" */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, D, NT; static uint32_t T[200]; static uint32_t cur[64]; static int ne = 0; static int deg[32];
static unsigned long long cnt[40][40];
static int tau_bf(void) {
    for (int k = 0; k <= n; k++) {
        /* all k-subsets */
        if (k == 0) { if (ne == 0) return 0; continue; }
        uint32_t S = (1u << k) - 1;
        while (S < (1u << n)) {
            int ok = 1; for (int i = 0; i < ne; i++) if (!(cur[i] & S)) { ok = 0; break; }
            if (ok) return k;
            uint32_t c = S & -S, r = S + c; S = (((r ^ S) >> 2) / c) | r;
        }
    }
    return n;
}
static int conn_spanning(void) {
    uint32_t used = 0; for (int i = 0; i < ne; i++) used |= cur[i];
    if (used != (1u << n) - 1) return 0;
    uint32_t comp = cur[0], prev = 0;
    while (comp != prev) { prev = comp; for (int i = 0; i < ne; i++) if (cur[i] & comp) comp |= cur[i]; }
    return comp == used;
}
static void rec(int start) {
    if (ne > 0 && conn_spanning()) cnt[ne][tau_bf()]++;
    for (int t = start; t < NT; t++) {
        uint32_t e = T[t]; int ok = 1;
        for (int i = 0; i < ne; i++) if (__builtin_popcount(cur[i] & e) >= 2) { ok = 0; break; }
        if (!ok) continue;
        int a = __builtin_ctz(e), b = __builtin_ctz(e & (e - 1)), c = 31 - __builtin_clz(e);
        if (deg[a] >= D || deg[b] >= D || deg[c] >= D) continue;
        deg[a]++; deg[b]++; deg[c]++; cur[ne++] = e;
        rec(t + 1);
        ne--; deg[a]--; deg[b]--; deg[c]--;
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); D = atoi(argv[2]);
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) T[NT++] = (1u << a) | (1u << b) | (1u << c);
    rec(0);
    for (int m = 0; m < 40; m++) for (int t = 0; t < 40; t++) if (cnt[m][t]) printf("%d %d %d %llu\n", n, m, t, cnt[m][t]);
    return 0;
}
