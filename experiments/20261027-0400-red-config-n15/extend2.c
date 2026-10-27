/* extend.c -- one step of the level-by-level generation of connected members of class C with max degree <= DMAX.
   Usage: extend NP K DMAX [nofilter] < parents   (parents: canon lines "C m a.b.c ..." on NP vertices, connected, in C)
   For every parent and every way to add ONE edge containing exactly K new vertices (K=0,1,2; new vertices get labels NP, NP+1)
   such that the child is linear, F7-free, satisfies P3 (e(S)<=|S|-2) and has max degree <= DMAX, prints "FOUND: (a,b,c) ..." on NP+K vertices.
   Canonical-deletion filter (reduces duplicates, never loses a class): the child is printed only if the added edge has maximal
   isomorphism-invariant key among the REMOVABLE edges of the child (removable: removing the edge and its private vertices leaves a
   connected hypergraph).  Completeness: every connected child with m>=2 edges has a removable edge (last edge of a BFS edge order);
   take a removable edge e* of maximal key; deleting e* gives a connected parent in C; the child arises from some labelled copy of
   that parent by adding an edge of the same key, which passes the filter.  Final deduplication by canon | sort -u. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t ed[40]; static int ne, NP, K, DMAX = 3, NOF = 0, NV;
static int dg[32]; static uint32_t nb[32];
static int own[32]; static uint32_t fbd;
static int augm(int e, uint32_t *seen) {
    for (uint32_t r = ed[e] & ~fbd & ~*seen; r; r &= r - 1) {
        int v = __builtin_ctz(r); *seen |= 1u << v;
        if (own[v] < 0 || augm(own[v], seen)) { own[v] = e; return 1; }
    }
    return 0;
}
static int c_ok(void) {
    int n1 = ne - 1;
    for (int a = 0; a < n1; a++) { uint32_t U1 = ed[n1] | ed[a]; if (__builtin_popcount(U1) > 7) continue;
     for (int b = a + 1; b < n1; b++) { uint32_t U2 = U1 | ed[b]; if (__builtin_popcount(U2) > 7) continue;
      for (int c = b + 1; c < n1; c++) { uint32_t U3 = U2 | ed[c]; if (__builtin_popcount(U3) > 7) continue;
       for (int d = c + 1; d < n1; d++) { uint32_t U = U3 | ed[d]; if (__builtin_popcount(U) != 7) continue;
        int es[5] = {n1, a, b, c, d}; int d3 = 0, d2 = 0;
        for (uint32_t r = U; r; r &= r - 1) { int v = __builtin_ctz(r), dd = 0; for (int k = 0; k < 5; k++) dd += (ed[es[k]] >> v) & 1; if (dd == 3) d3++; else if (dd == 2) d2++; }
        if (d3 == 1 && d2 == 6) return 0; } } } }
    uint32_t used = 0; for (int i = 0; i < ne; i++) used |= ed[i];
    for (uint32_t rx = used; rx; rx &= rx - 1) { int x = __builtin_ctz(rx);
      for (uint32_t ry = rx & (rx - 1); ry; ry &= ry - 1) { int y = __builtin_ctz(ry);
        fbd = (1u << x) | (1u << y); for (int v = 0; v < 32; v++) own[v] = -1;
        for (int e = 0; e < ne; e++) { uint32_t seen = 0; if (!augm(e, &seen)) return 0; } } }
    return 1;
}
/* key of edge i (isomorphism invariant, independent of removability) */
static int64_t edge_key_nr(int i) {
    uint32_t e = ed[i], priv = 0;
    for (uint32_t r = e; r; r &= r - 1) { int v = __builtin_ctz(r); if (dg[v] == 1) priv |= 1u << v; }
    int dd[3], k = 0; for (uint32_t r = e; r; r &= r - 1) dd[k++] = dg[__builtin_ctz(r)];
    for (int a = 0; a < 3; a++) for (int b = a + 1; b < 3; b++) if (dd[a] < dd[b]) { int t = dd[a]; dd[a] = dd[b]; dd[b] = t; }
    uint32_t adj = 0; for (uint32_t r = e; r; r &= r - 1) adj |= nb[__builtin_ctz(r)];
    adj &= ~e; int S = 0; for (uint32_t r = adj; r; r &= r - 1) S += dg[__builtin_ctz(r)];
    int p = __builtin_popcount(priv);
    return ((int64_t)p << 40) | ((int64_t)dd[0] << 32) | ((int64_t)dd[1] << 28) | ((int64_t)dd[2] << 24) | S;
}
/* removable: removing edge i and its private vertices leaves a connected hypergraph */
static int removable(int i) {
    uint32_t e = ed[i], priv = 0;
    for (uint32_t r = e; r; r &= r - 1) { int v = __builtin_ctz(r); if (dg[v] == 1) priv |= 1u << v; }
    uint32_t verts = 0; for (int j = 0; j < ne; j++) verts |= ed[j];
    verts &= ~priv;
    if (ne < 2) return 0;
    uint32_t comp = 0;
    for (int j = 0; j < ne; j++) if (j != i) { comp = ed[j]; break; }
    uint32_t prev = 0; while (comp != prev) { prev = comp; for (int j = 0; j < ne; j++) if (j != i && (ed[j] & comp)) comp |= ed[j]; }
    return (comp & verts) == verts;
}
static void emit(void) {
    printf("FOUND:"); for (int i = 0; i < ne; i++) { printf(" ("); int f = 1; for (int x = 0; x < 32; x++) if (ed[i] >> x & 1) { printf(f ? "%d" : ",%d", x); f = 0; } printf(")"); }
    printf("\n");
}
static void try_add(int x, int y, int z) {
    ed[ne++] = (1u << x) | (1u << y) | (1u << z);
    dg[x]++; dg[y]++; dg[z]++;
    nb[x] |= (1u << y) | (1u << z); nb[y] |= (1u << x) | (1u << z); nb[z] |= (1u << x) | (1u << y);
    int ok = 1;
    if (!NOF) { int64_t kn = edge_key_nr(ne - 1);
        if (!removable(ne - 1)) ok = 0;
        else for (int j = 0; j < ne - 1 && ok; j++) { int64_t kj = edge_key_nr(j); if (kj > kn && removable(j)) ok = 0; } }
    if (ok && c_ok()) emit();
    ne--; dg[x]--; dg[y]--; dg[z]--;
    nb[x] &= ~((1u << y) | (1u << z)); nb[y] &= ~((1u << x) | (1u << z)); nb[z] &= ~((1u << x) | (1u << y));
}
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage\n"); return 1; }
    NP = atoi(argv[1]); K = atoi(argv[2]); DMAX = atoi(argv[3]); NOF = argc > 4; NV = NP + K;
    static char line[1 << 14];
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] != 'C') continue;
        char *p = line + 1; int m, k; if (sscanf(p, "%d%n", &m, &k) != 1) continue; p += k;
        ne = 0; memset(dg, 0, sizeof dg); memset(nb, 0, sizeof nb);
        for (int i = 0; i < m; i++) { int a, b, c; if (sscanf(p, " %d.%d.%d%n", &a, &b, &c, &k) != 3) return 2; p += k;
            ed[ne++] = (1u << a) | (1u << b) | (1u << c); dg[a]++; dg[b]++; dg[c]++;
            nb[a] |= (1u << b) | (1u << c); nb[b] |= (1u << a) | (1u << c); nb[c] |= (1u << a) | (1u << b); }
        if (K == 0) {
            for (int a = 0; a < NP; a++) if (dg[a] < DMAX) for (int b = a + 1; b < NP; b++) if (dg[b] < DMAX && !(nb[a] >> b & 1))
                for (int c = b + 1; c < NP; c++) if (dg[c] < DMAX && !(nb[a] >> c & 1) && !(nb[b] >> c & 1)) try_add(a, b, c);
        } else if (K == 1) {
            for (int a = 0; a < NP; a++) if (dg[a] < DMAX) for (int b = a + 1; b < NP; b++) if (dg[b] < DMAX && !(nb[a] >> b & 1)) try_add(a, b, NP);
        } else {
            for (int a = 0; a < NP; a++) if (dg[a] < DMAX) try_add(a, NP, NP + 1);
        }
    }
    return 0;
}
