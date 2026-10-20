/* bf.c -- referee L010 round 3 (written from scratch).  Labelled brute force: every linear 3-uniform hypergraph on vertex set
   {0..N-1} with exactly M edges (edges chosen as an increasing sequence of triples in lexicographic order; linearity enforced
   while building), connected (all N vertices in one component), max degree <= D, tau >= T0.  Prints each as "FOUND: (a,b,c) ..."
   and a count.  Usage: bf N M T0 D */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int N, M, T0, D; static uint32_t tri[2000]; static int ntri;
static uint32_t ch[32]; static int deg[32]; static uint32_t nb[32];
static unsigned long long found = 0, total_conn = 0;
static int coverable(int k, uint32_t left) { if (!left) return 1; if (k <= 0) return 0; int i = __builtin_ctz(left); uint32_t e = ch[i];
    while (e) { int v = __builtin_ctz(e); e &= e - 1; uint32_t l2 = left; for (int j = 0; j < M; j++) if ((l2 >> j & 1) && (ch[j] >> v & 1)) l2 &= ~(1u << j); if (coverable(k - 1, l2)) return 1; } return 0; }
static int tau(void) { int k = 0; while (!coverable(k, (1u << M) - 1)) k++; return k; }
static int connected(void) { uint32_t comp = 1u, prev = 0; while (comp != prev) { prev = comp; for (int i = 0; i < M; i++) if (ch[i] & comp) comp |= ch[i]; } return comp == (1u << N) - 1; }
static void rec(int k, int start) {
    if (k == M) { if (!connected()) return; total_conn++; if (tau() >= T0) { found++; printf("FOUND:"); for (int i = 0; i < M; i++) { printf(" ("); int f = 1; for (int v = 0; v < N; v++) if (ch[i] >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } printf(")"); } printf("\n"); } return; }
    for (int t = start; t < ntri; t++) { uint32_t e = tri[t]; int a = __builtin_ctz(e), b = __builtin_ctz(e & (e - 1)), c = 31 - __builtin_clz(e);
        if (deg[a] >= D || deg[b] >= D || deg[c] >= D) continue;
        if ((nb[a] >> b & 1) || (nb[a] >> c & 1) || (nb[b] >> c & 1)) continue;   /* a pair already inside an edge: not linear */
        ch[k] = e; deg[a]++; deg[b]++; deg[c]++; uint32_t sa = nb[a], sb = nb[b], sc = nb[c]; nb[a] |= e; nb[b] |= e; nb[c] |= e;
        rec(k + 1, t + 1);
        nb[a] = sa; nb[b] = sb; nb[c] = sc; deg[a]--; deg[b]--; deg[c]--; }
}
int main(int argc, char **argv) { if (argc < 5) return 1; N = atoi(argv[1]); M = atoi(argv[2]); T0 = atoi(argv[3]); D = atoi(argv[4]);
    for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) for (int c = b + 1; c < N; c++) tri[ntri++] = (1u << a) | (1u << b) | (1u << c);
    rec(0, 0); printf("BF N=%d M=%d T0=%d D=%d connected_linear_labelled=%llu found=%llu\n", N, M, T0, D, total_conn, found); return 0; }
