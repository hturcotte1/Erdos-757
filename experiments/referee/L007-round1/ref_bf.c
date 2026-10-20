/* ref_bf.c -- referee brute force: all LABELLED linear 3-graphs on [n] (DFS over the C(n,3) triples in index order,
   each triple in or out, no symmetry reduction).  For every edge set that is spanning (every vertex in an edge) and
   connected, tally (m, tau, maxdeg).  Output lines: "n m tau maxdeg count". */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, T; static int tr[200][3]; static uint32_t tm[200];
static int E[40], ne = 0; static uint32_t cov[32]; /* cov[v]: vertices paired with v */
static unsigned long long tally[40][16][16];
static int hit(uint32_t rem, int k) { /* rem: edge-index mask into E */
    if (!rem) return 1; if (!k) return 0;
    int i = __builtin_ctz(rem);
    for (int j = 0; j < 3; j++) { int v = tr[E[i]][j]; uint32_t r2 = rem;
        for (int q = 0; q < ne; q++) if ((r2 >> q & 1) && (tm[E[q]] >> v & 1)) r2 &= ~(1u << q);
        if (hit(r2, k - 1)) return 1; }
    return 0; }
static void leaf(void) {
    uint32_t U = 0; for (int i = 0; i < ne; i++) U |= tm[E[i]];
    if (U != (1u << n) - 1) return;
    /* connectivity */
    uint32_t seen = 1, fr = 1;
    while (fr) { uint32_t nf = 0; for (int i = 0; i < ne; i++) if (tm[E[i]] & seen) nf |= tm[E[i]]; nf &= ~seen; seen |= nf; fr = nf; }
    if (seen != U) return;
    int t = 0; uint32_t all = ne == 32 ? 0xffffffffu : ((1u << ne) - 1); while (!hit(all, t)) t++;
    int dg[32] = {0}, mx = 0; for (int i = 0; i < ne; i++) for (int j = 0; j < 3; j++) { int v = tr[E[i]][j]; if (++dg[v] > mx) mx = dg[v]; }
    tally[ne][t][mx]++;
}
static void dfs(int i) {
    if (i == T) { if (ne > 0) leaf(); return; }
    dfs(i + 1);
    int a = tr[i][0], b = tr[i][1], c = tr[i][2];
    if ((cov[a] >> b & 1) || (cov[a] >> c & 1) || (cov[b] >> c & 1)) return;
    cov[a] |= (1u<<b)|(1u<<c); cov[b] |= (1u<<a)|(1u<<c); cov[c] |= (1u<<a)|(1u<<b);
    E[ne++] = i; dfs(i + 1); ne--;
    cov[a] &= ~((1u<<b)|(1u<<c)); cov[b] &= ~((1u<<a)|(1u<<c)); cov[c] &= ~((1u<<a)|(1u<<b));
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); T = 0;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) { tr[T][0]=a; tr[T][1]=b; tr[T][2]=c; tm[T]=(1u<<a)|(1u<<b)|(1u<<c); T++; }
    dfs(0);
    for (int m = 0; m < 40; m++) for (int t = 0; t < 16; t++) for (int d = 0; d < 16; d++) if (tally[m][t][d]) printf("%d %d %d %d %llu\n", n, m, t, d, tally[m][t][d]);
    return 0; }
