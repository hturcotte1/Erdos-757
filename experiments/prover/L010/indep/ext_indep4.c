/* ext_indep4.c (= ext_indep3.c with MAXT 65536 and Gosper-hack enumeration of the (TG-1)- and TG-subsets; for 18/19-vertex inputs, certificate L010)
   ext_indep3.c (= ext_indep2.c with MAXT 32768, for 17-vertex inputs) -- independent re-implementation (prover, certificates L008, L009) of the vertex-extension step, using a different
   tau test from ext_vertex2.c.
   Usage: ext_indep2 NG TG MAXDEG < input      input lines "m a1 b1 c1 ... am bm cm" (a 3-graph G on vertices 0..NG-1).
   For each G: checks tau(G) = TG exactly (no transversal of size TG-1, at least one of size TG), lists ALL transversals of G of
   size TG, and for every unordered triple of pairwise disjoint pairs {a_i,b_i} of V(G) such that no pair lies inside an edge of
   G and every a_i, b_i has G-degree <= MAXDEG-1, forms H = G + {NG,a_i,b_i} (i=1,2,3).
   A transversal of H with at most TG vertices cannot contain NG (its rest would be a transversal of G of size TG-1), so
   tau(H) <= TG  iff  some TG-transversal of G meets all three pairs.  Prints every H with tau(H) >= TG+1 as "HIT: (..) ..".
   Implementation: for each admissible pair p a bitset over the TG-transversals (bit j = transversal j meets p); a triple is
   a hit iff the AND of its three bitsets is zero. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define MAXT 65536
#define W (MAXT / 64)
static uint64_t bs[256][W];
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: ext_indep2 NG TG MAXDEG < input\n"); return 1; }
    int NG = atoi(argv[1]), TG = atoi(argv[2]), MD = atoi(argv[3]);
    int m; unsigned long long graphs = 0, tested = 0, hits = 0, bad_tau = 0;
    static uint32_t tr[MAXT];
    while (scanf("%d", &m) == 1) {
        uint32_t g[32]; int deg[32] = {0};
        for (int i = 0; i < m; i++) { int a, b, c; if (scanf("%d %d %d", &a, &b, &c) != 3) return 2;
            g[i] = (1u << a) | (1u << b) | (1u << c); deg[a]++; deg[b]++; deg[c]++; }
        graphs++;
        int nt = 0, small = 0;
        /* all vertex subsets of size TG-1 and TG, by Gosper's hack (instead of scanning all 2^NG subsets) */
        for (int p = TG - 1; p <= TG; p++) {
            if (p < 0 || p > NG) continue;
            uint32_t S = (p == 0) ? 0 : ((1u << p) - 1);
            while (1) {
                int ok = 1; for (int i = 0; i < m; i++) if (!(g[i] & S)) { ok = 0; break; }
                if (ok) { if (p == TG - 1) small++; else { if (nt >= MAXT) { fprintf(stderr, "MAXT\n"); return 3; } tr[nt++] = S; } }
                if (p == 0) break;
                uint32_t c = S & -S, r = S + c; S = (((r ^ S) >> 2) / c) | r;
                if (S >= (1u << NG)) break;
            }
        }
        if (small || nt == 0) { bad_tau++; continue; }
        int words = (nt + 63) / 64;
        uint32_t pr[256]; int np = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > MD - 1 || deg[b] > MD - 1) continue;
            uint32_t p = (1u << a) | (1u << b); int ok = 1;
            for (int i = 0; i < m; i++) if ((g[i] & p) == p) { ok = 0; break; }
            if (!ok) continue;
            memset(bs[np], 0, sizeof(uint64_t) * words);
            for (int j = 0; j < nt; j++) if (tr[j] & p) bs[np][j >> 6] |= 1ull << (j & 63);
            pr[np++] = p;
        }
        for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) {
            if (pr[x] & pr[y]) continue;
            for (int z = y + 1; z < np; z++) {
                if ((pr[x] | pr[y]) & pr[z]) continue;
                tested++;
                int covered = 0;
                for (int w = 0; w < words; w++) if (bs[x][w] & bs[y][w] & bs[z][w]) { covered = 1; break; }
                if (covered) continue;
                hits++;
                printf("HIT:");
                for (int i = 0; i < m; i++) { printf(" ("); int f = 1; for (int v = 0; v < NG; v++) if (g[i] >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } printf(")"); }
                uint32_t three[3] = { pr[x], pr[y], pr[z] };
                for (int j = 0; j < 3; j++) { printf(" ("); int f = 1; for (int v = 0; v < NG; v++) if (three[j] >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } printf(",%d)", NG); }
                printf("\n");
            }
        }
    }
    printf("SUMMARY graphs=%llu bad_tau=%llu tested=%llu hits=%llu\n", graphs, bad_tau, tested, hits);
    return 0;
}
