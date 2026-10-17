/* bf_lab.c -- referee round 2 (L008): labelled brute force, no symmetry reduction.
   Enumerates every linear 3-graph on the labelled vertex set [n] (each edge set exactly once: DFS over the triples in index
   order, each triple in or out) with maximum degree <= D, and tallies, for every m and tau:
     ALL[m][tau]  = number of labelled graphs (isolated vertices allowed)
     CON[m][tau]  = number of those that are connected and spanning (every vertex in an edge, primal graph connected).
   tau by exhaustive search over vertex subsets in order of size.  Usage: bf_lab n D   (n <= 10) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, D, NT; static int T[200][3]; static uint32_t TM[200];
static int ne; static uint32_t E[64]; static int deg[16]; static uint32_t cov[16];
static unsigned long long ALL[40][12], CON[40][12];
static int tau(void) {
    uint32_t full = (1u << n);
    for (int k = 0; k <= n; k++) {
        for (uint32_t S = 0; S < full; S++) {
            if (__builtin_popcount(S) != k) continue;
            int ok = 1; for (int j = 0; j < ne; j++) if (!(E[j] & S)) { ok = 0; break; }
            if (ok) return k;
        }
    }
    return n;
}
static int conn_spanning(void) {
    uint32_t used = 0; for (int j = 0; j < ne; j++) used |= E[j];
    if (used != (1u << n) - 1) return 0;
    if (ne == 0) return 0;
    uint32_t comp = E[0], prev = 0;
    while (comp != prev) { prev = comp; for (int j = 0; j < ne; j++) if (E[j] & comp) comp |= E[j]; }
    return comp == used;
}
static void rec(int i) {
    if (i == NT) { int t = tau(); ALL[ne][t]++; if (conn_spanning()) CON[ne][t]++; return; }
    rec(i + 1);                                      /* triple i out */
    int a = T[i][0], b = T[i][1], c = T[i][2];
    if (deg[a] >= D || deg[b] >= D || deg[c] >= D) return;
    if ((cov[a] >> b & 1) || (cov[a] >> c & 1) || (cov[b] >> c & 1)) return;
    E[ne++] = TM[i]; deg[a]++; deg[b]++; deg[c]++;
    uint32_t ca = cov[a], cb = cov[b], cc = cov[c];
    cov[a] |= (1u << b) | (1u << c); cov[b] |= (1u << a) | (1u << c); cov[c] |= (1u << a) | (1u << b);
    rec(i + 1);
    cov[a] = ca; cov[b] = cb; cov[c] = cc; deg[a]--; deg[b]--; deg[c]--; ne--;
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); D = atoi(argv[2]);
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) { T[NT][0] = a; T[NT][1] = b; T[NT][2] = c; TM[NT] = (1u << a) | (1u << b) | (1u << c); NT++; }
    rec(0);
    for (int m = 0; m < 40; m++) for (int t = 0; t < 12; t++) {
        if (ALL[m][t]) printf("ALL n=%d D=%d m=%d tau=%d count=%llu\n", n, D, m, t, ALL[m][t]);
        if (CON[m][t]) printf("CON n=%d D=%d m=%d tau=%d count=%llu\n", n, D, m, t, CON[m][t]);
    }
    return 0;
}
