/* ext.c -- referee L010 round 2 (from scratch).  One-vertex extensions with a degree-3 new vertex.
   Usage: ext NG TG MD [print_all_hits] < input   input lines "G: (a,b,c) ..." or "m a b c ..." (graph G on 0..NG-1).
   For every unordered triple of pairwise disjoint pairs {a_i,b_i} of {0..NG-1} with no pair inside an edge of G and every
   endpoint of G-degree <= MD-1, H = G + {NG,a_i,b_i}.  tau(H) is tested DIRECTLY on H: hit iff H has no vertex cover of
   size <= TG (exact branching).  For each hit: linearity, F7 (two disjoint edges f1,f2 + an outside vertex p with >= 3
   edges meeting f1 and f2 once each), (P3) via all edge subsets, connectivity of all NG+1 vertices, max degree.
   Prints "HIT: ... | inC=. conn=. f7=. p3=." (only hits in C or connected unless print_all_hits=1) and a summary. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static uint32_t E[64]; static int ne, NV;
static int coverable(uint64_t left, int k) {
    if (!left) return 1; if (k <= 0) return 0;
    int i = __builtin_ctzll(left); uint32_t e = E[i];
    while (e) { int v = __builtin_ctz(e); e &= e - 1; uint64_t l2 = left;
        for (int j = i; j < ne; j++) if ((l2 >> j & 1) && (E[j] >> v & 1)) l2 &= ~(1ull << j);
        if (coverable(l2, k - 1)) return 1; }
    return 0;
}
static uint64_t ALL(void) { return (ne >= 64) ? ~0ull : ((1ull << ne) - 1); }
static int linear(void) { for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) if (__builtin_popcount(E[i] & E[j]) > 1) return 0; return 1; }
static int f7(void) {
    for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) { if (E[i] & E[j]) continue; uint32_t U = E[i] | E[j];
        for (int p = 0; p < NV; p++) { if (U >> p & 1) continue; int c = 0;
            for (int t = 0; t < ne; t++) if ((E[t] >> p & 1) && __builtin_popcount(E[t] & E[i]) == 1 && __builtin_popcount(E[t] & E[j]) == 1) c++;
            if (c >= 3) return 1; } }
    return 0;
}
static int p3(void) { static uint32_t U[1 << 20]; U[0] = 0; if (ne > 20) exit(7);
    for (uint32_t F = 1; F < (1u << ne); F++) { int lo = __builtin_ctz(F); U[F] = U[F & (F - 1)] | E[lo];
        if (__builtin_popcount(U[F]) < __builtin_popcount(F) + 2) return 0; }
    return 1; }
static int conn(void) { uint32_t R = 1, P = 0; while (R != P) { P = R; for (int j = 0; j < ne; j++) if (E[j] & R) R |= E[j]; } return R == ((1u << NV) - 1); }
static void pr(const char *tag, const char *suffix) {
    printf("%s:", tag); for (int j = 0; j < ne; j++) { uint32_t e = E[j]; int a = __builtin_ctz(e); e &= e - 1; int b = __builtin_ctz(e); e &= e - 1; printf(" (%d,%d,%d)", a, b, __builtin_ctz(e)); }
    printf(" | %s\n", suffix);
}
int main(int argc, char **argv) {
    int NG = atoi(argv[1]), TG = atoi(argv[2]), MD = atoi(argv[3]), PALL = argc > 4 ? atoi(argv[4]) : 0;
    static char line[1 << 16];
    unsigned long long graphs = 0, tested = 0, hits = 0, hitsC = 0, hitsConn = 0, hitsConnC = 0, hitsF7 = 0, hitsP3bad = 0, nonlin = 0, tauG_ne = 0;
    while (fgets(line, sizeof line, stdin)) {
        int ed[64][3], me = 0; char *bar = strchr(line, '|'); if (bar) *bar = 0;
        if (strchr(line, '(')) { char *p = line; while ((p = strchr(p, '('))) { if (sscanf(p, "(%d,%d,%d)", &ed[me][0], &ed[me][1], &ed[me][2]) != 3) return 2; me++; p++; } }
        else { char *p = line; int k, u; if (sscanf(p, "%d%n", &k, &u) != 1) continue; p += u;
            for (int i = 0; i < k; i++) { if (sscanf(p, "%d %d %d%n", &ed[me][0], &ed[me][1], &ed[me][2], &u) != 3) return 2; p += u; me++; } }
        graphs++;
        int deg[32] = {0}; uint32_t G[64]; int mg = me;
        for (int j = 0; j < me; j++) { G[j] = 0; for (int t = 0; t < 3; t++) { if (ed[j][t] < 0 || ed[j][t] >= NG) return 3; G[j] |= 1u << ed[j][t]; deg[ed[j][t]]++; } }
        /* tau(G) for the record */
        memcpy(E, G, sizeof(uint32_t) * mg); ne = mg; NV = NG;
        int tg = 0; while (!coverable(ALL(), tg)) tg++;
        if (tg != TG) tauG_ne++;
        uint32_t P[256]; int np = 0;
        for (int a = 0; a < NG; a++) for (int b = a + 1; b < NG; b++) {
            if (deg[a] > MD - 1 || deg[b] > MD - 1) continue;
            uint32_t pm = (1u << a) | (1u << b); int ok = 1;
            for (int j = 0; j < mg; j++) if ((G[j] & pm) == pm) { ok = 0; break; }
            if (ok) { if (np >= 256) return 4; P[np++] = pm; }
        }
        for (int x = 0; x < np; x++) for (int y = x + 1; y < np; y++) { if (P[x] & P[y]) continue;
            for (int z = y + 1; z < np; z++) { if ((P[x] | P[y]) & P[z]) continue;
                tested++;
                memcpy(E, G, sizeof(uint32_t) * mg); ne = mg; NV = NG + 1;
                uint32_t nvb = 1u << NG; E[ne++] = P[x] | nvb; E[ne++] = P[y] | nvb; E[ne++] = P[z] | nvb;
                if (coverable(ALL(), TG)) continue;          /* tau(H) <= TG: not a hit */
                hits++;
                int li = linear(); if (!li) nonlin++;
                int f = f7(), q = p3(), c = conn(), inC = li && !f && q;
                hitsF7 += f; hitsP3bad += !q; hitsC += inC; hitsConn += c; hitsConnC += (c && inC);
                if (PALL || inC || c) { char s[96]; sprintf(s, "inC=%d conn=%d f7=%d p3=%d", inC, c, f, q); pr("HIT", s); }
            } }
    }
    printf("EXTSUMMARY NG=%d TG=%d MD=%d graphs=%llu tauG_not_TG=%llu tested=%llu hits=%llu nonlinear=%llu hits_F7=%llu hits_P3bad=%llu hits_inC=%llu hits_conn=%llu hits_conn_inC=%llu\n",
           NG, TG, MD, graphs, tauG_ne, tested, hits, nonlin, hitsF7, hitsP3bad, hitsC, hitsConn, hitsConnC);
    return 0;
}
