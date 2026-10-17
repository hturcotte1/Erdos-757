/* bf_cell.c: brute-force count of LABELLED connected linear 3-graphs on [n] with exactly m edges, tau >= t and every vertex
   covered.  DFS over triples in index order (each edge set generated once), no symmetry reduction; the only pruning is
   tau(placed) >= t - (m - depth) (valid: each further edge raises tau by at most 1).  tau by exhaustive subset search. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, m, t, nt; static uint32_t T[400]; static uint32_t cov[32]; static uint32_t E[32]; static int ne;
static unsigned long long cnt = 0, nodes = 0;
static uint32_t subs[16][4096]; static int nsubs[16];   /* all vertex subsets of [n] by size */
static int tau_ge(int k) { /* is tau(E[0..ne)) >= k ?  i.e. no vertex set of size k-1 meets every edge (if a smaller set
                              did, so would any (k-1)-superset, as k-1 <= n) */
    if (k <= 0) return 1;
    int s = k - 1; if (s > n) return 0;
    for (int j = 0; j < nsubs[s]; j++) {
        uint32_t S = subs[s][j];
        int ok = 1; for (int i = 0; i < ne; i++) if (!(E[i] & S)) { ok = 0; break; }
        if (ok) return 0;
    }
    return 1;
}
static int conn_span(void) {
    uint32_t used = 0; for (int i = 0; i < ne; i++) used |= E[i];
    if (used != (1u << n) - 1) return 0;
    uint32_t comp = E[0], prev = 0;
    while (comp != prev) { prev = comp; for (int i = 0; i < ne; i++) if (E[i] & comp) comp |= E[i]; }
    return comp == used;
}
static void rec(int start) {
    nodes++;
    if (ne == m) { if (conn_span() && tau_ge(t)) cnt++; return; }
    for (int i = start; i < nt; i++) {
        uint32_t x = T[i]; int a = __builtin_ctz(x), b = __builtin_ctz(x & (x - 1)), c = 31 - __builtin_clz(x);
        if ((cov[a] >> b & 1) || (cov[a] >> c & 1) || (cov[b] >> c & 1)) continue;
        cov[a] |= (1u<<b)|(1u<<c); cov[b] |= (1u<<a)|(1u<<c); cov[c] |= (1u<<a)|(1u<<b);
        E[ne++] = x;
        if (tau_ge(t - (m - ne))) rec(i + 1);
        ne--;
        cov[a] &= ~((1u<<b)|(1u<<c)); cov[b] &= ~((1u<<a)|(1u<<c)); cov[c] &= ~((1u<<a)|(1u<<b));
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); m = atoi(argv[2]); t = atoi(argv[3]); nt = 0;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) T[nt++] = (1u<<a)|(1u<<b)|(1u<<c);
    for (uint32_t S = 0; S < (1u << n); S++) { int p = __builtin_popcount(S); subs[p][nsubs[p]++] = S; }
    rec(0);
    printf("bf_cell n=%d m=%d t=%d nodes=%llu labelled=%llu\n", n, m, t, nodes, cnt);
    return 0;
}
