/* Referee L011: labelled brute force for validating the genbg pipeline.
   Counts all LABELLED connected linear 3-graphs on exactly the points 0..n-1 (every point in an edge), with m edges and
   maximum degree <= D, by tau.  Hyperedges are chosen as increasing sequences of triples (each edge set once).
   Usage: rbf n D   -> lines "n D m tau count" */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, D, NT; static uint32_t T[400]; static uint64_t TP[400];
static int pidx[16][16];
static uint32_t ch[64]; static int deg[16];
static unsigned long long cnt[64][32];
static int coverle(int m, uint64_t left, int k) {
    if (!left) return 1; if (k <= 0) return 0;
    int i = __builtin_ctzll(left); uint32_t e = ch[i];
    while (e) { int x = __builtin_ctz(e); e &= e - 1; uint64_t l = left;
        for (int j = 0; j < m; j++) if (ch[j] >> x & 1) l &= ~(1ull << j);
        if (coverle(m, l, k - 1)) return 1; }
    return 0;
}
static void rec(int start, int m, uint64_t pairs) {
    if (m > 0) {
        uint32_t U = 0; for (int i = 0; i < m; i++) U |= ch[i];
        if (U == (1u << n) - 1) {
            uint32_t comp = ch[0], prev = 0;
            while (comp != prev) { prev = comp; for (int i = 0; i < m; i++) if (ch[i] & comp) comp |= ch[i]; }
            if (comp == U) { int t = 0; while (!coverle(m, (1ull << m) - 1, t)) t++; cnt[m][t]++; }
        }
    }
    for (int i = start; i < NT; i++) {
        if (TP[i] & pairs) continue;
        uint32_t e = T[i]; int ok = 1;
        for (uint32_t f = e; f; f &= f - 1) if (deg[__builtin_ctz(f)] >= D) { ok = 0; break; }
        if (!ok) continue;
        for (uint32_t f = e; f; f &= f - 1) deg[__builtin_ctz(f)]++;
        ch[m] = e; rec(i + 1, m + 1, pairs | TP[i]);
        for (uint32_t f = e; f; f &= f - 1) deg[__builtin_ctz(f)]--;
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); D = atoi(argv[2]);
    int k = 0; for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) pidx[a][b] = k++;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) {
        T[NT] = (1u << a) | (1u << b) | (1u << c);
        TP[NT] = (1ull << pidx[a][b]) | (1ull << pidx[a][c]) | (1ull << pidx[b][c]); NT++; }
    rec(0, 0, 0);
    for (int m = 1; m < 64; m++) for (int t = 0; t < 32; t++) if (cnt[m][t]) printf("%d %d %d %d %llu\n", n, D, m, t, cnt[m][t]);
    return 0;
}
