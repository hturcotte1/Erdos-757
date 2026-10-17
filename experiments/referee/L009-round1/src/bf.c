/* Referee L009: brute force over ALL labelled 3-graphs on [n] with exactly m edges (edges = m-subsets of the C(n,3) triples, in
   increasing order), pruned only by linearity and max degree <= D (both inherited by subsets).  At the leaves: every vertex
   covered, connected, tau >= T (exact, by testing all vertex subsets of size T-1).  Counts labelled hypergraphs, and those in C
   (F7-free, P3).  Optionally prints them (PRINT=1) as "B: (a,b,c) ...".
   Usage: bf n m T D [print] */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, m, T, D, PR = 0;
static uint32_t tri[1200]; static int ntri = 0;
static uint32_t E[32]; static int deg[32];
static unsigned long long cnt = 0, cntC = 0, leaves = 0;
static int connected(void) {
    uint32_t comp = E[0], prev = 0;
    while (comp != prev) { prev = comp; for (int i = 0; i < m; i++) if (E[i] & comp) comp |= E[i]; }
    return comp == (1u << n) - 1;
}
static int tau_ge(void) {   /* no vertex subset of size T-1 meets all edges */
    if (T <= 0) return 1;
    int k = T - 1;
    if (k == 0) return m > 0;
    uint32_t S = (1u << k) - 1;
    while (S < (1u << n)) {
        int ok = 1; for (int i = 0; i < m; i++) if (!(E[i] & S)) { ok = 0; break; }
        if (ok) return 0;
        uint32_t c = S & -S, r = S + c; S = (((r ^ S) >> 2) / c) | r;
    }
    return 1;
}
static int f7(void) {
    int ix[5];
    for (ix[0] = 0; ix[0] < m; ix[0]++) for (ix[1] = ix[0]+1; ix[1] < m; ix[1]++) for (ix[2] = ix[1]+1; ix[2] < m; ix[2]++)
    for (ix[3] = ix[2]+1; ix[3] < m; ix[3]++) for (ix[4] = ix[3]+1; ix[4] < m; ix[4]++) {
        /* direct test against the definition: find a bijection to F7 = {012,034,056,135,246}: the five edges, a vertex of
           degree 3 within them, ... here: brute force over the 5! orders of the edges and check the incidence pattern */
        uint32_t U = 0; for (int a = 0; a < 5; a++) U |= E[ix[a]];
        if (__builtin_popcount(U) != 7) continue;
        static const int P[120][5] = {{0}}; (void)P;
        int perm[5] = {0,1,2,3,4};
        /* iterate permutations (Heap's algorithm, iterative) */
        int c[5] = {0,0,0,0,0}, i = 0, found = 0;
        for (;;) {
            uint32_t A = E[ix[perm[0]]], B = E[ix[perm[1]]], Cc = E[ix[perm[2]]], Dd = E[ix[perm[3]]], Ee = E[ix[perm[4]]];
            /* F7 pattern: A,B,C share one common vertex x (the 012,034,056 edges) and are otherwise disjoint;
               D,E disjoint; D and E each meet each of A,B,C in exactly one vertex different from x */
            uint32_t x = A & B & Cc;
            if (__builtin_popcount(x) == 1 && __builtin_popcount(A & B) == 1 && __builtin_popcount(A & Cc) == 1 && __builtin_popcount(B & Cc) == 1
                && !(Dd & Ee) && !(Dd & x) && !(Ee & x)
                && __builtin_popcount(Dd & A) == 1 && __builtin_popcount(Dd & B) == 1 && __builtin_popcount(Dd & Cc) == 1
                && __builtin_popcount(Ee & A) == 1 && __builtin_popcount(Ee & B) == 1 && __builtin_popcount(Ee & Cc) == 1) { found = 1; break; }
            while (i < 5 && c[i] >= i) { c[i] = 0; i++; }
            if (i >= 5) break;
            int j = (i % 2 == 0) ? 0 : c[i]; int t = perm[j]; perm[j] = perm[i]; perm[i] = t; c[i]++; i = 0;
        }
        if (found) return 1;
    }
    return 0;
}
static int p3(void) {
    for (uint32_t F = 1; F < (1u << m); F++) { uint32_t U = 0; for (int j = 0; j < m; j++) if (F >> j & 1) U |= E[j];
        if (__builtin_popcount(U) < __builtin_popcount(F) + 2) return 0; }
    return 1;
}
static void rec(int start, int k) {
    if (k == m) {
        leaves++;
        uint32_t U = 0; for (int i = 0; i < m; i++) U |= E[i];
        if (U != (1u << n) - 1 || !connected() || !tau_ge()) return;
        cnt++;
        int inC = !f7() && p3(); cntC += inC;
        if (PR) { printf("B C=%d:", inC); for (int i = 0; i < m; i++) { printf(" ("); int f = 1; for (int v = 0; v < n; v++) if (E[i] >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } printf(")"); } printf("\n"); }
        return;
    }
    for (int t = start; t <= ntri - (m - k); t++) {
        uint32_t e = tri[t]; int ok = 1;
        for (int i = 0; i < k; i++) if (__builtin_popcount(E[i] & e) >= 2) { ok = 0; break; }
        if (!ok) continue;
        for (int v = 0; v < n; v++) if ((e >> v & 1) && deg[v] >= D) { ok = 0; break; }
        if (!ok) continue;
        E[k] = e; for (int v = 0; v < n; v++) if (e >> v & 1) deg[v]++;
        rec(t + 1, k + 1);
        for (int v = 0; v < n; v++) if (e >> v & 1) deg[v]--;
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); m = atoi(argv[2]); T = atoi(argv[3]); D = atoi(argv[4]); if (argc > 5) PR = atoi(argv[5]);
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) tri[ntri++] = (1u << a) | (1u << b) | (1u << c);
    rec(0, 0);
    fprintf(PR ? stderr : stdout, "BF n=%d m=%d T=%d D=%d leaves=%llu labelled=%llu labelled_in_C=%llu\n", n, m, T, D, leaves, cnt, cntC);
    return 0;
}
