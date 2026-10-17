/* ext_indep.c -- independent re-implementation (prover L007) of the vertex-extension step, by a different tau test.
   Input: lines "8 a1 b1 c1 ... a8 b8 c8" (a 3-graph G on vertices 0..12 with 8 edges).
   For each G: checks tau(G) = 5 exactly (no 4-transversal; some 5-transversal), lists ALL 5-transversals of G,
   and for every unordered triple of pairwise disjoint pairs {a_i,b_i} of V(G), none contained in an edge of G,
   forms H = G + {13,a_i,b_i} (i=1,2,3).  Since tau(G) = 5, a transversal of H of size <= 5 cannot contain 13
   (its rest would be a 4-transversal of G), so tau(H) <= 5 iff some 5-transversal of G meets all three pairs.
   Prints every H with tau(H) >= 6 as "HIT: (..) .." and a summary line. */
#include <stdio.h>
#include <stdint.h>
int main(void) {
    int m; unsigned long long graphs = 0, tested = 0, hits = 0, bad_tau = 0;
    while (scanf("%d", &m) == 1) {
        uint32_t g[16];
        for (int i = 0; i < m; i++) { int a, b, c; if (scanf("%d %d %d", &a, &b, &c) != 3) return 2; g[i] = (1u<<a)|(1u<<b)|(1u<<c); }
        graphs++;
        /* all transversals of size 4 and 5 */
        uint32_t t5[1300]; int n5 = 0, n4 = 0;
        for (uint32_t S = 0; S < (1u << 13); S++) {
            int p = __builtin_popcount(S); if (p != 4 && p != 5) continue;
            int ok = 1; for (int i = 0; i < m; i++) if (!(g[i] & S)) { ok = 0; break; }
            if (!ok) continue;
            if (p == 4) n4++; else t5[n5++] = S;
        }
        if (n4 != 0 || n5 == 0) { bad_tau++; continue; }
        /* admissible pairs */
        uint32_t pr[78]; int np = 0;
        for (int a = 0; a < 13; a++) for (int b = a + 1; b < 13; b++) {
            uint32_t p = (1u<<a)|(1u<<b); int ok = 1;
            for (int i = 0; i < m; i++) if ((g[i] & p) == p) { ok = 0; break; }
            if (ok) pr[np++] = p;
        }
        for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) {
            if (pr[x] & pr[y]) continue;
            for (int z = y + 1; z < np; z++) {
                if ((pr[x] | pr[y]) & pr[z]) continue;
                tested++;
                int covered = 0;
                for (int k = 0; k < n5; k++) { uint32_t T = t5[k]; if ((T & pr[x]) && (T & pr[y]) && (T & pr[z])) { covered = 1; break; } }
                if (covered) continue;
                hits++;
                printf("HIT:");
                uint32_t all[3] = { pr[x], pr[y], pr[z] };
                for (int i = 0; i < m; i++) { printf(" ("); int f = 1; for (int v = 0; v < 13; v++) if (g[i] >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } printf(")"); }
                for (int j = 0; j < 3; j++) { printf(" ("); int f = 1; for (int v = 0; v < 13; v++) if (all[j] >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } printf(",13)"); }
                printf("\n");
            }
        }
    }
    printf("graphs=%llu bad_tau=%llu tested=%llu hits(tau>=6)=%llu\n", graphs, bad_tau, tested, hits);
    return 0;
}
