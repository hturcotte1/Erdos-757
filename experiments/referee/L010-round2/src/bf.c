/* bf.c -- referee L010 round 2: labelled brute force (no isomorph rejection, no nauty).
   Counts all 3-graphs on the labelled vertex set {0..n-1} with exactly M edges that are linear, have max degree <= D and
   min degree >= DMIN, are connected (CONN=1: every vertex reachable from 0) or arbitrary (CONN=0), and tau >= T0.
   Also reports how many of them are F7-free and satisfy (P3).  DFS over the C(n,3) triples in lexicographic order.
   Usage: bf n M T0 D DMIN CONN */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, M, T0, D, DMIN, CONN, PRINT = 0; static int tri[1000][3], nt;
static uint32_t E[64]; static int ne, deg[32]; static uint32_t pairs[32];
static unsigned long long cnt = 0, cntC = 0, hist[40], histC[40];
static int cov(uint64_t left, int k) { if (!left) return 1; if (k <= 0) return 0; int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int v = __builtin_ctz(e); e &= e - 1; uint64_t l2 = left; for (int j = 0; j < ne; j++) if (E[j] >> v & 1) l2 &= ~(1ull << j); if (cov(l2, k - 1)) return 1; } return 0; }
static int has_f7(void) { /* pair of disjoint edges + outside vertex p with >= 3 edges meeting both once (linear graphs) */
    for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) { if (E[i] & E[j]) continue; uint32_t U = E[i] | E[j];
        for (int p = 0; p < n; p++) { if (U >> p & 1) continue; int c = 0;
            for (int t = 0; t < ne; t++) if ((E[t] >> p & 1) && __builtin_popcount(E[t] & E[i]) == 1 && __builtin_popcount(E[t] & E[j]) == 1) c++;
            if (c >= 3) return 1; } }
    return 0; }
static int p3(void) { for (uint32_t F = 1; F < (1u << ne); F++) { uint32_t U = 0; int c = 0; for (int j = 0; j < ne; j++) if (F >> j & 1) { U |= E[j]; c++; }
    if (__builtin_popcount(U) < c + 2) return 0; } return 1; }
static int conn(void) { uint32_t R = 1, P = 0; while (R != P) { P = R; for (int j = 0; j < ne; j++) if (E[j] & R) R |= E[j]; } return R == ((1u << n) - 1); }
static void rec(int i) {
    if (ne == M) {
        for (int v = 0; v < n; v++) if (deg[v] < DMIN) return;
        if (CONN && !conn()) return;
        int t = 0; while (!cov((1ull << ne) - 1, t)) t++;
        hist[t]++; int inC = (!has_f7() && p3()); histC[t] += inC;
        if (t < T0) return;
        cnt++; cntC += inC;
        if (PRINT) { printf("L:"); for (int j = 0; j < ne; j++) { uint32_t e = E[j]; int a = __builtin_ctz(e); e &= e - 1; int b = __builtin_ctz(e); e &= e - 1; printf(" (%d,%d,%d)", a, b, __builtin_ctz(e)); } printf("\n"); }
        return;
    }
    if (nt - i < M - ne) return;
    for (int t = i; t < nt; t++) {
        int a = tri[t][0], b = tri[t][1], c = tri[t][2];
        if (deg[a] >= D || deg[b] >= D || deg[c] >= D) continue;
        if ((pairs[a] >> b & 1) || (pairs[a] >> c & 1) || (pairs[b] >> c & 1)) continue;
        E[ne++] = (1u << a) | (1u << b) | (1u << c); deg[a]++; deg[b]++; deg[c]++;
        pairs[a] |= (1u << b) | (1u << c); pairs[b] |= (1u << a) | (1u << c); pairs[c] |= (1u << a) | (1u << b);
        rec(t + 1);
        ne--; deg[a]--; deg[b]--; deg[c]--;
        pairs[a] &= ~((1u << b) | (1u << c)); pairs[b] &= ~((1u << a) | (1u << c)); pairs[c] &= ~((1u << a) | (1u << b));
    }
}
int main(int argc, char **argv) {
    if (getenv("BFPRINT")) PRINT = 1;
    n = atoi(argv[1]); M = atoi(argv[2]); T0 = atoi(argv[3]); D = atoi(argv[4]); DMIN = atoi(argv[5]); CONN = atoi(argv[6]);
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) { tri[nt][0] = a; tri[nt][1] = b; tri[nt][2] = c; nt++; }
    rec(0);
    printf("BF n=%d M=%d T0=%d D=%d DMIN=%d CONN=%d labelled=%llu labelled_inC=%llu", n, M, T0, D, DMIN, CONN, cnt, cntC);
    printf(" hist"); for (int t = 0; t <= M; t++) printf(" %d:%llu:%llu", t, hist[t], histC[t]); printf("\n");
    return 0;
}
