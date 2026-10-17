/* ref_ext.c -- referee's vertex-extension check (Route I, Step 5.2), written from scratch.
   Input: lines "G: (a,b,c) (a,b,c) ..." describing a 3-graph G on vertices 0..12 (any number of edges <= 20).
   For each G: all unordered triples of pairwise disjoint pairs {x_i,y_i} of {0..12} such that no pair lies inside an
   edge of G; H = G + {x_i,y_i,13}.  tau(H) is computed exactly (branching on an unhit edge) and H is printed if
   tau(H) >= TMIN (argv[1]).  Also checks linearity of G and of every H.  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int ne; static uint32_t em[32]; static uint32_t incv[32];
static int hit(uint32_t rem, int k) {
    if (!rem) return 1; if (!k) return 0;
    int i = __builtin_ctz(rem); uint32_t e = em[i];
    while (e) { int v = __builtin_ctz(e); e &= e - 1; if (hit(rem & ~incv[v], k - 1)) return 1; }
    return 0;
}
static int tau(void) { uint32_t all = (1u << ne) - 1; int t = 0; while (!hit(all, t)) t++; return t; }
static void rebuild(void) { memset(incv, 0, sizeof incv); for (int i = 0; i < ne; i++) for (int v = 0; v < 32; v++) if (em[i] >> v & 1) incv[v] |= 1u << i; }
static int linear(void) { for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) if (__builtin_popcount(em[i] & em[j]) > 1) return 0; return 1; }
int main(int argc, char **argv) {
    int TMIN = atoi(argv[1]);
    char line[4096]; unsigned long long graphs = 0, tested = 0, hits = 0, nonlin = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, "G:", 2)) continue;
        int g = 0; uint32_t ge[32]; char *p = line + 2; int a, b, c, k;
        while (sscanf(p, " (%d,%d,%d)%n", &a, &b, &c, &k) == 3) { ge[g++] = (1u << a) | (1u << b) | (1u << c); p += k; }
        graphs++;
        uint32_t pr[100]; int np = 0;
        for (int x = 0; x < 13; x++) for (int y = x + 1; y < 13; y++) {
            uint32_t q = (1u << x) | (1u << y); int ok = 1;
            for (int i = 0; i < g; i++) if ((ge[i] & q) == q) ok = 0;
            if (ok) pr[np++] = q;
        }
        ne = g; memcpy(em, ge, sizeof(uint32_t) * g); if (!linear()) nonlin++;
        for (int i = 0; i < np; i++) for (int j = i + 1; j < np; j++) if (!(pr[i] & pr[j]))
            for (int l = j + 1; l < np; l++) if (!((pr[i] | pr[j]) & pr[l])) {
                ne = g; memcpy(em, ge, sizeof(uint32_t) * g);
                em[ne++] = pr[i] | (1u << 13); em[ne++] = pr[j] | (1u << 13); em[ne++] = pr[l] | (1u << 13);
                rebuild(); tested++;
                if (!linear()) nonlin++;
                if (tau() >= TMIN) {
                    hits++; printf("HIT:");
                    for (int q = 0; q < ne; q++) { printf(" ("); int f = 1; for (int v = 0; v < 14; v++) if (em[q] >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } printf(")"); }
                    printf("\n");
                }
            }
    }
    printf("#END graphs=%llu tested=%llu hits=%llu nonlinear=%llu\n", graphs, tested, hits, nonlin);
    return 0;
}
