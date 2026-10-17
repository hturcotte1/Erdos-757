/* myfilter.c -- referee L010 round 2.  Usage: myfilter TAG NV [match] < file   (lines "TAG: (a,b,c) ...", text after '|' ignored)
   Per graph: linear; F7 (two disjoint edges + outside vertex with >= 3 edges meeting both once; valid for linear graphs);
   (P3) e(S) <= |S|-2 for all |S|>=2, tested (a) as |union F| >= |F|+2 for all nonempty edge sets F and, with 'match',
   (b) by Hall: for every vertex pair {u,w} the incidence bigraph minus u,w has a matching saturating all edges
   [(b) <=> (a): Hall's condition in B-{u,w} for all u,w is |N(F)-{u,w}| >= |F|, i.e. |N(F)| >= |F|+2 taking u,w in N(F)];
   connectivity over all NV vertices and over the non-isolated vertices; max degree.  Prints a summary. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static uint32_t E[64]; static int ne, NV;
static int linear(void) { for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) if (__builtin_popcount(E[i] & E[j]) > 1) return 0; return 1; }
static int f7(void) {
    for (int i = 0; i < ne; i++) for (int j = i + 1; j < ne; j++) { if (E[i] & E[j]) continue; uint32_t U = E[i] | E[j];
        for (int p = 0; p < NV; p++) { if (U >> p & 1) continue; int c = 0;
            for (int t = 0; t < ne; t++) if ((E[t] >> p & 1) && __builtin_popcount(E[t] & E[i]) == 1 && __builtin_popcount(E[t] & E[j]) == 1) c++;
            if (c >= 3) return 1; } }
    return 0; }
static int p3_subsets(void) { static uint32_t U[1 << 20]; if (ne > 20) exit(7); U[0] = 0;
    for (uint32_t F = 1; F < (1u << ne); F++) { int hi = 31 - __builtin_clz(F); U[F] = U[F ^ (1u << hi)] | E[hi];
        if (__builtin_popcount(U[F]) < __builtin_popcount(F) + 2) return 0; } return 1; }
static int mate_v[32], mate_e[64], seen[32];
static uint32_t avail;
static int aug(int e) { uint32_t c = E[e] & avail; while (c) { int v = __builtin_ctz(c); c &= c - 1; if (seen[v]) continue; seen[v] = 1;
        if (mate_v[v] < 0 || aug(mate_v[v])) { mate_v[v] = e; mate_e[e] = v; return 1; } } return 0; }
static int p3_match(void) {
    for (int u = 0; u < NV; u++) for (int w = u + 1; w < NV; w++) {
        avail = ((NV >= 32) ? 0xffffffffu : ((1u << NV) - 1)) & ~((1u << u) | (1u << w));
        for (int v = 0; v < 32; v++) mate_v[v] = -1;
        for (int e = 0; e < ne; e++) { memset(seen, 0, sizeof seen); if (!aug(e)) return 0; }
    }
    return 1; }
static int conn_all(void) { uint32_t R = 1, P = 0; while (R != P) { P = R; for (int j = 0; j < ne; j++) if (E[j] & R) R |= E[j]; } return R == ((1u << NV) - 1); }
static int conn_edges(void) { uint32_t used = 0; for (int j = 0; j < ne; j++) used |= E[j]; uint32_t R = E[0], P = 0;
    while (R != P) { P = R; for (int j = 0; j < ne; j++) if (E[j] & R) R |= E[j]; } return R == used; }
int main(int argc, char **argv) {
    const char *tag = argv[1]; NV = atoi(argv[2]); int MATCH = argc > 3 && !strcmp(argv[3], "match");
    static char line[1 << 16]; size_t tl = strlen(tag);
    unsigned long long tot = 0, lin = 0, nf7 = 0, p3bad = 0, f7free_p3bad = 0, surv = 0, ca = 0, ce = 0, mism = 0, maxdeg = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (strncmp(line, tag, tl) || line[tl] != ':') continue;
        char *bar = strchr(line, '|'); if (bar) *bar = 0;
        ne = 0; char *p = line; while ((p = strchr(p, '('))) { int a, b, c; if (sscanf(p, "(%d,%d,%d)", &a, &b, &c) != 3) return 2;
            if (a < 0 || b < 0 || c < 0 || a >= NV || b >= NV || c >= NV) return 3; E[ne++] = (1u << a) | (1u << b) | (1u << c); p++; }
        tot++;
        int L = linear(), F = f7(), Q = p3_subsets();
        if (MATCH) { int Q2 = p3_match(); if (Q2 != Q) mism++; }
        lin += L; nf7 += F; p3bad += !Q; f7free_p3bad += (!F && !Q); surv += (L && !F && Q); ca += conn_all(); ce += conn_edges();
        for (int v = 0; v < NV; v++) { unsigned long long d = 0; for (int j = 0; j < ne; j++) d += E[j] >> v & 1; if (d > maxdeg) maxdeg = d; }
    }
    printf("MYFILTER tag=%s NV=%d total=%llu linear=%llu F7=%llu P3_violated=%llu F7free_and_P3_violated=%llu inC=%llu conn_allvertices=%llu conn_edgepart=%llu maxdeg=%llu%s",
           tag, NV, tot, lin, nf7, p3bad, f7free_p3bad, surv, ca, ce, maxdeg, MATCH ? "" : "\n");
    if (MATCH) printf(" P3_subset_vs_matching_mismatches=%llu\n", mism);
    return 0;
}
