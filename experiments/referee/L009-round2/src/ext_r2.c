/* ext_r2.c -- referee L009 round 2: one-vertex extensions with an exact tau computation (written from scratch for this review).
   Usage: ext_r2 NG TMIN MAXDEG [print] < input
   Input: one hypergraph per line, edges written as "(a,b,c)" anywhere on the line (other text ignored), vertices 0..NG-1.
   For each G, every unordered triple of pairwise disjoint pairs {a_i,b_i} of V(G) such that no pair lies inside an edge of G and
   every endpoint has G-degree <= MAXDEG-1 gives H = G + {NG,a_i,b_i} (i=1,2,3); tau(H) is computed EXACTLY (branching on an
   uncovered edge, matching lower bound) and H is printed as "XHIT: ..." when tau(H) >= TMIN (if print=1).
   Summary: number of inputs, extensions, histogram of tau(H)-tau(G), hits.                                                          */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int NE; static uint32_t E[64]; static uint64_t INC[32];
static int cover_le(uint64_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    uint64_t l = left; uint32_t used = 0; int cnt = 0;
    while (l) { int i = __builtin_ctzll(l); l &= l - 1; if (!(E[i] & used)) { used |= E[i]; if (++cnt > k) return 0; } }
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int x = __builtin_ctz(e); e &= e - 1; if (cover_le(left & ~INC[x], k - 1)) return 1; }
    return 0;
}
static void build_inc(int nv) {
    for (int x = 0; x < nv; x++) INC[x] = 0;
    for (int j = 0; j < NE; j++) for (int x = 0; x < nv; x++) if (E[j] >> x & 1) INC[x] |= 1ull << j;
}
static int tau_exact(int nv) { build_inc(nv); uint64_t all = (NE >= 64) ? ~0ull : ((1ull << NE) - 1); int k = 0; while (!cover_le(all, k)) k++; return k; }
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: ext_r2 NG TMIN MAXDEG [print]\n"); return 1; }
    int NG = atoi(argv[1]), TMIN = atoi(argv[2]), MD = atoi(argv[3]), PR = argc > 4 ? atoi(argv[4]) : 1;
    static char line[1 << 16];
    unsigned long long inputs = 0, ext = 0, hits = 0, hist[8] = {0}; int tg_min = 99, tg_max = -1;
    while (fgets(line, sizeof line, stdin)) {
        uint32_t G[64]; int ng = 0; char *p = line;
        while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) == 3) { if (a >= NG || b >= NG || c >= NG) { fprintf(stderr, "vertex out of range\n"); return 2; } G[ng++] = (1u << a) | (1u << b) | (1u << c); } p++; }
        if (!ng) continue;
        inputs++;
        int deg[32] = {0}; for (int j = 0; j < ng; j++) for (int x = 0; x < NG; x++) if (G[j] >> x & 1) deg[x]++;
        NE = ng; memcpy(E, G, sizeof(uint32_t) * ng); int tg = tau_exact(NG);
        if (tg < tg_min) tg_min = tg; if (tg > tg_max) tg_max = tg;
        uint32_t pr[600]; int np = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > MD - 1 || deg[b] > MD - 1) continue;
            uint32_t q = (1u << a) | (1u << b); int inside = 0;
            for (int j = 0; j < ng; j++) if ((G[j] & q) == q) { inside = 1; break; }
            if (!inside) pr[np++] = q;
        }
        for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) { if (pr[x] & pr[y]) continue;
            for (int z = y + 1; z < np; z++) { if ((pr[x] | pr[y]) & pr[z]) continue;
                NE = ng + 3; memcpy(E, G, sizeof(uint32_t) * ng);
                E[ng] = pr[x] | (1u << NG); E[ng + 1] = pr[y] | (1u << NG); E[ng + 2] = pr[z] | (1u << NG);
                int th = tau_exact(NG + 1); ext++;
                int dlt = th - tg; if (dlt >= 0 && dlt < 8) hist[dlt]++;
                if (th >= TMIN) { hits++; if (PR) { printf("XHIT: tau=%d", th); for (int j = 0; j < NE; j++) { printf(" ("); int f = 1; for (int v = 0; v <= NG; v++) if (E[j] >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } printf(")"); } printf("\n"); } }
            } }
    }
    printf("EXT_R2 NG=%d TMIN=%d MAXDEG=%d inputs=%llu tau(G) in [%d,%d] extensions=%llu hits=%llu tau(H)-tau(G) histogram: 0:%llu 1:%llu\n",
           NG, TMIN, MD, inputs, tg_min, tg_max, ext, hits, hist[0], hist[1]);
    return 0;
}
