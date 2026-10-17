/* bf.c -- referee L010 round 1.  Brute force over ALL labelled linear 3-graphs on [n] with maximum degree <= D
   (DFS over the C(n,3) triples in lexicographic order; a triple is added iff it shares <= 1 vertex with every chosen triple
   and keeps all degrees <= D).  No symmetry reduction, no tau pruning.  Every DFS node is one labelled graph; for those
   that are connected and spanning (every vertex in an edge, primal graph connected) we tally counts by (m, tau), tau by
   exhaustive search over vertex subsets in increasing size.  Output lines: "n D m tau count". Usage: bf n D [mmax] */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, D, MMAX = 99, nt; static uint32_t T[1000]; static uint32_t ch[64]; static int m = 0; static int deg[32];
static unsigned long long cnt[40][40];
static int tau(void) {
    for (int k = 0; k <= n; k++) {
        /* all k-subsets */
        int idx[32]; for (int i = 0; i < k; i++) idx[i] = i;
        while (1) {
            uint32_t S = 0; for (int i = 0; i < k; i++) S |= 1u << idx[i];
            int ok = 1; for (int j = 0; j < m; j++) if (!(ch[j] & S)) { ok = 0; break; }
            if (ok) return k;
            int i = k - 1; while (i >= 0 && idx[i] == n - k + i) i--;
            if (i < 0) break;
            idx[i]++; for (int j = i + 1; j < k; j++) idx[j] = idx[j - 1] + 1;
        }
    }
    return -1;
}
static int conn_spanning(void) {
    uint32_t used = 0; for (int j = 0; j < m; j++) used |= ch[j];
    if (used != (n == 32 ? 0xffffffffu : (1u << n) - 1)) return 0;
    uint32_t c = ch[0], p = 0; while (c != p) { p = c; for (int j = 0; j < m; j++) if (ch[j] & c) c |= ch[j]; }
    return c == used;
}
static void dfs(int start) {
    if (m >= 1 && conn_spanning()) cnt[m][tau()]++;
    if (m >= MMAX) return;
    for (int i = start; i < nt; i++) {
        uint32_t t = T[i]; int ok = 1;
        for (int j = 0; j < m; j++) if (__builtin_popcount(ch[j] & t) >= 2) { ok = 0; break; }
        if (!ok) continue;
        for (int v = 0; v < n; v++) if ((t >> v & 1) && deg[v] >= D) { ok = 0; break; }
        if (!ok) continue;
        ch[m++] = t; for (int v = 0; v < n; v++) if (t >> v & 1) deg[v]++;
        dfs(i + 1);
        m--; for (int v = 0; v < n; v++) if (t >> v & 1) deg[v]--;
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); D = atoi(argv[2]); if (argc > 3) MMAX = atoi(argv[3]);
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) T[nt++] = (1u << a) | (1u << b) | (1u << c);
    dfs(0);
    for (int mm = 1; mm < 40; mm++) for (int t = 0; t < 40; t++) if (cnt[mm][t]) printf("%d %d %d %d %llu\n", n, D, mm, t, cnt[mm][t]);
    return 0;
}
