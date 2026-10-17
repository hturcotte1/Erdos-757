/* bf_cells.c: brute force over ALL labelled linear 3-graphs on [n] (DFS over triples in index order, no isomorphism
   reduction, no canonical growth).  For those that are connected and cover all n vertices, tally (m, tau).
   tau computed exactly by trying all vertex subsets in order of size (n <= 10). Output: lines "m tau maxdeg count". */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, nt; static uint32_t T[200]; static uint32_t cov[32]; static uint32_t E[64]; static int ne;
static unsigned long long tally[64][16][16];
static int popc(uint32_t x) { return __builtin_popcount(x); }
static int connected_spanning(void) {
    uint32_t used = 0; for (int i = 0; i < ne; i++) used |= E[i];
    if (used != (1u << n) - 1) return 0;
    uint32_t comp = E[0], prev = 0;
    while (comp != prev) { prev = comp; for (int i = 0; i < ne; i++) if (E[i] & comp) comp |= E[i]; }
    return comp == used;
}
static int tau_exact(void) {
    int best = n;
    for (uint32_t S = 0; S < (1u << n); S++) {
        int p = popc(S); if (p >= best) continue;
        int ok = 1; for (int i = 0; i < ne; i++) if (!(E[i] & S)) { ok = 0; break; }
        if (ok) best = p;
    }
    return best;
}
static void rec(int start) {
    if (ne >= 1 && connected_spanning()) { int md = 0; for (int x = 0; x < n; x++) { int d = 0; for (int i = 0; i < ne; i++) if (E[i] >> x & 1) d++; if (d > md) md = d; } tally[ne][tau_exact()][md]++; }
    for (int i = start; i < nt; i++) {
        uint32_t t = T[i]; int a = __builtin_ctz(t), b = __builtin_ctz(t & (t - 1)), c = 31 - __builtin_clz(t);
        if ((cov[a] >> b & 1) || (cov[a] >> c & 1) || (cov[b] >> c & 1)) continue;
        cov[a] |= (1u<<b)|(1u<<c); cov[b] |= (1u<<a)|(1u<<c); cov[c] |= (1u<<a)|(1u<<b);
        E[ne++] = t; rec(i + 1); ne--;
        cov[a] &= ~((1u<<b)|(1u<<c)); cov[b] &= ~((1u<<a)|(1u<<c)); cov[c] &= ~((1u<<a)|(1u<<b));
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); nt = 0;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) T[nt++] = (1u<<a)|(1u<<b)|(1u<<c);
    rec(0);
    for (int m = 0; m < 64; m++) for (int t = 0; t < 16; t++) for (int d = 0; d < 16; d++) if (tally[m][t][d]) printf("%d %d %d %llu\n", m, t, d, tally[m][t][d]);
    return 0;
}
