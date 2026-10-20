/* Referee L009 round 3: my own one-vertex extension with a DEFINITIONAL tau test (no reuse of the transversal list idea).
   Input lines: "G ...: (a,b,c) (d,e,f) ..." or "FOUND: (..) .." or any "TAG: (..)" line: a 3-graph G on vertices 0..NG-1.
   For each G and each unordered triple of pairwise disjoint pairs {a_i,b_i} with (i) no pair inside an edge of G,
   (ii) deg_G(a_i), deg_G(b_i) <= MAXDEG-1, form H = G + {NG,a_i,b_i} (3 edges) and compute tau(H) exactly by branching
   (is there a vertex set of size <= k meeting all edges, k = 0,1,2,...). Report every H with tau(H) >= THIT, and a histogram
   of tau(H) - tau(G). Usage: myext NG THIT MAXDEG < input */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t E[40]; static int ne;
static int coverable(uint32_t alive, int k) {
    if (!alive) return 1; if (k <= 0) return 0;
    uint32_t used = 0; int mt = 0; for (int j = 0; j < ne; j++) if ((alive >> j & 1) && !(E[j] & used)) { used |= E[j]; mt++; }
    if (mt > k) return 0;
    int i = __builtin_ctz(alive); uint32_t e = E[i];
    while (e) { int x = __builtin_ctz(e); e &= e - 1; uint32_t rest = alive;
        for (int j = 0; j < ne; j++) if (E[j] >> x & 1) rest &= ~(1u << j);
        if (coverable(rest, k - 1)) return 1; }
    return 0;
}
static int tau_exact(void) { uint32_t all = ne >= 32 ? 0xffffffffu : ((1u << ne) - 1); int k = 0; while (!coverable(all, k)) k++; return k; }
static void print_graph(FILE *f, int nv) {
    for (int j = 0; j < ne; j++) { fprintf(f, " ("); int first = 1; for (int v = 0; v < nv; v++) if (E[j] >> v & 1) { fprintf(f, first ? "%d" : ",%d", v); first = 0; } fprintf(f, ")"); }
}
int main(int argc, char **argv) {
    int NG = atoi(argv[1]), THIT = atoi(argv[2]), MD = atoi(argv[3]);
    char line[8192]; unsigned long long graphs = 0, tested = 0, hits = 0; long long hist[8] = {0};
    int tauG_min = 99, tauG_max = -1;
    while (fgets(line, sizeof line, stdin)) {
        char *p = strchr(line, ':'); if (!p) continue;
        ne = 0; int deg[32] = {0};
        while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) { fprintf(stderr, "parse\n"); return 2; }
            E[ne++] = (1u << a) | (1u << b) | (1u << c); deg[a]++; deg[b]++; deg[c]++; p++; }
        if (ne == 0) continue;
        graphs++;
        int m = ne; int tG = tau_exact(); if (tG < tauG_min) tauG_min = tG; if (tG > tauG_max) tauG_max = tG;
        uint32_t pr[300]; int np = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > MD - 1 || deg[b] > MD - 1) continue;
            uint32_t q = (1u << a) | (1u << b); int inside = 0;
            for (int j = 0; j < m; j++) if ((E[j] & q) == q) { inside = 1; break; }
            if (!inside) pr[np++] = q;
        }
        for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) { if (pr[x] & pr[y]) continue;
            for (int z = y + 1; z < np; z++) { if ((pr[x] | pr[y]) & pr[z]) continue;
                ne = m + 3; E[m] = pr[x] | (1u << NG); E[m + 1] = pr[y] | (1u << NG); E[m + 2] = pr[z] | (1u << NG);
                tested++;
                int tH = tau_exact(); int dlt = tH - tG; if (dlt < 0) dlt = 0; if (dlt > 7) dlt = 7; hist[dlt]++;
                if (tH >= THIT) { hits++; printf("HIT tau=%d:", tH); print_graph(stdout, NG + 1); printf("\n"); }
                ne = m; } }
    }
    printf("MYEXT NG=%d THIT=%d MAXDEG=%d graphs=%llu tauG_range=[%d,%d] tested=%llu hits=%llu hist(tauH-tauG)=[%lld,%lld,%lld,%lld]\n",
           NG, THIT, MD, graphs, tauG_min, tauG_max, tested, hits, hist[0], hist[1], hist[2], hist[3]);
    return 0;
}
