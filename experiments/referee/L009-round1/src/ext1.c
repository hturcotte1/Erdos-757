/* Referee L009: my own one-vertex extension step (written independently of ext_indep2/ext_vertex2).
   Usage: ext1 N TARGET MAXDEG [PRINTALL] < file   (every line containing ':' and groups "(a,b,c)" is an input G on vertices 0..N-1)
   For each G: tau(G) computed exactly (branching), then EVERY H = G + {N,a1,b1} + {N,a2,b2} + {N,a3,b3} with the three pairs
   pairwise disjoint, no pair inside an edge of G (linearity of H), and deg_G(a_i), deg_G(b_i) <= MAXDEG-1 (so Delta(H) <= MAXDEG
   when Delta(G) <= MAXDEG), is formed; tau(H) computed exactly; H printed as "X tau=.. C=.. conn=..:" if tau(H) >= TARGET
   (or always if PRINTALL).  C = linear, F7-free (5 edges on 7 vertices with a disjoint pair), (P3) |U(F)| >= |F|+2 for all F.
   conn = the hypergraph is connected and covers all N+1 vertices.  Summary: histogram of tau(H) - tau(G). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint64_t E[64]; static int ne;
static int cover_le(uint64_t left, int k) {     /* left: bitmask over edge indices */
    if (!left) return 1;
    if (k <= 0) return 0;
    /* branch on the unmet edge with the smallest index */
    int i = __builtin_ctzll(left); uint64_t e = E[i];
    while (e) {
        int x = __builtin_ctzll(e); e &= e - 1;
        uint64_t l2 = left;
        for (int j = 0; j < ne; j++) if ((l2 >> j & 1) && (E[j] >> x & 1)) l2 &= ~(1ull << j);
        if (cover_le(l2, k - 1)) return 1;
    }
    return 0;
}
static int tau(void) { uint64_t all = ne >= 64 ? ~0ull : ((1ull << ne) - 1); for (int k = 0;; k++) if (cover_le(all, k)) return k; }
static int linear(void) { for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) if (__builtin_popcountll(E[i] & E[j]) > 1) return 0; return 1; }
static int f7(void) {
    int ix[5];
    for (ix[0] = 0; ix[0] < ne; ix[0]++) for (ix[1] = ix[0]+1; ix[1] < ne; ix[1]++) for (ix[2] = ix[1]+1; ix[2] < ne; ix[2]++)
    for (ix[3] = ix[2]+1; ix[3] < ne; ix[3]++) for (ix[4] = ix[3]+1; ix[4] < ne; ix[4]++) {
        uint64_t U = 0; for (int a = 0; a < 5; a++) U |= E[ix[a]];
        if (__builtin_popcountll(U) != 7) continue;
        for (int a = 0; a < 5; a++) for (int b = a + 1; b < 5; b++) if (!(E[ix[a]] & E[ix[b]])) return 1;
    }
    return 0;
}
static int p3(void) {
    for (uint32_t F = 1; F < (1u << ne); F++) { uint64_t U = 0; for (int j = 0; j < ne; j++) if (F >> j & 1) U |= E[j];
        if (__builtin_popcountll(U) < __builtin_popcount(F) + 2) return 0; }
    return 1;
}
static int conn(int nv) {
    uint64_t comp = E[0], prev = 0;
    while (comp != prev) { prev = comp; for (int i = 0; i < ne; i++) if (E[i] & comp) comp |= E[i]; }
    return comp == ((nv >= 64) ? ~0ull : ((1ull << nv) - 1));
}
static void pr(const char *tag, int t, int c, int cn, int nv) {
    printf("%s tau=%d C=%d conn=%d:", tag, t, c, cn);
    for (int i = 0; i < ne; i++) { printf(" ("); int f = 1; for (int v = 0; v < nv; v++) if (E[i] >> v & 1) { printf(f ? "%d" : ",%d", v); f = 0; } printf(")"); }
    printf("\n");
}
int main(int argc, char **argv) {
    int N = atoi(argv[1]), TARGET = atoi(argv[2]), MD = atoi(argv[3]), PALL = argc > 4 ? atoi(argv[4]) : 0;
    static char line[1 << 16];
    unsigned long long graphs = 0, tested = 0, hits = 0, hitsC = 0, hitsCconn = 0, hist[4] = {0, 0, 0, 0};
    int tGmin = 99, tGmax = -1;
    while (fgets(line, sizeof line, stdin)) {
        char *p = strchr(line, ':'); if (!p) continue;
        int m0 = 0; uint64_t G[64]; int deg[64] = {0};
        while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) return 2;
            if (a >= N || b >= N || c >= N) { fprintf(stderr, "label >= N\n"); return 3; }
            G[m0++] = (1ull << a) | (1ull << b) | (1ull << c); deg[a]++; deg[b]++; deg[c]++; p++; }
        graphs++;
        ne = m0; memcpy(E, G, sizeof(uint64_t) * m0);
        int tG = tau(); if (tG < tGmin) tGmin = tG; if (tG > tGmax) tGmax = tG;
        uint64_t P[2048]; int np = 0;
        for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) {
            if (deg[a] > MD - 1 || deg[b] > MD - 1) continue;
            uint64_t q = (1ull << a) | (1ull << b); int ok = 1;
            for (int i = 0; i < m0; i++) if ((G[i] & q) == q) { ok = 0; break; }
            if (ok) P[np++] = q;
        }
        uint64_t x = 1ull << N;
        for (int i = 0; i < np; i++) for (int j = i + 1; j < np; j++) { if (P[i] & P[j]) continue;
          for (int k = j + 1; k < np; k++) { if ((P[i] | P[j]) & P[k]) continue;
            tested++;
            ne = m0 + 3; E[m0] = P[i] | x; E[m0 + 1] = P[j] | x; E[m0 + 2] = P[k] | x;
            uint64_t all = (1ull << ne) - 1;
            int tH = cover_le(all, tG) ? (cover_le(all, tG - 1) ? -1 : tG) : tG + 1;   /* tau(H) in {tG, tG+1}; -1 = impossible */
            if (tH < 0) { fprintf(stderr, "tau decreased?!\n"); return 4; }
            hist[tH - tG]++;
            if (tH >= TARGET || PALL) {
                int c = linear() && !f7() && p3(), cn = conn(N + 1);
                if (tH >= TARGET) { hits++; hitsC += c; hitsCconn += c && cn; }
                pr("X", tH, c, cn, N + 1);
            }
          } }
    }
    fprintf(stderr, "EXT1 N=%d TARGET=%d MAXDEG=%d graphs=%llu tau(G)_range=[%d,%d] tested=%llu tau(H)-tau(G): 0:%llu 1:%llu | hits(tau>=TARGET)=%llu hits_in_C=%llu hits_in_C_connected=%llu\n",
            N, TARGET, MD, graphs, tGmin, tGmax, tested, hist[0], hist[1], hits, hitsC, hitsCconn);
    return 0;
}
