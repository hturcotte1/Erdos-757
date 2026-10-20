/* r3_bf.c -- referee L008 round 3: labelled brute force with NO symmetry reduction.  Enumerates every linear 3-graph on the
   vertex set [n] (edges = triples chosen in increasing index order, each new triple sharing <= 1 vertex with every earlier one,
   degrees <= D), and tallies those that are connected and spanning (no isolated vertex) by (m, tau, maxdeg).
   tau by brute force over all vertex subsets of size k = 0,1,2,... (first k admitting a transversal).
   Usage: r3_bf n D   -> lines "n m tau maxdeg count" */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, D, nt; static uint32_t T[200]; static uint32_t E[64]; static int ne, deg[32]; static uint32_t nb[32];
static unsigned long long cnt[40][40][40];
static int tau(void) {
    for (int k = 0; k <= n; k++) {
        if (k == 0) { if (ne == 0) return 0; continue; }
        uint32_t S = (1u << k) - 1;
        while (S < (1u << n)) { int ok = 1; for (int i = 0; i < ne; i++) if (!(E[i] & S)) { ok = 0; break; } if (ok) return k;
            uint32_t c = S & -S, r = S + c; S = (((r ^ S) >> 2) / c) | r; }
    }
    return n;
}
static int connected_spanning(void) {
    uint32_t all = (1u << n) - 1, used = 0; for (int i = 0; i < ne; i++) used |= E[i];
    if (used != all) return 0;
    uint32_t comp = 1u, prev = 0; while (comp != prev) { prev = comp; for (int i = 0; i < ne; i++) if (E[i] & comp) comp |= E[i]; }
    return comp == all;
}
static void rec(int start) {
    if (ne > 0 && connected_spanning()) { int md = 0; for (int v = 0; v < n; v++) if (deg[v] > md) md = deg[v]; cnt[ne][tau()][md]++; }
    for (int t = start; t < nt; t++) {
        uint32_t e = T[t]; int a = __builtin_ctz(e), b = __builtin_ctz(e & (e-1)), c = 31 - __builtin_clz(e);
        if (deg[a] >= D || deg[b] >= D || deg[c] >= D) continue;
        if ((nb[a] >> b & 1) || (nb[a] >> c & 1) || (nb[b] >> c & 1)) continue;
        E[ne++] = e; deg[a]++; deg[b]++; deg[c]++; nb[a] |= (1u<<b)|(1u<<c); nb[b] |= (1u<<a)|(1u<<c); nb[c] |= (1u<<a)|(1u<<b);
        rec(t + 1);
        nb[a] &= ~((1u<<b)|(1u<<c)); nb[b] &= ~((1u<<a)|(1u<<c)); nb[c] &= ~((1u<<a)|(1u<<b)); deg[a]--; deg[b]--; deg[c]--; ne--;
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); D = atoi(argv[2]); nt = 0;
    for (int a = 0; a < n; a++) for (int b = a+1; b < n; b++) for (int c = b+1; c < n; c++) T[nt++] = (1u<<a)|(1u<<b)|(1u<<c);
    rec(0);
    for (int m = 0; m < 40; m++) for (int t = 0; t < 40; t++) for (int d = 0; d < 40; d++) if (cnt[m][t][d]) printf("%d %d %d %d %llu\n", n, m, t, d, cnt[m][t][d]);
    return 0;
}
