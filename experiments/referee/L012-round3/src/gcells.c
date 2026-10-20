/* gcells.c (referee L012 round 3) -- read genbg graph6 output (bipartite: n1 hypergraph vertices, n2 edge-vertices of degree 3),
   convert to 3-graphs and keep those in C with tau == T exactly, connected on all n1 vertices, max degree <= D.
   Own filters: linear (pairwise edge intersections <= 1; genbg -Z1 already guarantees it), F7 (centre-based), (P3) brute force over
   all nonempty edge subsets, tau by brute force over k-subsets, connectivity by union-find.
   Usage: gcells n1 n2 T D < graph6   Output: "FOUND: (a,b,c) ..." lines and a SUMMARY. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int n1, n2, T, D; static uint32_t E[48]; static int ne;
static int is_edge(uint32_t mask) { for (int i = 0; i < ne; i++) if (E[i] == mask) return 1; return 0; }
static int has_f7(void) {
    for (int p = 0; p < n1; p++) {
        int at[16], na = 0; for (int i = 0; i < ne; i++) if (E[i] >> p & 1) at[na++] = i;
        if (na < 3) continue;
        for (int i = 0; i < na; i++) for (int j = i + 1; j < na; j++) for (int k = j + 1; k < na; k++) {
            int pr[3][2]; int es[3] = {at[i], at[j], at[k]};
            for (int q = 0; q < 3; q++) { uint32_t r = E[es[q]] & ~(1u << p); pr[q][0] = __builtin_ctz(r); r &= r - 1; pr[q][1] = __builtin_ctz(r); }
            for (int s2 = 0; s2 < 2; s2++) for (int s3 = 0; s3 < 2; s3++) {
                uint32_t t1 = (1u << pr[0][0]) | (1u << pr[1][s2]) | (1u << pr[2][s3]);
                uint32_t t2 = (1u << pr[0][1]) | (1u << pr[1][1 - s2]) | (1u << pr[2][1 - s3]);
                if (is_edge(t1) && is_edge(t2)) return 1;
            }
        }
    }
    return 0;
}
static int p3_ok(void) {
    int cnt[32]; memset(cnt, 0, sizeof cnt); int nv = 0, nf = 0;
    unsigned long long total = 1ull << ne;
    for (unsigned long long g = 1; g < total; g++) {
        int bit = __builtin_ctzll(g); uint32_t em = E[bit]; int adding = (((g ^ (g >> 1)) >> bit) & 1);
        if (adding) { nf++; for (uint32_t r = em; r; r &= r - 1) { int v = __builtin_ctz(r); if (cnt[v]++ == 0) nv++; } }
        else { nf--; for (uint32_t r = em; r; r &= r - 1) { int v = __builtin_ctz(r); if (--cnt[v] == 0) nv--; } }
        if (nf >= 1 && nv < nf + 2) return 0;
    }
    return 1;
}
static int has_cover(int k) {
    int idx[32]; for (int i = 0; i < k; i++) idx[i] = i;
    while (1) {
        uint32_t S = 0; for (int i = 0; i < k; i++) S |= 1u << idx[i];
        int ok = 1; for (int i = 0; i < ne; i++) if (!(E[i] & S)) { ok = 0; break; }
        if (ok) return 1;
        int i = k - 1; while (i >= 0 && idx[i] == n1 - k + i) i--; if (i < 0) return 0;
        idx[i]++; for (int j = i + 1; j < k; j++) idx[j] = idx[j - 1] + 1;
    }
}
static int tau(void) { for (int k = 0; k <= n1; k++) if (has_cover(k)) return k; return n1; }
static int connected_all(void) {
    int par[40]; for (int i = 0; i < n1; i++) par[i] = i;
    #define FIND(x) ({ int _x = (x); while (par[_x] != _x) _x = par[_x] = par[par[_x]]; _x; })
    for (int i = 0; i < ne; i++) { int v[3], k = 0; for (uint32_t r = E[i]; r; r &= r - 1) v[k++] = __builtin_ctz(r); par[FIND(v[1])] = FIND(v[0]); par[FIND(v[2])] = FIND(v[0]); }
    int r0 = FIND(0); for (int i = 1; i < n1; i++) if (FIND(i) != r0) return 0; return 1;
}
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: gcells n1 n2 T D < graph6\n"); return 1; }
    n1 = atoi(argv[1]); n2 = atoi(argv[2]); T = atoi(argv[3]); D = atoi(argv[4]);
    static char line[1 << 12]; unsigned long long tot = 0, nlin = 0, nf7 = 0, np3 = 0, ntau = 0, nconn = 0, ndeg = 0, found = 0;
    int n = n1 + n2;
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '>' || line[0] == '\n') continue;
        char *p = line; if (*p == ':' || *p == '&') { fprintf(stderr, "not graph6\n"); return 2; }
        int nn = *p - 63; p++; if (nn != n) { fprintf(stderr, "n mismatch %d vs %d\n", nn, n); return 2; }
        /* adjacency bits: for j = 1..n-1, i = 0..j-1 in order, 6 bits per char */
        static int adj[64][64]; memset(adj, 0, sizeof adj);
        int bitpos = 0;
        for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) {
            int ch = p[bitpos / 6] - 63; int bit = (ch >> (5 - bitpos % 6)) & 1; bitpos++;
            adj[i][j] = adj[j][i] = bit;
        }
        tot++;
        ne = 0; int ok = 1;
        for (int j = n1; j < n; j++) { uint32_t mk = 0; int c = 0; for (int i = 0; i < n1; i++) if (adj[i][j]) { mk |= 1u << i; c++; }
            if (c != 3) { ok = 0; break; } E[ne++] = mk; }
        for (int i = 0; i < n1; i++) for (int j = i + 1; j < n1; j++) if (adj[i][j]) ok = 0;
        if (!ok) { fprintf(stderr, "unexpected bipartite structure\n"); return 3; }
        int lin = 1; for (int i = 0; i < ne && lin; i++) for (int j = i + 1; j < ne; j++) if (__builtin_popcount(E[i] & E[j]) >= 2) { lin = 0; break; }
        if (!lin) continue; nlin++;
        if (has_f7()) { nf7++; continue; }
        if (!p3_ok()) { np3++; continue; }
        if (tau() != T) { ntau++; continue; }
        if (!connected_all()) { nconn++; continue; }
        int dmax = 0; for (int v = 0; v < n1; v++) { int d = 0; for (int i = 0; i < ne; i++) d += E[i] >> v & 1; if (d > dmax) dmax = d; }
        if (dmax > D) { ndeg++; continue; }
        found++;
        printf("FOUND:"); for (int i = 0; i < ne; i++) { int v[3], k = 0; for (uint32_t r = E[i]; r; r &= r - 1) v[k++] = __builtin_ctz(r); printf(" (%d,%d,%d)", v[0], v[1], v[2]); } printf("\n");
    }
    printf("SUMMARY n1=%d n2=%d T=%d D=%d total=%llu linear=%llu contain_F7=%llu P3_violated=%llu wrong_tau=%llu disconnected=%llu degree_too_large=%llu found=%llu\n",
           n1, n2, T, D, tot, nlin, nf7, np3, ntau, nconn, ndeg, found);
    return 0;
}
