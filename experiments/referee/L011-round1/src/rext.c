/* Referee L011: vertex-extension step, written from scratch.
   Usage: rext NG TH MAXDEG < inputs
     inputs: lines "TAG: (a,b,c) ..." (any tag) or "m a1 b1 c1 ..."; each is a 3-graph G on points 0..NG-1 (isolated points
     allowed: every label < NG is a point).
   For every unordered triple of pairwise disjoint pairs {c_j,d_j} of points of G such that no pair lies inside an edge of G
   and every c_j,d_j has G-degree <= MAXDEG-1, form H = G + {c_j,d_j,NG} (j=1,2,3), and test DIRECTLY on H whether
   tau(H) >= TH (no set of TH-1 points of H meets every edge of H; branch-and-bound on H itself, point NG included).
   Prints "HIT: <edges of H>" for every such H, then "RSUMMARY inputs=.. tested=.. hits=.. tauG_min=.. tauG_max=..". */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static uint32_t E[40]; static uint64_t INC[40]; static int NE;
static int cover_le(uint64_t left, int k) {
    if (!left) return 1;
    if (k <= 0) return 0;
    { uint32_t used = 0; int cnt = 0; uint64_t l = left;
      while (l) { int i = __builtin_ctzll(l); l &= l - 1; if (!(E[i] & used)) { used |= E[i]; if (++cnt > k) return 0; } } }
    /* branch on the uncovered edge with the fewest... simply the first uncovered edge */
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int x = __builtin_ctz(e); e &= e - 1; if (cover_le(left & ~INC[x], k - 1)) return 1; }
    return 0;
}
static int tau_of(int np) { uint64_t all = (NE >= 64) ? ~0ull : ((1ull << NE) - 1); int k = 0; while (!cover_le(all, k)) k++; (void)np; return k; }
static void build_inc(int np) { for (int x = 0; x < np; x++) INC[x] = 0; for (int i = 0; i < NE; i++) for (int x = 0; x < np; x++) if (E[i] >> x & 1) INC[x] |= 1ull << i; }
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: rext NG TH MAXDEG\n"); return 1; }
    int NG = atoi(argv[1]), TH = atoi(argv[2]), MD = atoi(argv[3]);
    static char line[1 << 16];
    unsigned long long inputs = 0, tested = 0, hits = 0; int tmin = 99, tmax = -1;
    while (fgets(line, sizeof line, stdin)) {
        int ed[40][3], m = 0; char *p = line; while (*p == ' ') p++;
        if (*p >= '0' && *p <= '9') { m = (int)strtol(p, &p, 10); for (int i = 0; i < m; i++) for (int j = 0; j < 3; j++) ed[i][j] = (int)strtol(p, &p, 10); }
        else { char *c = strchr(line, ':'); if (!c) continue; p = c + 1;
               while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[m][0], &ed[m][1], &ed[m][2]) != 3) return 2; m++; p++; } }
        inputs++;
        int deg[40] = {0}; uint32_t G[40];
        for (int i = 0; i < m; i++) { G[i] = 0; for (int j = 0; j < 3; j++) { if (ed[i][j] >= NG) { fprintf(stderr, "label >= NG\n"); return 3; } G[i] |= 1u << ed[i][j]; deg[ed[i][j]]++; } }
        /* tau(G), for the record */
        NE = m; for (int i = 0; i < m; i++) E[i] = G[i]; build_inc(NG);
        int tg = tau_of(NG); if (tg < tmin) tmin = tg; if (tg > tmax) tmax = tg;
        /* admissible pairs */
        uint32_t pr[512]; int np = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > MD - 1 || deg[b] > MD - 1) continue;
            uint32_t q = (1u << a) | (1u << b); int inside = 0;
            for (int i = 0; i < m; i++) if ((G[i] & q) == q) { inside = 1; break; }
            if (!inside) pr[np++] = q;
        }
        NE = m + 3; for (int i = 0; i < m; i++) E[i] = G[i];
        uint32_t w = 1u << NG;
        for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) {
            if (pr[x] & pr[y]) continue;
            for (int z = y + 1; z < np; z++) {
                if ((pr[x] | pr[y]) & pr[z]) continue;
                tested++;
                E[m] = pr[x] | w; E[m + 1] = pr[y] | w; E[m + 2] = pr[z] | w;
                build_inc(NG + 1);
                if (cover_le((1ull << NE) - 1, TH - 1)) continue;   /* tau(H) <= TH-1 */
                hits++;
                printf("HIT:");
                for (int i = 0; i < NE; i++) { int v[3], k = 0; for (int t = 0; t <= NG; t++) if (E[i] >> t & 1) v[k++] = t; printf(" (%d,%d,%d)", v[0], v[1], v[2]); }
                printf("\n");
            }
        }
    }
    printf("RSUMMARY inputs=%llu tested=%llu hits=%llu tauG_min=%d tauG_max=%d\n", inputs, tested, hits, tmin, tmax);
    return 0;
}
