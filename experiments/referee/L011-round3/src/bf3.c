/* Referee L011 round 3: labelled brute force.  Usage: bf3 N M T0 D [print] : every labelled linear 3-graph on points 0..N-1 with
   exactly M edges, every point degree in [1,D] (so no isolated point), connected, tau >= T0.  DFS over triples in lexicographic
   order; linearity and degree enforced incrementally.  Prints "L: (a,b,c) ..." lines and a count. */
#include "common3.h"
static int N, M, T0, D, PR; static uint32_t tri[8192]; static int nt;
static HG h; static int deg[32]; static uint32_t pairused[32]; static unsigned long long cnt = 0, leaves = 0;
static void rec(int start, int placed) {
    if (placed == M) {
        leaves++;
        for (int x = 0; x < N; x++) if (deg[x] < 1) return;
        hg_build(&h, N); int sz[32]; if (hg_components(&h, sz) != 1) return;
        if (hg_tau(&h) < T0) return;
        cnt++; if (PR) { printf("L:"); hg_print(stdout, &h); printf("\n"); }
        return;
    }
    if (nt - start < M - placed) return;
    for (int t = start; t < nt; t++) {
        uint32_t e = tri[t]; int v[3], k = 0; for (uint32_t f = e; f; f &= f - 1) v[k++] = __builtin_ctz(f);
        if (deg[v[0]] >= D || deg[v[1]] >= D || deg[v[2]] >= D) continue;
        if ((pairused[v[0]] >> v[1] & 1) || (pairused[v[0]] >> v[2] & 1) || (pairused[v[1]] >> v[2] & 1)) continue;
        h.E[placed] = e; deg[v[0]]++; deg[v[1]]++; deg[v[2]]++;
        pairused[v[0]] |= (1u << v[1]) | (1u << v[2]); pairused[v[1]] |= (1u << v[0]) | (1u << v[2]); pairused[v[2]] |= (1u << v[0]) | (1u << v[1]);
        h.ne = placed + 1; rec(t + 1, placed + 1);
        deg[v[0]]--; deg[v[1]]--; deg[v[2]]--;
        pairused[v[0]] &= ~((1u << v[1]) | (1u << v[2])); pairused[v[1]] &= ~((1u << v[0]) | (1u << v[2])); pairused[v[2]] &= ~((1u << v[0]) | (1u << v[1]));
    }
}
int main(int argc, char **argv) {
    N = atoi(argv[1]); M = atoi(argv[2]); T0 = atoi(argv[3]); D = atoi(argv[4]); PR = argc > 5;
    nt = 0; for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) for (int c = b + 1; c < N; c++) tri[nt++] = (1u << a) | (1u << b) | (1u << c);
    h.ne = 0; rec(0, 0);
    printf("BFSUM N=%d M=%d T0=%d D=%d labelled=%llu leaves=%llu\n", N, M, T0, D, cnt, leaves);
    return 0;
}
