/* Referee L009 round 3: brute force over ALL labelled linear 3-graphs on [n] with m edges (DFS over triples in index order,
   pruned only by linearity and max degree D). At the leaves: keep those that are connected, span all n vertices and have
   tau >= T0; print them as "BF: (a,b,c) ...". Usage: bf n m T0 D */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, m, T0, D, ntr; static uint32_t tr[1024]; static uint32_t ed[32]; static int dg[32];
static unsigned long long leaves = 0, kept = 0;
static int coverable(uint32_t alive, int k) {
    if (!alive) return 1; if (k <= 0) return 0;
    int i = __builtin_ctz(alive); uint32_t e = ed[i];
    while (e) { int x = __builtin_ctz(e); e &= e - 1; uint32_t rest = alive;
        for (int j = 0; j < m; j++) if (ed[j] >> x & 1) rest &= ~(1u << j);
        if (coverable(rest, k - 1)) return 1; }
    return 0;
}
static int connected_spanning(void) {
    uint32_t all = (1u << n) - 1, comp = ed[0], prev = 0;
    while (comp != prev) { prev = comp; for (int j = 0; j < m; j++) if (ed[j] & comp) comp |= ed[j]; }
    return comp == all;
}
static void rec(int start, int ne) {
    if (ne == m) {
        leaves++;
        if (!connected_spanning()) return;
        if (T0 > 0 && coverable((1u << m) - 1, T0 - 1)) return;
        kept++; printf("BF:"); for (int j = 0; j < m; j++) { printf(" ("); int f = 1; for (int v = 0; v < n; v++) if (ed[j] >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } printf(")"); } printf("\n");
        return;
    }
    for (int t = start; t < ntr; t++) {
        uint32_t e = tr[t]; int ok = 1;
        for (int j = 0; j < ne; j++) if (__builtin_popcount(e & ed[j]) >= 2) { ok = 0; break; }
        if (!ok) continue;
        int a = __builtin_ctz(e), c = 31 - __builtin_clz(e), b = __builtin_ctz(e & ~(1u << a) & ~(1u << c));
        if (dg[a] >= D || dg[b] >= D || dg[c] >= D) continue;
        ed[ne] = e; dg[a]++; dg[b]++; dg[c]++;
        rec(t + 1, ne + 1);
        dg[a]--; dg[b]--; dg[c]--;
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); m = atoi(argv[2]); T0 = atoi(argv[3]); D = atoi(argv[4]);
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) tr[ntr++] = (1u << a) | (1u << b) | (1u << c);
    rec(0, 0);
    fprintf(stderr, "BFSUMMARY n=%d m=%d T0=%d D=%d linear_labelled=%llu connected_spanning_tau_ge_T0=%llu\n", n, m, T0, D, leaves, kept);
    return 0;
}
